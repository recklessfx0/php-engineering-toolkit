"""Record local workflow events and runner observations for one engineering run."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import tempfile
from uuid import uuid4

from route_task import PHASES, ROUTES

SKILLS = {"php-engineer", "laravel-development"} | {
    skill for route in ROUTES.values() for skill in route
}
ASSISTANT_EVENTS = ("phase", "recommended", "applied", "reference", "decision", "handoff", "blocker")


def clean(value):
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", str(value))


def start(root):
    root.mkdir(parents=True, exist_ok=True)
    run = root / uuid4().hex
    run.mkdir()
    record(run, "assistant", "started", "Run opened")
    return run


def record(run, source, kind, subject, detail=None, *, check=None):
    if not run.is_dir():
        raise ValueError("run directory is missing; initialize a run first")
    now = datetime.now(timezone.utc)
    event = {
        "schema_version": 1,
        "timestamp": now.isoformat(),
        "source": source,
        "kind": kind,
        "subject": clean(subject),
    }
    if detail:
        event["detail"] = clean(detail)
    if check is not None:
        event["check"] = check
    name = now.strftime("%Y%m%dT%H%M%S%f") + "-" + uuid4().hex + ".event.json"
    # Publish only complete events. Independent writers never share a file.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=run, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            json.dump(event, handle, ensure_ascii=False)
            handle.close()
            temporary.replace(run / name)
        finally:
            temporary.unlink(missing_ok=True)


def events(run):
    if not run.is_dir():
        raise ValueError("run directory does not exist")
    result = []
    for path in sorted(run.glob("*.event.json")):
        with path.open(encoding="utf-8") as source:
            event = json.load(source)
        if event.get("schema_version") != 1:
            raise ValueError(f"unsupported event version in {path.name}")
        result.append(event)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("start")
    init.add_argument("directory", type=Path)
    add = commands.add_parser("add")
    add.add_argument("run", type=Path)
    add.add_argument("kind", choices=ASSISTANT_EVENTS)
    add.add_argument("subject")
    add.add_argument("--detail", required=True, help="short, redacted evidence or decision")
    show = commands.add_parser("show")
    show.add_argument("run", type=Path)
    try:
        args = parser.parse_args()
        if args.command == "start":
            print(start(args.directory).resolve())
        elif args.command == "show":
            print(json.dumps(events(args.run), indent=2))
        else:
            if not args.subject.strip() or not args.detail.strip():
                raise ValueError("subject and detail must be non-empty")
            if args.kind == "phase" and args.subject not in PHASES:
                raise ValueError("unknown phase")
            if args.kind in {"recommended", "applied"} and args.subject not in SKILLS:
                raise ValueError("unknown toolkit skill")
            record(args.run, "assistant", args.kind, args.subject, args.detail)
    except (OSError, ValueError, AttributeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
