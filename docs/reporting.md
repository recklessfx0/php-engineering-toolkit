# PHP Engineer run reports

The coordinator's end-of-run response works in any chat or CLI. It distinguishes skills recommended by the router, skills applied by the assistant, and checks observed by the runner. Applied-skill notes are supplied by the caller. The runner does not observe host tool calls, token usage or model costs.

## Live progress and saved reports

From a toolkit checkout, run:

```powershell
python skills/php-engineer/scripts/quality_gate.py . --only lint --progress --report-json .php-engineer-run.json --task "Verify PHP changes" --recommended php-core --applied "php-core=Reviewed target PHP syntax"
```

Use the actual PHP project path in place of `.` when running from another checkout. Supply `--trusted` only for reviewed project tooling. `--progress` sends status events to stderr and leaves the existing JSON result list on stdout. `--color auto` colors terminal output, honors `NO_COLOR`, and falls back to plain text when redirected. Choose `always` or `never` to override it.

The optional report path is replaced with each snapshot. Use a dedicated file and a separate path per concurrent run. Schema version 1 records task, project, elapsed verification time, available and reported skill usage, active check, and structured check outcomes. It omits raw stdout and stderr even with `--diagnostics`. Review task labels and notes before sharing. A failure's baseline starts as unknown. The assistant can add attribution to its response when it has comparable evidence.

```powershell
python skills/php-engineer/scripts/run_report.py .php-engineer-run.json
python skills/php-engineer/scripts/run_report.py .php-engineer-run.json --format html --output report.html
python skills/php-engineer/scripts/run_report.py .php-engineer-run.json --format status --color always
```

Markdown uses status icons with labels. HTML uses light and dark palettes and opens directly in a browser. The renderer creates new output files and reports an error if the destination already exists. `--next-step` on the quality gate adds a follow-up to both saved formats.

## Claude Code status line

In Claude Code's user settings, add or adapt the following setting. Use absolute paths to your trusted Python interpreter, the installed renderer, and the report snapshot. If you already use a status command, include the toolkit command in your existing script.

```json
{
  "statusLine": {
    "type": "command",
    "command": "python /absolute/path/to/run_report.py /absolute/path/to/.php-engineer-run.json --format status --color always"
  }
}
```

Create the snapshot before enabling the command. The status line displays the latest saved snapshot when Claude Code refreshes it. Use a different report path for each project or concurrent session. The status command reads the report file and needs no access to the host transcript. Other clients can render the same JSON through a host-specific adapter or show the Markdown in their normal response. [Claude Code status line documentation](https://code.claude.com/docs/en/statusline)

## Record a workflow across phases

Opt in to a local run history when decisions or handoffs need to be reviewable. In PowerShell:

```powershell
$run = python skills/php-engineer/scripts/run_log.py start .php-engineer-runs
python skills/php-engineer/scripts/run_log.py add $run phase implement --detail "The affected service and contract are known."
python skills/php-engineer/scripts/run_log.py add $run applied php-core --detail "Checked compatibility with the supported PHP version."
python skills/php-engineer/scripts/quality_gate.py . --only lint --run-log $run --report-json "$run/report.json"
python skills/php-engineer/scripts/run_report.py "$run/report.json" --run-log $run --format html --output "$run/report.html"
```

Use the actual PHP project path for verification. Record recommendations, applied skills, references, decisions, handoffs, and blockers only when they affect the next action. Assistant entries and runner observations carry separate source labels. The runner records structured check outcomes without raw output. Use short redacted notes and avoid including prompts, credentials, source excerpts, or customer data. `run_log.py show $run` prints the ordered events as JSON. The Markdown report includes the history and HTML puts it under an expandable section. Each run has a unique directory and independently written event files. Keep the run directory out of version control.
