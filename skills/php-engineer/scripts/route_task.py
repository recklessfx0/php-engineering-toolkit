"""Select skills for the current development phase or print a task shortlist."""
import argparse
import json

ROUTES = {
    "core": ("php-core",),
    "api": ("api-development", "php-testing", "security-audit", "phpstan-analysis"),
    "analysis": ("phpstan-analysis", "php-core"),
    "refactor": ("php-refactoring", "php-testing"),
    "performance": ("php-performance",),
    "testing": ("php-testing",),
    "security": ("security-audit",),
    "framework": (),
}


def route(tasks, framework):
    skills = []
    for task in tasks:
        primary, *support = ROUTES[task] or (
            "laravel-development" if framework == "laravel" else "php-core",
        )
        skills.append(primary)
        if framework == "laravel" and task in {"api", "refactor", "performance"}:
            skills.append("laravel-development")
        skills.extend(support)
    return list(dict.fromkeys(skills))


PHASES = ("discover", "design", "implement", "verify", "report")
PRIMARY_REASONS = {
    "core": "Resolve a PHP language or compatibility decision.",
    "api": "Work on the API contract or endpoint implementation.",
    "analysis": "Diagnose or fix a static analysis finding.",
    "refactor": "Preserve behavior while restructuring code.",
    "performance": "Measure or address a suspected bottleneck.",
    "testing": "Write or diagnose project tests.",
    "security": "Review or repair a security boundary.",
    "framework": "Resolve framework-specific behavior or wiring.",
}
NEEDS = {
    "framework-wiring": (("design", "implement", "verify"), "laravel-development",
                         "Framework behavior or wiring needs Laravel-specific guidance."),
    "php-compatibility": (("design", "implement"), "php-core",
                          "The PHP version or language behavior affects this change."),
    "api-contract": (("design", "implement", "verify"), "api-development",
                     "An API contract decision or compatibility question is open."),
    "regression-coverage": (("implement", "verify"), "php-testing",
                            "Coverage needs to be added or diagnosed."),
    "analysis-finding": (("implement", "verify"), "phpstan-analysis",
                         "An analyzer finding requires interpretation or repair."),
    "security-boundary": (("design", "implement", "verify"), "security-audit",
                          "Access control or another trust boundary needs review."),
    "performance-evidence": (("design", "implement", "verify"), "php-performance",
                              "A performance question requires measurement or interpretation."),
}


def route_phase(task, framework, phase, needs=(), loaded=()):
    """Recommend work for an agent-classified phase using explicit evidence signals."""
    selected = {}

    if phase in {"design", "implement"} or (
        phase == "verify" and task in {"analysis", "testing", "security", "performance"}
    ):
        primary = next(iter(ROUTES[task]), None)
        if primary is None:
            primary = "laravel-development" if framework == "laravel" else "php-core"
        selected[primary] = PRIMARY_REASONS[task]

    deferred = []
    for need in dict.fromkeys(needs):
        phases, skill, reason = NEEDS[need]
        if phase not in phases or (need == "framework-wiring" and framework != "laravel"):
            deferred.append(need)
        else:
            selected.setdefault(skill, reason)

    return {
        "phase": phase,
        "task": task,
        "framework": framework,
        "skills": [{"name": skill, "reason": reason, "action": "reuse" if skill in loaded else "load"}
                   for skill, reason in selected.items()],
        "deferred_needs": deferred,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="+", choices=tuple(ROUTES))
    parser.add_argument("--framework", default="unknown",
                        choices=("unknown", "plain-php", "laravel", "symfony"))
    parser.add_argument("--phase", choices=PHASES)
    parser.add_argument("--need", action="append", choices=tuple(NEEDS), default=[])
    parser.add_argument("--loaded", action="append", choices=sorted({
        "php-engineer", "laravel-development", *(skill for skills in ROUTES.values() for skill in skills)
    }), default=[])
    args = parser.parse_args()
    if args.phase:
        if len(args.tasks) != 1:
            parser.error("phase routing requires one current task category")
        print(json.dumps(route_phase(args.tasks[0], args.framework, args.phase, args.need, args.loaded)))
        return
    if args.need or args.loaded:
        parser.error("--need and --loaded require --phase")
    print(json.dumps(route(args.tasks, args.framework)))


if __name__ == "__main__":
    main()
