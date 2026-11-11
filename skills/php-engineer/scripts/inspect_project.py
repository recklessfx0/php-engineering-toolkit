"""Inspect Composer metadata and conventional paths without running project code."""
import argparse
import json
from pathlib import Path

from configuration import load_config, read_json

TOOLS = {
    "pest": "pestphp/pest", "phpunit": "phpunit/phpunit",
    "phpstan": "phpstan/phpstan", "larastan": "larastan/larastan",
    "pint": "laravel/pint", "php-cs-fixer": "friendsofphp/php-cs-fixer",
}
CONFIGS = (
    "composer.json", "composer.lock", "phpunit.xml", "phpunit.xml.dist",
    "phpstan.neon", "phpstan.neon.dist", "phpstan.dist.neon", "pint.json",
    ".php-cs-fixer.php", ".php-cs-fixer.dist.php", ".php-engineering-toolkit.json",
)
DIRECTORIES = ("app", "src", "routes", "config", "database", "tests", "public", "bootstrap")


def inspect(root):
    warnings = []

    def metadata(name):
        path = root / name
        try:
            if path.is_symlink():
                raise ValueError("symbolic link skipped")
            return read_json(path) if path.exists() else {}
        except (OSError, ValueError, RecursionError):
            warnings.append(f"{name} could not be read as local JSON")
            return {}

    composer = metadata("composer.json")
    lock = metadata("composer.lock")
    requirements = {}
    for section in ("require", "require-dev"):
        values = composer.get(section, {})
        if isinstance(values, dict):
            requirements.update({key: value for key, value in values.items() if isinstance(value, str)})
        else:
            warnings.append(f"composer.json {section} must be an object")

    def versions(document, sections):
        result = {}
        for section in sections:
            packages = document.get(section, [])
            if isinstance(packages, list):
                for package in packages:
                    if isinstance(package, dict):
                        name, version = package.get("name"), package.get("version")
                        if isinstance(name, str) and isinstance(version, str):
                            result[name] = version
        return result

    locked = versions(lock, ("packages", "packages-dev"))
    installed = {}
    vendor_metadata = root / "vendor/composer/installed.json"
    try:
        if vendor_metadata.is_file() and vendor_metadata.resolve().is_relative_to(root):
            data = json.loads(vendor_metadata.read_text(encoding="utf-8-sig"))
            if isinstance(data, list):
                data = {"packages": data}
            if isinstance(data, dict):
                installed = versions(data, ("packages",))
    except (OSError, ValueError, RecursionError):
        warnings.append("Composer installed package metadata could not be read")
    packages = requirements.keys() | locked.keys() | installed.keys()
    framework = "plain-php"
    if "laravel/framework" in packages or (root / "artisan").is_file():
        framework = "laravel"
    elif "symfony/framework-bundle" in packages:
        framework = "symfony"
    elif not composer and not any(root.glob("*.php")) and not (root / "src").is_dir():
        framework = "unknown"

    config = load_config(root)
    framework_override = config["framework"]
    platform = composer.get("config")
    platform = platform.get("platform") if isinstance(platform, dict) else None
    return {
        "framework": framework if framework_override == "auto" else framework_override,
        "detected_framework": framework,
        "framework_versions": {
            name: installed.get(name) or locked.get(name) or requirements.get(name)
            for name in ("laravel/framework", "symfony/framework-bundle") if name in packages
        },
        "php": {
            "constraint": requirements.get("php"),
            "composer_platform": platform.get("php") if isinstance(platform, dict) else None,
            "target_override": None if config["php_version"] == "auto" else config["php_version"],
        },
        "dependencies": requirements,
        "tools": {
            tool: {"required": requirements.get(package), "locked": locked.get(package),
                   "installed": installed.get(package),
                   "entrypoint": (root / f"vendor/bin/{tool}").is_file()}
            for tool, package in TOOLS.items()
        },
        "configurations": [name for name in CONFIGS if (root / name).is_file()],
        "directories": [name for name in DIRECTORIES if (root / name).is_dir()],
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    root = parser.parse_args().project.resolve()
    if not root.is_dir():
        parser.error("project must be a directory")
    try:
        print(json.dumps(inspect(root), indent=2))
    except (OSError, ValueError, RecursionError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
