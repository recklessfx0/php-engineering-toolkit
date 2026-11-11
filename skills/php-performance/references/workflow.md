# php-performance workflow

Look for repeated queries during iteration or Resource serialization. Eager-load only required relationships and columns, retaining join keys and authorization scopes. Compare query counts and review query plans against representative data before adding indexes. Consider write and migration costs. For batch work, measure memory while comparing chunking and streaming and check ordering and retry behavior.

Compare cold and warm cache separately. Document cache keys, isolation, invalidation and stampede behavior. Measure queue wait and execution times separately and review retries, job payloads and I/O concurrency. Record workload, sample size and baseline and changed metrics. Treat unmeasured improvements as hypotheses.

## Representative measurement

Record dataset size and distribution, concurrency, cache state, environment and sample count. Capture query counts and timings, request latency percentiles, peak memory or queue wait as applicable. Attribute the dominant cost using a profile or query trace before selecting a change. Inspect query plans in an appropriate environment and account for index write and storage cost.

Repeat the baseline workload with the change in place and separate cold from warm cache results. Check tenant scope, stable output and error behavior under the same workload. Record regressions in other resource dimensions and explain tradeoffs. If representative data or tooling is unavailable, label the proposed improvement a hypothesis.
