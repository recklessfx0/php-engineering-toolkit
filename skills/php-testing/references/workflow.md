# php-testing workflow

Use a unit test for deterministic domain logic and a feature or integration test where routing, middleware, persistence or container wiring carries the risk. Use data providers or datasets for distinct equivalence classes. Mock external boundaries and preserve the behavior under test. Control time, ordering and generated identifiers where relevant.

For a bug, capture the observable regression and verify the test fails for the intended reason before applying the fix when practical. Use isolated test databases and test-specific credentials. Review incorrect assertions separately from production defects. Finish with the relevant adjacent suite and report what ran.
