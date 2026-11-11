# Skill development

Put a new skill in `skills/<name>/SKILL.md`. Use a lowercase kebab-case name matching the folder and a single-line, double-quoted description. This repository's validator checks a canonical subset of YAML frontmatter. Keep entry-point instructions independent and link to deeper guidance under `references/`.

Put reusable deterministic helpers in the skill's `scripts/` directory. Prefer standard-library tools, explicit arguments and JSON for automation. Keep paths relative to the skill's own location. Add a routing category or rule only when the coordinator should select the skill. Add a deterministic test for automation changes and an evaluation scenario for behavioral changes. Run the validator and tests before review.
