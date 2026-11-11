---
name: php-engineer
description: "Coordinate PHP or Laravel changes by identifying the current development phase, selecting relevant specialists, and verifying the outcome."
---

# php-engineer

1. Read the request, repository instructions, working-tree state and closest relevant code. Use `python <this-skill>/scripts/inspect_project.py <project>` when Composer or tool inventory is needed. Reuse that inventory and establish the PHP syntax floor from project constraints, CI and deployment evidence.
2. Identify the current phase from the work in front of you. A reported failure can start in verification. A located, well-defined patch can start in implementation. Consult [phase routing](references/workflow.md) when the choice matters.
3. Select one current task category. If a shortlist helps, run `python <this-skill>/scripts/route_task.py <category> --framework <framework> --phase <phase>` with `--need` for each concrete additional decision and `--loaded` for instructions already in context. Read only relevant skill entry points and the references needed for the next decision. When shell access is unavailable, use the routing table directly.
4. Keep a short working record of the phase, supporting evidence, applied skills and next action. Revisit an earlier phase only when new evidence changes the work. Run focused checks with the project's existing commands or `quality_gate.py`. Review project-controlled tool and test configuration before using `--trusted`.
5. For a production change, open the matching playbook when relevant: [public API contract](references/public-api-change.md), [populated table during a rolling deploy](references/rolling-schema-change.md), or [slow tenant-scoped endpoint](references/slow-tenant-endpoint.md).
6. Report the outcome, skills that contributed and observed verification results using the [run summary format](references/workflow.md). Apply the project's reporting preferences.
