# php-engineer workflow

## Routing and verification

Use `core`, `framework`, `api`, `analysis`, `refactor`, `performance`, `testing`, or `security`. Combine categories only for distinct work. Laravel augments API, refactor and performance tasks. For analysis repairs add testing when runtime behavior or a public contract could regress. Narrow the API shortlist for contract-only changes.

For a useful baseline, run the same check selection, tool versions and configuration before and after. Compare diagnostics by check, path, identifier and message. Label failures pre-existing only with comparable evidence. Otherwise report that attribution is unknown. Use local diagnostics for comparisons and redact sensitive output before sharing.

With `auto_fix: safe`, fix narrowly scoped defects introduced by the change. With `off`, report remediation separately. Dependency installation requires authorization in `ask` mode and is disabled by `deny`. Destructive actions are outside this workflow. Observe repository and user instructions governing test databases and external calls. Reporting flags govern summary, detailed failures and recommendations. Always retain essential verification status.
