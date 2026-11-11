"""Run PHP quality checks in a trusted checkout and report structured outcomes."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

from configuration import load_config
from inspect_project import inspect

CHECKS = ("lint", "analysis", "tests", "format", "audit")
EXCLUDED = {".git", "vendor", "node_modules", "storage"}


def local_file(root, relative):
    path = root / relative
    return path.is_file() and path.resolve().is_relative_to(root)


def php_files(root):
    def walk_error(error):
        raise error

    for directory, folders, names in os.walk(root, onerror=walk_error):
        parent = Path(directory)
        folders[:] = sorted(
            name for name in folders if name not in EXCLUDED
            and not (parent / name).is_symlink()
            and not getattr(parent / name, "is_junction", lambda: False)()
            and (parent / name).resolve().is_relative_to(root)
        )
        for name in sorted(names):
            path = parent / name
            if path.suffix.lower() == ".php" and not path.is_symlink():
                yield str(path)


def check(root, name, command, timeout, diagnostics):
    try:
        process = subprocess.run(command, cwd=root, shell=False, stdin=subprocess.DEVNULL,
                                 capture_output=diagnostics, timeout=timeout,
                                 **({} if diagnostics else {
                                     "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}))
    except subprocess.TimeoutExpired:
        return {"check": name, "status": "error", "reason": "timed out"}
    except OSError:
        return {"check": name, "status": "error", "reason": "could not launch command"}
    result = {"check": name, "status": "pass" if process.returncode == 0 else "fail",
              "exit_code": process.returncode}
    if diagnostics:
        result.update(stdout=process.stdout[-16000:].decode(errors="replace"),
                      stderr=process.stderr[-16000:].decode(errors="replace"))
    return result


def gate(root, args, config):
    quality = config["quality"]
    php = shutil.which("php")
    project = inspect(root)
    requested = set(args.only or CHECKS)
    enabled = {
        "lint": True, "analysis": quality["run_static_analysis"], "tests": quality["run_tests"],
        "format": quality["check_formatting"], "audit": quality["security_review"] and args.network,
    }

    def vendor_tool(*names):
        return next((str(root / "vendor/bin" / name) for name in names
                     if local_file(root, "vendor/bin/" + name)), None)

    stan = vendor_tool("phpstan")
    tests = vendor_tool("pest", "phpunit")
    pint = vendor_tool("pint")
    fixer = vendor_tool("php-cs-fixer")
    composer = shutil.which("composer")
    if composer and Path(composer).suffix.lower() in {".bat", ".cmd"}:
        phar = Path(composer).with_name("composer.phar")
        composer_command = [php, str(phar)] if php and phar.is_file() else None
    else:
        composer_command = [composer] if composer else None

    def php_command(entry, *arguments):
        return [php, entry, *arguments] if php and entry else None

    stan_options = ["analyse", "--no-progress", "--no-interaction"]
    if not any(name.startswith("phpstan.") for name in project["configurations"]):
        stan_options.extend(["--level", str(quality["phpstan_level"]), *[
            str(root / name) for name in ("app", "src") if name in project["directories"]
        ]])
    commands = {
        "analysis": php_command(stan, *stan_options),
        "tests": php_command(tests),
        "format": php_command(pint, "--test") if pint else php_command(
            fixer, "fix", "--dry-run", "--diff", "--using-cache=no"),
        "audit": [*composer_command, "--no-plugins", "--no-scripts", "--no-interaction",
                  "audit", "--locked"] if composer_command and local_file(root, "composer.lock") else None,
    }
    results = []
    for name in CHECKS:
        reason = None
        status = "skipped"
        if name not in requested:
            reason = "excluded by --only"
        elif not enabled[name]:
            reason = "network requires --network" if name == "audit" and quality[
                "security_review"] else "disabled by configuration"
        elif name != "lint" and not args.trusted:
            reason = "requires --trusted after reviewing checkout and tool configuration"
        elif name == "lint" and php:
            count = 0
            failures = []
            for path in php_files(root):
                count += 1
                result = check(root, name, [php, "-n", "-l", path], args.timeout, args.diagnostics)
                if result["status"] != "pass":
                    result["path"] = str(Path(path).relative_to(root))
                    failures.append(result)
            if failures:
                results.extend(failures)
                continue
            if count:
                results.append({"check": name, "status": "pass", "files": count})
                continue
            reason = "no PHP files found"
        elif name != "lint" and commands[name]:
            results.append(check(root, name, commands[name], args.timeout, args.diagnostics))
            continue
        else:
            status = "unavailable"
            reason = "required executable, local tool, or lockfile missing"
        results.append({"check": name, "status": status, "reason": reason})

    if args.custom:
        if not args.trusted:
            results.append({"check": "custom", "status": "skipped", "reason": "requires --trusted"})
        else:
            executable = Path(args.custom[0])
            if not executable.is_absolute() or executable.suffix.lower() in {".bat", ".cmd", ".ps1"}:
                raise ValueError("Custom checks require an absolute executable path and an argument vector")
            results.append(check(root, "custom", args.custom, args.timeout, args.diagnostics))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--only", nargs="+", choices=CHECKS)
    parser.add_argument("--trusted", action="store_true")
    parser.add_argument("--network", action="store_true")
    parser.add_argument("--diagnostics", action="store_true", help="include raw tool output locally")
    parser.add_argument("--timeout", type=int, default=120, help="seconds per subprocess")
    parser.add_argument("--custom", nargs=argparse.REMAINDER, help="absolute executable and argv, last option")
    args = parser.parse_args()
    root = args.project.resolve()
    if args.custom == []:
        parser.error('--custom requires an executable')
    if not root.is_dir() or args.timeout < 1:
        parser.error("provide a project directory and a positive timeout")
    try:
        results = gate(root, args, load_config(root))
    except (OSError, ValueError, RecursionError) as error:
        parser.error(str(error))
    print(json.dumps(results, indent=2))
    return int(any(result["status"] in {"fail", "error"} for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
