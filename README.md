# PHP Engineering Toolkit

Nine Agent Skills for implementing, reviewing and verifying changes in PHP projects with Claude Code, Codex, Gemini CLI, and GitHub Copilot. The toolkit includes a read-only Composer project inspector, a task router and a configurable quality gate. The Python helpers use the standard library.

## Install

From the toolkit checkout, run the command for your host with Python 3.10+.

```sh
# Claude Code
python scripts/install_skills.py --host claude --repo /path/to/php-project

# Codex, Gemini CLI, and supported Copilot surfaces
python scripts/install_skills.py --repo /path/to/php-project
```

Open the PHP project and ask the assistant to use `php-engineer`. Use `/php-engineer` in Claude Code or `$php-engineer` in Codex. Replace `--repo /path/to/php-project` with `--user` for personal installation.

For a chat or API assistant, export a Markdown prompt and include it with your task.

```sh
python scripts/export_prompt.py php-engineer api-development --output php-workflow.md
```

See [installation](docs/installation.md) for supported paths, updates and Codex plugin packaging.

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

For a trusted checkout with local tools installed and test services isolated, add `--trusted`. Composer advisory lookup also requires `--network`. Each check reports its own outcome. See [run reports](docs/reporting.md) for live terminal progress, Markdown and HTML summaries, and the Claude Code status line. See [configuration](docs/configuration.md) for the schema, exit codes and output options.

## Repository map

- `skills/` contains canonical skill folders, references and the coordinator's self-contained helpers and configuration.
- `scripts/` contains the installer, prompt exporter and repository validator.
- `tests/` contains deterministic tests and review fixtures. [Agent evaluations](docs/evaluations.md) are run separately.
- `examples/` contains plain PHP and Laravel inspection samples.
- `plugin.json` is the portable skills-only plugin manifest.
- `.github/` contains validation, execution safety and issue workflows.

See [architecture](docs/architecture.md), [troubleshooting](docs/troubleshooting.md) and the [release checklist](docs/releasing.md). The original repository content is available under the [MIT License](LICENSE).
