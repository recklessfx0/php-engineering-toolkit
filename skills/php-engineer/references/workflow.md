# php-engineer workflow

## Phase routing

| Phase | Evidence for entering | What to do next |
| --- | --- | --- |
| Discover | Relevant code, project constraints or requested outcome are unclear | Read the smallest useful slice. Use the coordinator alone. |
| Design | A contract, data model or compatibility decision is open | Resolve it with the primary skill and add a specialist for a concrete decision. |
| Implement | The change is defined and the relevant code is located | Patch the responsible layer. Load a specialist only when it will change the implementation. |
| Verify | A failure is reported or a change needs evidence | Run scoped checks. Load a specialist for diagnosis, new coverage or a specific review. |
| Report | The requested work and available verification are accounted for | Summarize outcomes and gaps. Use the coordinator alone. |

Choose one category for the current work from `core`, `framework`, `api`, `analysis`, `refactor`, `performance`, `testing` and `security`. These select the corresponding specialists. The framework category uses Laravel development for Laravel and PHP core elsewhere. In verification, an analysis, testing, performance or security task can still select its primary skill. Routine lint, test and analyzer execution needs no additional skill.

Use `--need framework-wiring` for Laravel-specific behavior, `php-compatibility` for a language or runtime constraint, `api-contract` for a contract decision, `regression-coverage` for writing or diagnosing tests, `analysis-finding` for interpreting an analyzer finding, `security-boundary` for access control or another trust boundary, and `performance-evidence` for measuring or interpreting a bottleneck. Identify the evidence before passing a need. A tool being installed is insufficient evidence.

Keep the working record in the conversation. Record the phase, relevant paths or finding identifiers, skills already read and the next decision. Reinspect Composer metadata only if relevant inputs change. Use `reuse` recommendations from the router without reopening the same files when their contents are still available. Read a reference when it answers an open question. When a check fails, start with its diagnostic and nearby code. Expand only if necessary.

For a useful baseline, run the same check selection, tool versions and configuration before and after. Compare diagnostics by check, path, identifier and message. Label failures pre-existing only with comparable evidence. Otherwise report that attribution is unknown. Use local diagnostics for comparisons and redact sensitive output before sharing.

With `auto_fix: safe`, fix narrowly scoped defects introduced by the change. With `off`, report remediation separately. Dependency installation requires authorization in `ask` mode and is disabled by `deny`. Destructive actions are outside this workflow. Observe repository and user instructions governing test databases and external calls. Reporting flags govern summary, detailed failures and recommendations. Always retain essential verification status.

## Production playbooks

For routine fixes, verify the affected behavior and relevant surrounding checks. For changes involving persisted data, worker payloads, public contracts or privileged actions, identify the consumers or actors, compatibility window, verification evidence and recovery boundary. Record missing information as a gap.

## Run summary

Lead with the outcome and the most actionable failure or verification gap. List the skills whose instructions were applied, with one short contribution each. Keep recommendations separate. Include a compact verification table with status and evidence, followed by any outstanding action. Use status words alongside optional colored icons. Mention only measured timings and report baseline attribution only when comparable evidence is available.

For terminal progress, add `--progress` to the quality gate. When the user wants a saved report, add `--report-json <path>` and pass the task label, `--recommended <skill>`, and `--applied <skill>=<contribution>` as applicable. Repeat the skill flags as needed. Render the snapshot with `python <this-skill>/scripts/run_report.py <path> --format markdown` or select `html` or `status`. For a host without shell access, write the summary in the response using available evidence.

When a user requests a run history, initialize it with `run_log.py start <local-directory>` and reuse the printed run directory across phases. Record significant changes with `run_log.py add <run> <kind> <subject> --detail <redacted-note>`. For a handoff, note what was established and the next decision or evidence needed. Pass `--run-log <run> --report-json <run>/report.json` to the quality gate and `--run-log <run>` to the report renderer. Record observed checks through the runner. Keep the working record in the conversation for routine changes.
