# api-development workflow

Start from resource and operation semantics. Validate input with Form Requests in Laravel or the existing validator elsewhere. Allowlist filters and sort keys, bound page sizes and use stable ordering. Apply authorization to the record set before pagination or serialization. Use existing API Resources or serializers and distinguish absent fields from nullable fields.

Preserve existing versioning strategy and assess consumer impact before introducing a new version. Update OpenAPI for the actual request, security scheme, response and errors. Cover success, invalid input, unauthenticated access, forbidden access and pagination boundaries with feature or integration tests.

## Consumer compatibility and retries

Compare request and response schemas, requiredness, nullability, error envelopes, status codes, enum expansion, pagination ordering and supported media types. Verify existing clients can still deserialize and act on responses. Check OpenAPI against the route and representative request/response tests. For an incompatible change, document the migration path, coexistence and retirement criteria.

For retryable writes, use the project's established idempotency semantics. Scope keys to the caller and operation, handle repeated keys with differing payloads consistently, and verify duplicate and concurrent requests where they matter. For pagination, verify stable tie-breaking, page bounds and authorization before pagination, including cursor behavior where applicable.
