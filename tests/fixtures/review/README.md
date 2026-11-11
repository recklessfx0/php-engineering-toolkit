# Review fixtures

These isolated PHP snippets are inputs for agent evaluations. They have no registered routes, Composer bootstrap or database. The expected findings are a nullable return violating the declared type, missing record-level authorization, a relationship access that can trigger per-record queries and missing validation on a write path.
