# php-core workflow

PHP 8.0 introduced union types and constructor promotion. PHP 8.1 added enums, intersection types and readonly properties. PHP 8.2 added readonly classes and disjunctive normal form types. Use declared properties and check library compatibility before tightening types. A readonly property can still hold a mutable object. `strict_types` applies to calls from the declaring file and can change scalar coercion.

Check PSR-4 namespace and path casing on case-sensitive platforms. Follow the repository formatter and adopted PSRs. Prefer injecting collaborators at existing boundaries. Use interfaces where consumers need substitution or an explicit boundary. Handle expected exceptions where recovery is possible and preserve the previous exception when translating errors.
