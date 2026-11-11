# Architecture

The coordinator reads project metadata and scope first, then selects the smallest useful set of skill instructions. Each skill has a short discovery description, an independent entry point and a local reference. All runtime files needed by the coordinator travel with that skill.

The project inspector reads Composer requirements, lockfile and installed package metadata. It uses framework package presence and conventional files as signals, reports versions by source where applicable and never boots the project. It does not resolve Composer constraints or determine the deployment runtime. Symfony detection is supported with framework-neutral PHP guidance.

| Category | Primary workflow | Supporting workflow |
| --- | --- | --- |
| core | PHP core | |
| framework | Laravel development for Laravel, PHP core otherwise | |
| api | API development | Laravel when detected, testing, security and analysis |
| analysis | PHPStan analysis | PHP core, with testing chosen by the agent if needed |
| refactor | PHP refactoring | Laravel when detected, testing |
| performance | PHP performance | Laravel when detected, testing if useful |
| testing | PHP testing | |
| security | Security audit | |

The table describes the broad shortlist returned without `--phase`. The coordinator prefers phase routing, which accepts one category and the current phase. It emits a reason and a `load` or `reuse` action for each recommendation. The assistant infers the phase from the request, working tree and relevant code or diagnostics. The router uses those explicit inputs and does not dispatch agents.

```sh
python skills/php-engineer/scripts/route_task.py api --framework laravel --phase implement --need security-boundary --loaded api-development
python skills/php-engineer/scripts/route_task.py api --framework laravel --phase verify
```

The first command reuses API development and suggests security review for the changed boundary. The second recommends no specialist for routine verification. If an analyzer reports a finding that needs investigation, rerun with `--need analysis-finding` or switch the current category to `analysis`.

The runner lints PHP without loading php.ini. Tests, static analysis and formatting can load project code even in check modes. They require a trusted checkout. Composer audit additionally needs a lockfile and explicit network opt-in. Timeout applies per subprocess. The runner is a convenience layer and provides no isolation from processes launched by trusted tools. Compare pre-change and post-change diagnostics under the same settings to attribute regressions.

## Research and attribution

The canonical workflows use the Agent Skills standard. The installer selects a host discovery path and the prompt exporter combines selected instructions with their references. The plugin manifest follows official OpenAI packaging documentation. [Build skills](https://learn.chatgpt.com/docs/build-skills), [Package your plugin](https://developers.openai.com/plugins/build/plugins)

Jeffallan's MIT-licensed collection was reviewed as a reference for specialist skill organization and progressive disclosure. This toolkit's content and scripts were authored independently. [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills)
