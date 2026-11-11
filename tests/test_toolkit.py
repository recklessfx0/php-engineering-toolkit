import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/php-engineer/scripts"
sys.path[:0] = [str(SCRIPTS), str(ROOT / "scripts")]
from configuration import load_config
from export_prompt import render
from inspect_project import inspect
from install_skills import install
from quality_gate import check, gate
from route_task import route
from validate_skills import validate


class TemporaryProjectTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

class ToolkitTests(TemporaryProjectTest):
    def test_catalog(self):
        self.assertEqual(validate(ROOT / "skills"), [])

    def test_bad_catalog(self):
        header = '---\nname: php-core\ndescription: "Core"\n---\n'
        self.write("php-core/SKILL.md", header + "[missing](references/missing.md)")
        self.write("duplicate/SKILL.md", header + "Instructions")
        self.write("broken/SKILL.md", "Missing metadata")
        issues = "\n".join(validate(self.root))
        for message in ("duplicate skill name", "missing required skill",
                        "missing or unsafe reference", "expected canonical"):
            self.assertIn(message, issues)

    def test_install_complete_and_conflict(self):
        destination = self.root / ".agents/skills"
        self.assertEqual(len(install(destination)), 9)
        inspector = destination / "php-engineer/scripts/inspect_project.py"
        completed = subprocess.run(
            [sys.executable, str(inspector), str(self.root)],
            capture_output=True, check=True, text=True,
        )
        self.assertEqual(json.loads(completed.stdout)["framework"], "unknown")
        with self.assertRaisesRegex(ValueError, "Existing destinations"):
            install(destination)

    def test_install_cli_host_paths(self):
        for host in ("shared", "claude", "codex", "gemini", "copilot"):
            with self.subTest(host=host):
                project = self.root / host
                project.mkdir()
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts/install_skills.py"),
                     "--host", host, "--repo", str(project)],
                    check=True, capture_output=True,
                )
                namespace = ".claude" if host == "claude" else ".agents"
                skill = project / namespace / "skills/php-engineer"
                self.assertTrue((skill / "SKILL.md").is_file())
                self.assertTrue((skill / "scripts/quality_gate.py").is_file())

    def test_prompt_export_is_selective(self):
        prompt = render(["php-engineer", "api-development", "api-development"])
        self.assertIn("## Task and project context", prompt)
        self.assertIn("bound page sizes", prompt)
        self.assertEqual(prompt.count("# api-development workflow"), 1)
        self.assertNotIn("# php-performance workflow", prompt)
        self.assertNotIn("](references/", prompt)
        with self.assertRaises(ValueError):
            render(["../README"])

    def test_prompt_export_does_not_overwrite(self):
        output = self.write("prompt.md", "Keep this")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/export_prompt.py"),
             "php-core", "--output", str(output)],
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_text(encoding="utf-8"), "Keep this")

    def test_project_examples(self):
        php = inspect(ROOT / "examples/plain-php")
        laravel = inspect(ROOT / "examples/laravel")
        self.assertEqual(php["php"]["constraint"], "^8.1")
        self.assertEqual(php["php"]["target_override"], "8.1")
        self.assertEqual(php["framework"], "plain-php")
        self.assertEqual(laravel["framework"], "laravel")
        self.assertEqual(laravel["tools"]["pest"]["required"], "^3.0")
        self.assertIn("phpstan.neon", laravel["configurations"])

    def test_versions_from_lock_and_vendor(self):
        self.write("composer.lock", '{"packages":[{"name":"symfony/framework-bundle","version":"7.0"}]}')
        self.write("vendor/composer/installed.json", '{"packages":[{"name":"phpstan/phpstan","version":"2.1"}]}')
        found = inspect(self.root)
        self.assertEqual(found["framework_versions"], {"symfony/framework-bundle": "7.0"})
        self.assertEqual(found["framework"], "symfony")
        self.assertEqual(found["tools"]["phpstan"]["installed"], "2.1")

    def test_malformed_composer(self):
        self.write("composer.json", "[]")
        self.write("composer.lock", "{")
        self.assertEqual(len(inspect(self.root)["warnings"]), 2)

    def test_config_merge(self):
        self.write(".php-engineering-toolkit.json", '{"quality":{"run_tests":false}}')
        result = load_config(self.root)
        self.assertFalse(result["quality"]["run_tests"])
        self.assertTrue(result["quality"]["run_static_analysis"])

    def test_invalid_settings(self):
        for invalid in (
            '{"quality":{"phpstan_level":true}}', '{"quality":{"phpstan_level":11}}',
            '{"quality":{"run_tests":1}}', '{"framework":"other"}',
            '{"quality":{"typo":true}}', '{"framework":"auto","framework":"laravel"}',
        ):
            with self.subTest(invalid=invalid):
                self.write(".php-engineering-toolkit.json", invalid)
                with self.assertRaises(ValueError):
                    load_config(self.root)

    def test_route(self):
        self.assertEqual(route(["analysis"], "laravel"), ["phpstan-analysis", "php-core"])
        self.assertEqual(route(["refactor", "testing"], "laravel"),
                         ["php-refactoring", "laravel-development", "php-testing"])
        self.assertEqual(route(["performance"], "laravel"),
                         ["php-performance", "laravel-development"])
        self.assertEqual(set(route(["api"], "laravel")), {
            "api-development", "laravel-development", "php-testing",
            "security-audit", "phpstan-analysis",
        })


