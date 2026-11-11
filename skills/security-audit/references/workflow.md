# security-audit workflow

Check policy and tenant scope across direct reads, nested route binding and bulk writes. Review SQL binding including dynamic identifiers, context-appropriate escaping, CSRF on session-authenticated writes, explicit mass-assignment fields and upload validation, storage and access controls. Trace unsafe deserialization, debug exposure, credentials and sensitive response fields without reproducing secret values.

Review token lifetimes and abilities, rate limits, session settings and exposed routes. Use lockfile advisory checks when authorized. Describe the role, data scope and application state required for a weakness in general terms. Verify protections with positive and negative authorization or validation assertions in isolated tests. Assess severity from reachability and impact and state unverified assumptions.

## Tenant and privileged operations

Map the identities and tenant context across HTTP requests, queued jobs, batch operations, scheduled commands and exports. Confirm that every sensitive read or write carries the right scope and authorization through storage, caches and downstream work. Review privileged overrides for explicit authorization and auditability. Trace sensitive fields to responses, logs, files and error handlers. Keep credentials and real customer data out of evidence.

Verify expected access and denied access with synthetic users and independent tenant records. For async work, verify scope persists across dispatch and execution, and inspect how permissions are handled when access changes. Record the reviewed paths and gaps. Use defensive test assertions and report preconditions at the level needed to explain impact and remediation.
