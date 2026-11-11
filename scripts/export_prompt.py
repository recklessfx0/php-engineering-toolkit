"""Render selected PHP engineering instructions for an assistant without skill discovery."""
import argparse
from pathlib import Path
import sys

from validate_skills import HEADER, REQUIRED, ROOT


def render(skills):
    sections = [
        "# PHP Engineering Toolkit",
        "Use the workflows below for the task and project context I provide. "
        "If you lack repository or shell access, ask for the relevant files or "
        "command output and give me the steps to run locally. Report which checks "
        "were actually run and which remain pending. Redact secrets from shared evidence.",
    ]
    for name in dict.fromkeys(skills):
        if name not in REQUIRED:
            raise ValueError(f"Unknown toolkit skill: {name}")
        directory = ROOT / "skills" / name
        source = (directory / "SKILL.md").read_text(encoding="utf-8")
        header = HEADER.match(source)
        if not header:
            raise ValueError(f"Invalid skill metadata: {name}")
        body = source[header.end():].strip()
        reference = (directory / "references/workflow.md").read_text(encoding="utf-8").strip()
        sections.extend((body.replace("](references/workflow.md)", "]"), reference))
    sections.append("## Task and project context\n\n[Add your request and relevant code or diagnostics here.]")
    return "\n\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="+", choices=sorted(REQUIRED))
    parser.add_argument("--output", type=Path, help="create a Markdown file instead of printing")
    args = parser.parse_args()
    try:
        prompt = render(args.skills)
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as output:
                output.write(prompt)
        else:
            sys.stdout.write(prompt)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
