# php-refactoring workflow

Prefer a rename, extraction or consolidation that isolates a concrete responsibility. Preserve named arguments, array shapes, exception semantics, query scopes, transaction ordering, events and job dispatch. Use existing container and dependency injection conventions for Laravel services. Introduce an abstraction when callers share an invariant that would otherwise diverge. Verify between steps and keep unrelated style changes out of the diff.

## Incremental structural changes

Inventory external callers, configuration keys, serialized payloads, side-effect ordering and failure behavior. Capture representative outcomes and ordering with existing tests or narrowly targeted characterization. Separate structural steps so each can be reviewed and verified. Keep intentional behavior changes explicit.

When callers migrate independently, keep the old entry point delegating through a compatibility shim. Preserve input, output and exceptions across both paths. Identify adoption evidence and the condition for removing the shim. Recheck side effects and public contracts after each risky extraction or boundary move.
