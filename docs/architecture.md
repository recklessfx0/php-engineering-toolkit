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

The router accepts explicit categories and emits ordered, deduplicated skill names. The current agent classifies the prompt and uses the shortlist to read relevant instructions. There is no subagent dispatch or Codex service dependency.

The runner lints PHP without loading php.ini. Tests, static analysis and formatting can load project code even in check modes. They require a trusted checkout. Composer audit additionally needs a lockfile and explicit network opt-in. Timeout applies per subprocess. The runner is a convenience layer and provides no isolation from processes launched by trusted tools. Compare pre-change and post-change diagnostics under the same settings to attribute regressions.

## Research and attribution

Skill discovery and portable packaging follow official OpenAI documentation. [Build skills](https://learn.chatgpt.com/docs/build-skills), [Package your plugin](https://developers.openai.com/plugins/build/plugins)

Jeffallan's MIT-licensed collection was reviewed as a reference for specialist skill organization and progressive disclosure. This toolkit's content and scripts were authored independently. [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills)
