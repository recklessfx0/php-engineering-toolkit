# Repository instructions

Use the canonical skill folders under `skills/`. Keep runtime helpers self-contained so copied skill folders work without the source checkout. Preserve read-only inspection, explicit trusted execution and network opt-in. Keep defensive review fixtures inert.

Run `python scripts/validate_skills.py` and `python -m unittest discover -s tests -v` after changes. Update corresponding evaluation scenarios when behavior guidance changes.
