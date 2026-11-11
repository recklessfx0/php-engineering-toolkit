# php-engineer workflow

## Routing and verification

Use `core`, `framework`, `api`, `analysis`, `refactor`, `performance`, `testing`, or `security`. Combine categories only for distinct work. Laravel augments API, refactor and performance tasks. For analysis repairs add testing when runtime behavior or a public contract could regress. Narrow the API shortlist for contract-only changes.

For a useful baseline, run the same check selection, tool versions and configuration before and after. Compare diagnostics by check, path, identifier and message. Label failures pre-existing only with comparable evidence. Otherwise report that attribution is unknown. Use local diagnostics for comparisons and redact sensitive output before sharing.

With `auto_fix: safe`, fix narrowly scoped defects introduced by the change. With `off`, report remediation separately. Dependency installation requires authorization in `ask` mode and is disabled by `deny`. Destructive actions are outside this workflow. Observe repository and user instructions governing test databases and external calls. Reporting flags govern summary, detailed failures and recommendations. Always retain essential verification status.

## Run summary

Lead with the outcome and the most actionable failure or verification gap. List the skills whose instructions were applied, with one short contribution each. Keep recommendations separate. Include a compact verification table with status and evidence, followed by any outstanding action. Use status words alongside optional colored icons. Mention only measured timings and report baseline attribution only when comparable evidence is available.

For terminal progress, add `--progress` to the quality gate. When the user wants a saved report, add `--report-json <path>` and pass the task label, `--recommended <skill>`, and `--applied <skill>=<contribution>` as applicable. Repeat the skill flags as needed. Render the snapshot with `python <this-skill>/scripts/run_report.py <path> --format markdown` or select `html` or `status`. For a host without shell access, write the summary in the response using available evidence.
