# php-refactoring workflow

Prefer a rename, extraction or consolidation that isolates a concrete responsibility. Preserve named arguments, array shapes, exception semantics, query scopes, transaction ordering, events and job dispatch. Use existing container and dependency injection conventions for Laravel services. Introduce an abstraction when callers share an invariant that would otherwise diverge. Verify between steps and keep unrelated style changes out of the diff.
