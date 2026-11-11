# phpstan-analysis workflow

When PHPStan is missing, identify compatible PHPStan and Larastan ranges from their published Composer constraints and the app's Laravel and PHP versions. Propose installation before changing dependencies. Respect configured level and PHP version. For projects without configuration use an explicit level and source paths.

Group findings by identifier and shared cause. Fix incorrect narrowing or inaccurate return types at their source. Describe Eloquent models, collections and builders with generics matching actual runtime values. Use array shapes for stable keyed structures. Avoid casts and inline annotations that merely silence evidence. Keep existing baseline entries stable unless verified obsolete. Record justification and exact scope for any approved ignore.

## Baseline integrity

Capture before and after with the same PHPStan and Larastan versions, PHP target, config, scan paths and bootstrap. Use machine-readable output when available. Group findings by identifier and causal code path. Compare path, identifier and message while allowing for line shifts. Run a targeted diagnosis first and the normal CI scope before calling it resolved when available.

Check the baseline diff for new ignores, broadened patterns and increased expected counts. Remove obsolete entries only after verifying the findings are gone. Keep a level increase or analyzer upgrade separately identifiable so a change in rules does not obscure new findings. Report scope and versions alongside any claim that a finding is pre-existing.