class GateTests(TemporaryProjectTest):
    # Keep the gate fixtures independent of the installed PHP/Composer version.
    def options(self, **changes):
        options = dict(only=None, trusted=False, network=False, timeout=2,
                       diagnostics=False, custom=None)
        return argparse.Namespace(**(options | changes))

    def test_untrusted_does_not_execute_project_tools(self):
        self.write("vendor/bin/pest", "<?php exit(1);")
        with patch("quality_gate.check") as run:
            result = gate(self.root, self.options(), load_config(self.root))
        run.assert_not_called()
        self.assertEqual(next(item for item in result if item["check"] == "tests")["status"], "skipped")

    def test_trusted_uses_argv_and_level(self):
        entry = self.write("vendor/bin/phpstan", "<?php")
        source = self.write("src/Foo.php", "<?php")
        with patch("quality_gate.shutil.which", return_value="php"), patch("quality_gate.check") as run:
            gate(self.root, self.options(only=["analysis"], trusted=True), load_config(self.root))
        self.assertEqual(run.call_args.args[2], [
            "php", str(entry), "analyse", "--no-progress", "--no-interaction",
            "--level", "6", str(source.parent),
        ])

    @unittest.skipUnless(shutil.which("php"), "PHP CLI unavailable")
    def test_trusted_vendor_checks_execute_and_report_failures(self):
        self.write("src/Foo.php", "<?php")
        self.write("vendor/bin/phpstan", '<?php echo $argv[1]; exit(1);')
        self.write("vendor/bin/pest", '<?php echo "pest";')
        self.write("vendor/bin/phpunit", '<?php exit(99);')
        self.write("vendor/bin/pint", '<?php echo $argv[1];')
        results = gate(
            self.root,
            self.options(only=["analysis", "tests", "format"], trusted=True, diagnostics=True),
            load_config(self.root),
        )
        by_name = {result["check"]: result for result in results}
        self.assertEqual(by_name["analysis"]["status"], "fail")
        self.assertEqual(by_name["analysis"]["stdout"], "analyse")
        self.assertEqual(by_name["tests"]["stdout"], "pest")
        self.assertEqual(by_name["format"]["stdout"], "--test")

    def test_custom_rejects_shell_wrappers(self):
        with self.assertRaises(ValueError):
            gate(self.root, self.options(only=["tests"], trusted=True,
                                        custom=[str(self.root / "tool.cmd")]), load_config(self.root))

    def test_metacharacters_are_literal(self):
        result = check(self.root, "custom",
                       [sys.executable, "-c", "import sys; print(sys.argv[1])", "a & b | c"],
                       10, True)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["stdout"].strip(), "a & b | c")

    def test_launch_error_and_timeout(self):
        with patch("quality_gate.subprocess.run", side_effect=OSError):
            self.assertEqual(check(self.root, "test", ["tool"], 1, False)["status"], "error")
        with patch("quality_gate.subprocess.run", side_effect=subprocess.TimeoutExpired("tool", 1)):
            self.assertEqual(check(self.root, "test", ["tool"], 1, False)["reason"], "timed out")

    @unittest.skipUnless(shutil.which("php"), "PHP CLI unavailable")
    def test_lint_reports_syntax_failure(self):
        self.write("broken.php", "<?php function ()")
        result = gate(self.root, self.options(only=["lint"]), load_config(self.root))
        self.assertEqual(result[0]["status"], "fail")
        self.assertEqual(result[0]["path"], "broken.php")
