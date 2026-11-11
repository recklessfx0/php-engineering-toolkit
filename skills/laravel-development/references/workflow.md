# laravel-development workflow

Validate input with existing Form Requests and serialize API responses through existing Resources. Scope Eloquent relationships and queries to authorized records. Add indexes and constraints with migration rollback and deployment compatibility in mind. Review transaction boundaries and dispatch work that depends on committed records after commit. Make retryable jobs idempotent and handle failure and backoff explicitly.

Follow existing Sanctum guard and token conventions and check policies independently of authentication. Scope cache keys by tenant or user where applicable and define invalidation on writes. Register events, listeners, scheduled tasks and notifications in the locations used by the installed Laravel version. Cover the route or job through existing framework tests using isolated services and database configuration.

## Rolling deploys, data and workers

Identify the database engine and version, table size, lock risk, and how long old app and worker versions can coexist. Introduce additive schema changes before deploying code that needs them. For a backfill, use stable batches and checkpoints, define how retries avoid duplicate effects, and account for writes during the transition. Verify the data invariant before enforcing constraints or removing old fields. State the recovery boundary after any irreversible transformation.

For jobs, inspect dispatch, transaction commit, retry, timeout, failed-job handling and external side effects. Use a durable idempotency key at the side-effect boundary when redelivery is possible. Verify duplicate delivery, partial failure and compatibility of queued payloads with both worker versions. Coordinate worker restart with the deployment where applicable.

For shared caches, confirm tenant scope, version compatibility, TTL and invalidation after committed writes. Verify the affected path with a cache hit and miss and with an independent tenant where relevant.
