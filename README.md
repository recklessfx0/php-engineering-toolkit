# PHP Engineering Toolkit for Codex

Nine skills for implementing, reviewing and verifying changes in PHP projects. The toolkit includes a read-only Composer project inspector, a task router and a configurable quality gate. The Python helpers use the standard library.

## Install

From a checkout of this toolkit, run either command with Python 3.10 or newer.

```sh
python scripts/install_skills.py --repo /path/to/php-project
python scripts/install_skills.py --user
```

Open the PHP project in Codex CLI or the Codex IDE extension and select `$php-engineer`. Repository scope installs into the target project's `.agents/skills`. User scope installs into your home directory's `.agents/skills`. See [installation](docs/installation.md) for updates and plugin packaging.

## Skills

| Skill | When to use it |
| --- | --- |
| `php-engineer` | Discover project conventions and coordinate changes across specialist workflows |
| `php-core` | Implement target-compatible PHP and Composer changes |
| `laravel-development` | Work on framework features, persistence, queues and application tests |
| `phpstan-analysis` | Diagnose PHPStan and Larastan findings |
| `security-audit` | Review trust boundaries and recommend defensive fixes |
| `api-development` | Change REST endpoints while preserving established contracts |
| `php-testing` | Write or diagnose PHPUnit and Pest coverage |
| `php-refactoring` | Restructure code while preserving behavior |
| `php-performance` | Measure and diagnose latency, queries, memory and I/O |

Try `$php-engineer Add pagination to the orders endpoint and verify access control and contract compatibility`, or invoke `$phpstan-analysis` directly for a focused diagnostic task.

## Run the helpers

From the toolkit checkout:

```sh
python skills/php-engineer/scripts/inspect_project.py examples/laravel
python skills/php-engineer/scripts/route_task.py api --framework laravel
python skills/php-engineer/scripts/quality_gate.py examples/plain-php --only lint
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

For a trusted checkout with local tools installed and test services isolated, add `--trusted`. Composer advisory lookup also requires `--network`. Each check reports its own outcome. See [configuration](docs/configuration.md) for the schema, exit codes and output options.

## Repository map

- `skills/` contains canonical skill folders, references and the coordinator's self-contained helpers and configuration.
- `scripts/` contains the installer and repository validator.
- `tests/` contains deterministic tests and review fixtures. [Agent evaluations](docs/evaluations.md) are run separately.
- `examples/` contains plain PHP and Laravel inspection samples.
- `plugin.json` is the portable skills-only plugin manifest.
- `.github/` contains validation, execution safety and issue workflows.

See [architecture](docs/architecture.md), [troubleshooting](docs/troubleshooting.md) and the [release checklist](docs/releasing.md). The original repository content is available under the [MIT License](LICENSE).
