"""Validate the toolkit's canonical two-field skill format and package references."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/php-engineer/scripts"))
from route_task import ROUTES
from configuration import load_config

REQUIRED = {"php-engineer", "laravel-development"} | {
    name for names in ROUTES.values() for name in names
}
HEADER = re.compile(r'---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: (.+)\n---\n')


def validate(skills):
    issues = []
    names = set()
    for directory in sorted(skills.iterdir()):
        if not directory.is_dir() or directory.name.startswith("."):
            continue
        path = directory / "SKILL.md"
        try:
            source = path.read_text(encoding="utf-8")
            header = HEADER.match(source)
            if not header:
                raise ValueError("expected canonical name and quoted description")
            name, encoded = header.groups()
            description = json.loads(encoded)
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must be 1–1024 characters")
            if name in names:
                issues.append(f"{directory.name}: duplicate skill name {name}")
            names.add(name)
            if name != directory.name or len(name) > 64:
                issues.append(f"{directory.name}: name must match folder and fit in 64 characters")
            body = source[header.end():]
            if not body.strip():
                issues.append(f"{directory.name}: missing instructions")
            for reference in re.findall(r"\]\((references/[^)]+)\)", body):
                target = directory / reference
                if not target.resolve().is_relative_to(directory.resolve()) or not target.is_file():
                    issues.append(f"{directory.name}: missing or unsafe reference {reference}")
        except (OSError, ValueError) as error:
            issues.append(f"{directory.name}: {error}")
    issues.extend(f"missing required skill {name}" for name in sorted(REQUIRED - names))
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, default=ROOT / "skills")
    args = parser.parse_args()
    try:
        issues = validate(args.skills)
        load_config(ROOT)
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        if manifest["name"] != "php-engineering-toolkit" or not re.fullmatch(
            r"\d+\.\d+\.\d+", manifest["version"]
        ):
            issues.append("invalid plugin identity or version")
    except (OSError, ValueError, KeyError) as error:
        issues = [str(error)]
    for issue in issues:
        print(issue, file=sys.stderr)
    if not issues:
        print("Skill metadata, references, default configuration and plugin identity validated")
    return bool(issues)


if __name__ == "__main__":
    raise SystemExit(main())
