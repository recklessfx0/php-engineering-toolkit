# Troubleshooting

- **Skill missing**. Check that the folder containing `SKILL.md` sits directly under `.agents/skills`, open the project in Codex and restart the client if needed.
- **Duplicate skill**. Check both scopes and any installed plugins for a second copy.
- **Python command unavailable**. Use the path to a Python 3.10+ interpreter, or try `python3` on Unix or `py -3` on Windows.
- **Unexpected PHP lint failure**. Compare `php -v` with the Composer platform and deployment runtime. The runner uses PHP CLI from PATH.
- **Skipped or unavailable tool**. Read the reason in the JSON result. Project checks require `--trusted` and local vendor entry points. On Windows, Composer batch wrappers are supported only when a sibling `composer.phar` is available.
- **PHPStan reports missing paths**. Add a project config for nonstandard source layouts or use the repository's existing analyzer command.
- **Insufficient diagnostics**. Run the applicable tool directly or rerun with `--diagnostics` after checking that the output can be kept private.
