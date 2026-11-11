# Agent behavior evaluations

Install the skills and start a fresh assistant session for each scenario. Open the toolkit checkout as the workspace. Use the host invocation in the installation guide or export the named skill and paste its text into a chat. Ask for review only unless the scenario explicitly asks to implement a change. Record the toolkit revision, client/model, selected skills, files read, checks attempted and pass or fail for each criterion. These manual evaluations are separate from deterministic tests.

| Prompt | Pass criteria |
| --- | --- |
| `$php-engineer Plan a REST API change in examples/laravel` | Detect Laravel and its PHP constraint, propose relevant skill shortlist, describe validation and verification, and recognize the sample has no installed runtime |
| `$phpstan-analysis Review tests/fixtures/review/analysis.php` | Identify the nullable return mismatch and discuss contract-preserving remediation without adding a baseline entry |
| `$security-audit Review displayOrder in tests/fixtures/review/laravel.php` | Identify missing record-level policy or scope, distinguish what can be inferred without routes, and propose defensive checks |
| `$php-performance Review authorNames in tests/fixtures/review/laravel.php` | Identify the potential repeated query and explain how to verify query counts before and after eager loading |
| `$api-development Review createOrder in tests/fixtures/review/laravel.php` | Identify missing quantity validation, propose a bounded integer rule and cover invalid input in tests |

Fail any scenario that fabricates a tool result or misrepresents a skipped check as passing.

For a coordinator run, verify that the summary distinguishes recommended from applied skills, shows the evidence for executed checks, and calls out unavailable checks or outstanding work.

## Phase and context evaluation

Run each scenario in a fresh session. Record the starting phase, evidence used, skill entry points and references opened, checks run, and any missed requirement. Compare with a run using the broad shortlist. Record token usage only if the host exposes it.

| Scenario | Expected routing |
| --- | --- |
| Existing PHPStan finding in a Laravel controller | Start in verification with PHPStan analysis. Add Laravel development only when framework behavior is relevant. |
| Narrow validation patch to an existing endpoint | Start in implementation with API development once the endpoint and contract are located. Add testing for new regression coverage. |
| Run existing checks on a finished refactor | Start in verification and run the checks. Load a specialist only when a diagnostic or review requires it. |
| New protected Laravel API contract | Start in design with API development. Add security review for the access boundary and Laravel development when framework wiring needs a decision. |

## Production workflow evaluation

Run with the updated toolkit and with the prior skill instructions using the same task, repository state, host and model. Score each required behavior as observed, missed or blocked. Record the actual files and references read and checks run. Capture token usage only when the host provides it. A routine controller patch is the control scenario and should skip these playbooks.

| Scenario | Required evidence and decisions |
| --- | --- |
| Add a new required field to a public API consumed by old clients | Identify the compatibility break, offer a compatible path or coexistence plan, verify old and new request behavior and authorization, and reconcile OpenAPI. |
| Replace a field in a populated Laravel table with old workers still active | Sequence an additive change, compatible app and worker behavior, resumable backfill, reconciliation, and cleanup after old workers drain. Identify the recovery boundary. |
| Diagnose a slow tenant endpoint whose serialization reads relationships | Capture a representative query and latency baseline, verify tenant isolation and response behavior, compare the same workload after the change, and label gaps in available evidence. |

For an opt-in run history, check that an assistant-recorded phase and skill decision appear alongside runner-observed results in the Markdown and HTML reports. Confirm diagnostics stay out of the history.
