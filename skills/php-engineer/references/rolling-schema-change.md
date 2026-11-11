# Migrate a populated table during a rolling deploy

Use when a schema or stored-data change can overlap old and new application instances or workers.

1. Identify the database engine and version, table shape, row count, active writers and supported worker versions. Determine what old and new processes must read and write during the deployment. Review engine-specific lock behavior and maintenance windows with the deployment owner.
2. Load `laravel-development` for migrations and workers. Add `php-testing` when compatibility or retry coverage must be created. Add `php-performance` when lock duration or backfill load requires measurement.
3. Expand the schema with compatible additions. Deploy compatible readers and writers in dependency order. Backfill in stable, bounded batches with a durable checkpoint and idempotent updates. Account for concurrent writes and record how to pause, resume, or rerun work safely.
4. Reconcile source and target data using counts and the application invariant. Validate constraints separately when the engine and change allow it. Confirm old application and worker versions have drained before removing any field, fallback or transitional write.
5. Verify old and new paths against representative data in an isolated environment. Test a partially completed batch and a retry. Describe rollback before and after irreversible steps, including where recovery requires a forward repair or a tested restore. Keep live execution subject to the project's deployment authorization.
