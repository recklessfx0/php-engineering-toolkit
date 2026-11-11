# Installation

Use Python 3.10+ for the helper scripts and PHP CLI for lint. Install optional tools through the target project's normal dependency workflow.

## Hosts with Agent Skills

The installer copies the same nine skill folders for each host. From the toolkit checkout, choose repository scope with `--repo /absolute/path/to/target` or personal scope with `--user`.

```sh
# Claude Code, repository scope
python scripts/install_skills.py --host claude --repo /absolute/path/to/target

# Claude Code, personal scope
python scripts/install_skills.py --host claude --user

# Codex, Gemini CLI, and supported GitHub Copilot surfaces
python scripts/install_skills.py --repo /absolute/path/to/target
```

| Host | Repository path | Personal path | How to start |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Run `/php-engineer` |
| Codex CLI and IDE extension | `.agents/skills/` | `~/.agents/skills/` | Select `$php-engineer` |
| Gemini CLI | `.agents/skills/` | `~/.agents/skills/` | Ask Gemini to use `php-engineer`; verify discovery with `/skills list` |
| GitHub Copilot | `.agents/skills/` | `~/.agents/skills/` | Ask Copilot to use `php-engineer` in a surface that supports Agent Skills |

The default `--host shared` and the `codex`, `gemini` and `copilot` aliases all install into the same location. Install the shared copy once per scope. For Claude Code and shared hosts on one project, run the installer once with `--host claude` and once with the default.

Start the host in the target project. For a team installation, commit the resulting skill directory in the target repository. Personal installations apply to local clients. Check the host's cloud setup instructions for remote environments. [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://learn.chatgpt.com/docs/build-skills), [Gemini CLI](https://geminicli.com/docs/cli/skills/), [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)

For manual installation on any host implementing [Agent Skills](https://agentskills.io/specification), copy the complete folders from `skills/` to that host's documented discovery path. Keep references and scripts with each skill. The installer checks for collisions before copying. To update, move your installed toolkit folders out of the discovery path after preserving local changes, then rerun the installer.

## Chat and API assistants

Export the workflows you need as a Markdown prompt.

```sh
python scripts/export_prompt.py php-engineer phpstan-analysis --output php-workflow.md
```

Paste the file into a chat, upload it if attachments are supported, or include its contents in an API instruction message. Replace the task placeholder with your request and relevant project context. For a production scenario, include the matching playbook from `skills/php-engineer/references/` with your prompt. Without repository or shell access, supply the relevant files or run checks locally and share redacted output.

## Plugin distribution

The root `plugin.json` packages the skills for Codex plugin distribution. For a local test, add the checkout to an existing marketplace root, point an entry to the plugin folder, and register the marketplace with `codex plugin marketplace add ./local-marketplace-root` if needed. Select the marketplace in the desktop Plugins Directory and install the toolkit. Claude Code uses the standalone installation above. [Official OpenAI packaging instructions](https://developers.openai.com/plugins/build/plugins)
