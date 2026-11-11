# php-core workflow

PHP 8.0 introduced union types and constructor promotion. PHP 8.1 added enums, intersection types and readonly properties. PHP 8.2 added readonly classes and disjunctive normal form types. Use declared properties and check library compatibility before tightening types. A readonly property can still hold a mutable object. `strict_types` applies to calls from the declaring file and can change scalar coercion.

Check PSR-4 namespace and path casing on case-sensitive platforms. Follow the repository formatter and adopted PSRs. Prefer injecting collaborators at existing boundaries. Use interfaces where consumers need substitution or an explicit boundary. Handle expected exceptions where recovery is possible and preserve the previous exception when translating errors.

## Release compatibility

Trace public methods to direct calls, named arguments, interface implementations, overrides and container registrations. Check return shape, nullability, exception types and error timing. For persisted or queued values, identify the readers and writers and verify that old values remain readable across deployments. Use a compatibility adapter where callers cannot switch together.

Compare Composer's PHP and extension requirements, platform overrides, lockfile and actual deploy images. For library changes, verify supported low and high dependency ranges with the existing matrix where available. For applications, verify the deployed locked set. A local lint run proves syntax only for the interpreter that ran it. Report any required runtime or dependency combinations that were unavailable.
