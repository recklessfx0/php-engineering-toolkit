---
name: php-engineer
description: "Coordinate PHP or Laravel changes that span discovery, implementation, and verification, or require choosing among specialist workflows."
---

# php-engineer

1. Inspect the working tree, repository instructions, Composer metadata, and nearby patterns. Run `python <this-skill>/scripts/inspect_project.py <project>` for read-only inventory. Read the project's `.php-engineering-toolkit.json` when present and consult [workflow details](references/workflow.md).
2. Classify the requested change. Run `python <this-skill>/scripts/route_task.py <category> --framework <detected-framework>` when the shortlist is useful. Read only applicable sibling `SKILL.md` files from this bundle or use the Codex skill picker. Routing suggests instructions for the current agent.
3. Establish the PHP syntax floor from constraints, platform settings, CI and deploy images. Plan only as much as the change requires. Capture a relevant baseline when feasible.
4. Implement using existing architecture, then run scoped checks with `python <this-skill>/scripts/quality_gate.py <project>`. Review project-controlled test and tool configuration before using `--trusted`. Diagnose failures and rerun relevant checks after in-scope repairs.
5. Report changes, check outcomes and blockers, and material security or performance implications. Apply the reporting preferences from the project configuration.
