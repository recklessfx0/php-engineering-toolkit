# php-performance workflow

Look for repeated queries during iteration or Resource serialization. Eager-load only required relationships and columns, retaining join keys and authorization scopes. Compare query counts and review query plans against representative data before adding indexes. Consider write and migration costs. For batch work, measure memory while comparing chunking and streaming and check ordering and retry behavior.

Compare cold and warm cache separately. Document cache keys, isolation, invalidation and stampede behavior. Measure queue wait and execution times separately and review retries, job payloads and I/O concurrency. Record workload, sample size and baseline and changed metrics. Treat unmeasured improvements as hypotheses.
