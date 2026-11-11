# api-development workflow

Start from resource and operation semantics. Validate input with Form Requests in Laravel or the existing validator elsewhere. Allowlist filters and sort keys, bound page sizes and use stable ordering. Apply authorization to the record set before pagination or serialization. Use existing API Resources or serializers and distinguish absent fields from nullable fields.

Preserve existing versioning strategy and assess consumer impact before introducing a new version. Update OpenAPI for the actual request, security scheme, response and errors. Cover success, invalid input, unauthenticated access, forbidden access and pagination boundaries with feature or integration tests.
