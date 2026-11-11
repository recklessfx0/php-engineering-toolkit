# security-audit workflow

Check policy and tenant scope across direct reads, nested route binding and bulk writes. Review SQL binding including dynamic identifiers, context-appropriate escaping, CSRF on session-authenticated writes, explicit mass-assignment fields and upload validation, storage and access controls. Trace unsafe deserialization, debug exposure, credentials and sensitive response fields without reproducing secret values.

Review token lifetimes and abilities, rate limits, session settings and exposed routes. Use lockfile advisory checks when authorized. Describe the role, data scope and application state required for a weakness in general terms. Verify protections with positive and negative authorization or validation assertions in isolated tests. Assess severity from reachability and impact and state unverified assumptions.
