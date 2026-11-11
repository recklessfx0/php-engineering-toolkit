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
