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
from route_task import route, route_phase
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


    def test_phase_routes_coordinator_only_without_specialist_work(self):
        for phase in ("discover", "verify", "report"):
            with self.subTest(phase=phase):
                self.assertEqual(route_phase("api", "laravel", phase)["skills"], [])
        self.assertEqual(route_phase("refactor", "laravel", "verify")["skills"], [])

    def test_phase_routes_only_evidence_and_reuses_loaded_skill(self):
        result = route_phase("api", "laravel", "implement",
                             ["api-contract", "security-boundary", "security-boundary"],
                             ["api-development"])
        self.assertEqual(
            [(item["name"], item["action"]) for item in result["skills"]],
            [("api-development", "reuse"), ("security-audit", "load")],
        )
        self.assertTrue(all(item["reason"] for item in result["skills"]))

    def test_phase_diagnoses_failures_and_defers_inapplicable_needs(self):
        result = route_phase("analysis", "laravel", "verify",
                             ["framework-wiring", "analysis-finding", "php-compatibility"])
        self.assertEqual([item["name"] for item in result["skills"]],
                         ["phpstan-analysis", "laravel-development"])
        self.assertEqual(result["deferred_needs"], ["php-compatibility"])
        symfony = route_phase("framework", "symfony", "implement", ["framework-wiring"])
        self.assertEqual([item["name"] for item in symfony["skills"]], ["php-core"])
        self.assertEqual(symfony["deferred_needs"], ["framework-wiring"])

    def test_phase_cli_keeps_legacy_output_and_rejects_multiple_categories(self):
        command = [sys.executable, str(SCRIPTS / "route_task.py")]
        legacy = subprocess.run(command + ["analysis"], check=True, capture_output=True)
        self.assertEqual(json.loads(legacy.stdout), ["phpstan-analysis", "php-core"])
        phase = subprocess.run(command + ["api", "--phase", "verify", "--need", "analysis-finding"],
                               check=True, capture_output=True)
        self.assertEqual(json.loads(phase.stdout)["skills"][0]["name"], "phpstan-analysis")
        invalid = subprocess.run(command + ["api", "core", "--phase", "design"],
                                 capture_output=True)
        self.assertEqual(invalid.returncode, 2)


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

class RunReportTests(TemporaryProjectTest):
    @unittest.skipUnless(shutil.which("php"), "PHP CLI unavailable")
    def test_report_cli_streams_and_saves_failed_check(self):
        self.write("broken.php", "<?php function ()")
        snapshot = self.root / "report.json"
        process = subprocess.run(
            [sys.executable, str(SCRIPTS / "quality_gate.py"), str(self.root),
             "--only", "lint", "--progress", "--color", "always", "--diagnostics",
             "--report-json", str(snapshot), "--task", "<script>sample</script>",
             "--recommended", "phpstan-analysis", "--applied", "php-core=Checked syntax",
             "--next-step", "Fix the declaration"],
            capture_output=True,
        )
        self.assertEqual(process.returncode, 1)
        self.assertIn(b"\x1b[34mRunning", process.stderr)
        self.assertIn(b"\x1b[31mFailed", process.stderr)
        self.assertIn("stderr", json.loads(process.stdout)[0])
        report = json.loads(snapshot.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "failed")
        self.assertIsNone(report["active_check"])
        self.assertEqual(report["checks"][0]["baseline"], "unknown")
        self.assertNotIn("stderr", report["checks"][0])
        self.assertEqual(report["skills"]["recommended"], ["phpstan-analysis"])
        self.assertEqual(report["skills"]["applied"][0]["name"], "php-core")

        def render_as(format):
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "run_report.py"), str(snapshot),
                 "--format", format, "--color", "never"],
                check=True, capture_output=True,
            )
            return result.stdout.decode("utf-8")

        html = render_as("html")
        self.assertIn("&lt;script&gt;sample&lt;/script&gt;", html)
        self.assertNotIn("<script>", html)
        self.assertIn("Fix the declaration", render_as("markdown"))
        self.assertIn("1/9 skills applied", render_as("status"))
        self.assertNotIn("\x1b", render_as("status"))

    def test_progress_snapshot_is_readable_during_a_check(self):
        from run_report import RunReport, color_enabled
        from io import StringIO

        snapshot = self.root / "report.json"
        options = argparse.Namespace(report_json=snapshot, progress=False, color="auto",
                                     task=None, recommended=[], applied=[], next_step=None)
        report = RunReport(self.root, inspect(self.root), options)
        report.begin("lint")
        self.assertEqual(json.loads(snapshot.read_text(encoding="utf-8"))["active_check"], "lint")
        report.record({"check": "lint", "status": "pass", "files": 1})
        report.finish()
        self.assertEqual(json.loads(snapshot.read_text(encoding="utf-8"))["status"], "complete")
        self.assertFalse(color_enabled("auto", StringIO()))
