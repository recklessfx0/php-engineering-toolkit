# Configuration

Create `.php-engineering-toolkit.json` at the inspected project root. Nested settings merge with the [defaults](../skills/php-engineer/scripts/default.json). The loader validates the closed [schema](../skills/php-engineer/scripts/schema.json) locally. Unknown keys, duplicate keys and incorrect types are errors.

```json
{
  "framework": "auto",
  "php_version": "8.2",
  "quality": {
    "phpstan_level": 7,
    "run_tests": true,
    "run_static_analysis": true,
    "check_formatting": true,
    "security_review": true
  },
  "automation": {
    "auto_fix": "safe",
    "dependency_installation": "ask",
    "destructive_actions": "deny"
  },
  "reporting": {
    "include_summary": true,
    "include_failures": true,
    "include_recommendations": true
  }
}
```

Framework and PHP overrides affect inspection and agent decisions. They do not install or switch the local PHP interpreter. PHP lint validates against the PHP executable on PATH. PHPStan's configured project level takes precedence over the fallback level. The fallback analyzes conventional `app` and `src` paths. Supply project PHPStan configuration for other layouts. Pint takes precedence over PHP-CS-Fixer when both are installed.

The automation and reporting objects are coordinator instructions. The quality runner always emits its JSON results and never applies fixes, installs dependencies or launches migrations itself. Existing project tools and tests may have side effects. Review their configuration and isolate databases and external services before trusted runs.

```sh
python skills/php-engineer/scripts/quality_gate.py /path/to/project --only lint analysis --trusted
python skills/php-engineer/scripts/quality_gate.py /path/to/project --only audit --trusted --network
python skills/php-engineer/scripts/quality_gate.py /path/to/project --trusted --custom /absolute/path/to/executable argument
```

Custom commands are explicit argument vectors supplied by the caller and must appear last. The runner does not load commands from project JSON. `--diagnostics` includes raw tool output tails, which may contain sensitive data. Keep them local and redact before sharing.

Exit code 0 indicates no executed check failed and can include skipped or unavailable checks. Code 1 indicates a failed or errored check. Code 2 indicates invalid invocation or configuration. CI consumers requiring a specific gate should assert that its JSON status is `pass`.
