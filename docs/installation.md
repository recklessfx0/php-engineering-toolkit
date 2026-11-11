# Installation

Use Python 3.10+ for the helper scripts and PHP CLI for lint. Optional tools should already be installed by the target project's normal dependency workflow.

## Codex CLI and IDE extension

Run one installer command from your toolkit checkout.

```sh
python scripts/install_skills.py --repo /absolute/path/to/target
python scripts/install_skills.py --user
```

For a manual installation, copy each complete skill directory from `skills/` into the target checkout's `.agents/skills/` or your home directory's `.agents/skills/`. Copy the entire folder, including references and scripts. In the CLI or IDE extension, open the target project and use the skill picker or type `$php-engineer`. Restart Codex if the skill fails to appear. For teams, commit the repository-scoped copy in the target repository.

The installer checks for collisions before copying. To update, move the installed toolkit skill directories out of the discovery path after preserving local changes, then rerun the installer. To uninstall, remove the installed toolkit directories you own. If a different skill uses the same name, use one installation scope or choose the intended copy in the picker. [Official skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills)

## Plugin distribution

The checkout is a portable plugin package. The root manifest declares its identity and the host discovers the canonical `skills/` directory. To test in a local marketplace, add the checkout as a plugin folder in an existing marketplace root and point its entry to that folder with a relative `./` path. Register the marketplace with `codex plugin marketplace add ./local-marketplace-root` if needed, then select it in the desktop Plugins Directory and install the toolkit. Use the standalone skill installation for IDE use. [Official marketplace and packaging instructions](https://developers.openai.com/plugins/build/plugins)
