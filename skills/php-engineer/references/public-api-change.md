# Change a public API contract

Use when a published request, response, permission, or error contract changes.

1. Identify the route and operation, OpenAPI definition, supported clients, and compatibility obligations. Capture one existing request/response and the access rules in tests or approved examples. Record unknown consumers as a rollout risk.
2. Load `api-development` for the contract decision. Compare required fields, nullability, enum handling, status and error envelopes, ordering, and retry semantics as applicable. Add `security-audit` when resource scope or authorization changes. Add `laravel-development` only for framework wiring that needs investigation.
3. Choose the smallest compatible change. For a breaking change, define how old and new clients coexist, how migration is measured, and when the old behavior can retire.
4. Verify representative old and new requests, failure responses and access decisions. For retryable writes or pagination changes, add cases for duplicate requests or stable traversal. Check OpenAPI against observed behavior.
5. Record affected consumers, rollout order, the owner of any migration step, and what would trigger a pause or rollback. Report test and schema evidence and remaining compatibility gaps.
