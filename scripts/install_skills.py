"""Copy self-contained skill folders into an explicit .agents/skills destination."""
import argparse
from pathlib import Path
import shutil

from validate_skills import ROOT, validate


def install(destination):
    source = ROOT / "skills"
    issues = validate(source)
    if issues:
        raise ValueError("\n".join(issues))
    skills = sorted(path for path in source.iterdir() if (path / "SKILL.md").is_file())
    conflicts = [skill.name for skill in skills if (destination / skill.name).exists()
                 or (destination / skill.name).is_symlink()]
    if conflicts:
        raise ValueError("Existing destinations: " + ", ".join(conflicts))
    destination.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        shutil.copytree(skill, destination / skill.name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return [skill.name for skill in skills]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--user", action="store_true")
    scope.add_argument("--repo", type=Path)
    args = parser.parse_args()
    root = Path.home() if args.user else args.repo.resolve()
    if not root.is_dir():
        parser.error("target directory must exist")
    destination = root / ".agents/skills"
    try:
        names = install(destination)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Copied {len(names)} skills to {destination}")


if __name__ == "__main__":
    main()
