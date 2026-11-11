# php-testing workflow

Use a unit test for deterministic domain logic and a feature or integration test where routing, middleware, persistence or container wiring carries the risk. Use data providers or datasets for distinct equivalence classes. Mock external boundaries and preserve the behavior under test. Control time, ordering and generated identifiers where relevant.

For a bug, capture the observable regression and verify the test fails for the intended reason before applying the fix when practical. Use isolated test databases and test-specific credentials. Review incorrect assertions separately from production defects. Finish with the relevant adjacent suite and report what ran.

## Failure-driven coverage

Choose cases from the failure modes of the change. Test authorization with allowed and denied identities, rollback with an injected failure, and retries with repeated delivery when these invariants matter. Use the actual database engine for engine-specific locking or constraint semantics. Verify test credentials and external-service fakes before running integration tests.

For flaky tests, record seed, order, time, parallelism and environment. Reproduce with the smallest configuration that preserves the failure. Look for shared state, real time, asynchronous completion and test order dependencies. Fix the cause and repeat under the conditions that exposed it. Treat retries of the suite as diagnostic evidence.
