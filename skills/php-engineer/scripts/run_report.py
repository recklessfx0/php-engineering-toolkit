"""Save and render portable PHP Engineer verification reports."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

from route_task import ROUTES

SKILLS = {"php-engineer", "laravel-development"} | {
    skill for route in ROUTES.values() for skill in route
}
STATUS = {
    "pass": ("Passed", "32", "🟢"),
    "fail": ("Failed", "31", "🔴"),
    "error": ("Error", "31", "🔴"),
    "unavailable": ("Unavailable", "33", "🟡"),
    "skipped": ("Skipped", "90", "⚪"),
    "running": ("Running", "34", "🔵"),
    "complete": ("Checks passed", "32", "🟢"),
    "partial": ("Verification incomplete", "33", "🟡"),
    "failed": ("Checks failed", "31", "🔴"),
}


def clean(value):
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", str(value))


def color_enabled(mode, stream):
    return mode == "always" or (
        mode == "auto" and stream.isatty() and "NO_COLOR" not in os.environ
        and os.environ.get("TERM") != "dumb"
    )


def label(status, color=False):
    name, code, _ = STATUS[status]
    return f"\033[{code}m{name}\033[0m" if color else name


def skill_notes(entries):
    result = {}
    for entry in entries:
        name, separator, note = entry.partition("=")
        if name not in SKILLS or not separator or not note.strip() or name in result:
            raise ValueError("--applied requires a unique toolkit skill and a note (skill=note)")
        result[name] = clean(note.strip())
    return [{"name": name, "note": note} for name, note in result.items()]


def save(path, report):
    # Replace the entire snapshot so readers can poll it while checks run.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False) as handle:
        temporary = Path(handle.name)
        try:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


class RunReport:
    def __init__(self, root, project, args):
        self.path = args.report_json
        self.progress = args.progress
        self.color = color_enabled(args.color, sys.stderr)
        self.started = time.monotonic()
        self.data = {
            "schema_version": 1,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "project": {"name": clean(root.name), "framework": project["framework"],
                        "php_constraint": project["php"]["constraint"]},
            "task": clean(args.task or "Project verification"),
            "skills": {"available": sorted(SKILLS), "recommended": list(dict.fromkeys(args.recommended)),
                       "applied": skill_notes(args.applied)},
            "status": "running",
            "active_check": None,
            "next_step": clean(args.next_step) if args.next_step else None,
            "elapsed_seconds": 0,
            "checks": [],
        }
        self.update()

    def update(self):
        self.data["elapsed_seconds"] = round(time.monotonic() - self.started, 3)
        if self.path:
            save(self.path, self.data)

    def begin(self, name):
        self.data["active_check"] = name
        self.update()
        if self.progress:
            print(f"PHP Engineer | {name} | {label('running', self.color)}",
                  file=sys.stderr, flush=True)

    def record(self, result):
        entry = {key: result[key] for key in ("check", "status", "exit_code", "files", "reason", "path")
                 if key in result}
        if entry["status"] in {"fail", "error"}:
            entry["baseline"] = "unknown"
        self.data["checks"].append(entry)
        self.data["active_check"] = None
        self.update()
        if self.progress and entry.get("reason") != "excluded by --only":
            print(f"PHP Engineer | {entry['check']} | {label(entry['status'], self.color)}",
                  file=sys.stderr, flush=True)

    def finish(self, interrupted=False):
        checks = self.data["checks"]
        self.data["active_check"] = None
        failed = interrupted or any(item["status"] in {"fail", "error"} for item in checks)
        pending = any(
            item["status"] == "unavailable" or (
                item["status"] == "skipped" and "requires --trusted" in item.get("reason", "")
            ) for item in checks
        )
        if failed:
            self.data["status"] = "failed"
        elif pending or not any(item["status"] == "pass" for item in checks):
            self.data["status"] = "partial"
        else:
            self.data["status"] = "complete"
        self.update()
        if self.progress:
            print(status_line(self.data, self.color), file=sys.stderr, flush=True)


def counts(report):
    return Counter(item["status"] for item in report["checks"])


def status_line(report, color=False):
    totals = counts(report)
    checks = " | ".join(f"{count} {label(status, color).lower()}"
                        for status, count in totals.items())
    active = report["active_check"]
    skills = report["skills"]
    parts = ["PHP Engineer", label(report["status"], color),
             f"{len(skills['applied'])}/{len(skills['available'])} skills applied"]
    if checks:
        parts.append(checks)
    if active:
        parts.append(f"{clean(active)} running")
    return " | ".join(parts)


def evidence(item):
    parts = [item[key] for key in ("path", "reason") if key in item]
    if "files" in item:
        parts.append(f"{item['files']} files checked")
    if "exit_code" in item:
        parts.append(f"Exit {item['exit_code']}")
    if "baseline" in item:
        parts.append(f"Baseline: {item['baseline']}")
    return " · ".join(map(clean, parts)) or "—"


def markdown_text(value):
    return re.sub(r"([\\`*_{}\[\]()#+.!|>])", r"\\\1", escape(clean(value), quote=False))


def render(report, format, color=False):
    if format == "status":
        return status_line(report, color) + "\n"
    skills = report["skills"]
    checks = sorted(report["checks"], key=lambda item: {
        "fail": 0, "error": 0, "unavailable": 1, "pass": 2, "skipped": 3
    }[item["status"]])
    project = report["project"]
    context = f"{project['name']} · {project['framework']} · {report['elapsed_seconds']}s"
    applied = skills["applied"]
    ratio = f"{len(applied)} of {len(skills['available'])}"
    recommended = ", ".join(skills["recommended"]) or "None recorded"
    available = ", ".join(skills["available"])
    status = report["status"]
    task = report["task"]
    next_step = report.get("next_step")
    if format == "markdown":
        md = markdown_text
        rows = ["# PHP Engineer", "", f"**{STATUS[status][2]} {label(status)}** · {md(task)}",
                "", md(context), "", f"## Skills applied ({ratio})", ""]
        rows.extend(f"- **{md(item['name'])}** · {md(item['note'])}" for item in applied)
        if not applied:
            rows.append("No applied skills recorded.")
        rows.extend(["", f"Recommended: {md(recommended)}", "", "## Verification", "",
                     "| Check | Status | Evidence |", "| --- | --- | --- |"])
        rows.extend(f"| {md(item['check'])} | {STATUS[item['status']][2]} {label(item['status'])}"
                    f" | {md(evidence(item))} |" for item in checks)
        if next_step:
            rows.extend(["", f"**Next step:** {md(next_step)}"])
        rows.extend(["", f"Available skills: {md(available)}"])
        return "\n".join(rows) + "\n"

    esc = lambda value: escape(clean(value))
    skill_html = "".join(f"<li><strong>{esc(item['name'])}</strong> · {esc(item['note'])}</li>"
                         for item in applied)
    table = "".join(
        f"<tr><th scope='row'>{esc(item['check'])}</th>"
        f"<td><span class='{item['status']}'>{label(item['status'])}</span></td>"
        f"<td>{esc(evidence(item))}</td></tr>" for item in checks
    )
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PHP Engineer run report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ max-width: 64rem; margin: auto; padding: 2rem 1rem; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: .65rem; border-bottom: 1px solid GrayText; }}
td span, .outcome {{ font-weight: 650; }}
.pass, .complete {{ color: #17633e; }}
.fail, .failed, .error {{ color: #a22430; }}
.unavailable, .partial {{ color: #805100; }}
.running {{ color: #195aa4; }}
.skipped {{ color: GrayText; }}
@media (prefers-color-scheme: dark) {{
  .pass, .complete {{ color: #85dbab; }}
  .fail, .failed, .error {{ color: #ff969f; }}
  .unavailable, .partial {{ color: #f9cb78; }}
  .running {{ color: #a2caff; }}
}}
</style>
<main>
<h1>PHP Engineer</h1>
<p><span class="outcome {status}">{label(status)}</span> · {esc(task)}</p>
<p>{esc(context)}</p>
<h2>Skills applied ({ratio})</h2>
{f"<ul>{skill_html}</ul>" if skill_html else "<p>No applied skills recorded.</p>"}
<p>Recommended: {esc(recommended)}</p>
<details><summary>Available skills</summary><p>{esc(available)}</p></details>
<h2>Verification</h2>
<table><thead><tr><th scope="col">Check</th><th scope="col">Status</th><th scope="col">Evidence</th></tr></thead>
<tbody>{table}</tbody></table>
{f"<p><strong>Next step:</strong> {esc(next_step)}</p>" if next_step else ""}
</main>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--format", choices=("markdown", "html", "status"), default="markdown")
    parser.add_argument("--output", type=Path, help="create a UTF-8 file instead of printing")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    args = parser.parse_args()
    try:
        with args.report.open(encoding="utf-8") as source:
            report = json.load(source)
        if report["schema_version"] != 1:
            raise ValueError("unsupported run report version")
        output = render(report, args.format, color_enabled(args.color, sys.stdout))
        if args.output:
            with args.output.open("x", encoding="utf-8") as destination:
                destination.write(output)
        else:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stdout.write(output)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
