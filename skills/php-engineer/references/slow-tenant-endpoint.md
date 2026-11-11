# Diagnose a slow tenant-scoped endpoint

Use when latency or resource use is reported on an endpoint that handles tenant data.

1. Identify route, tenant identity, data scope, request shape and performance target. Capture comparable workload conditions using synthetic or approved data. Record tenant size and distribution, concurrency, cache state, and environment.
2. Load `php-performance` to isolate the dominant cost. Read query counts and timings, request latency and memory as relevant. Compare requests for different tenant sizes and distinguish repeated database queries from slow queries, serialization and downstream I/O.
3. Use `laravel-development` if Eloquent loading or framework behavior needs interpretation. Use `security-audit` if tenant scope, authorization or cache key boundaries change. Preserve authorization before pagination and keep stable response order and shape.
4. Apply the smallest measured improvement. Verify behavior for allowed access, independent tenants and empty or boundary pages. Repeat the same workload before and after and report relevant tradeoffs such as index write cost, memory or cache invalidation.
5. Record measurements, environment, limitations, and a rollout signal such as query count or latency against a known baseline. Present unmeasured improvements as hypotheses.
