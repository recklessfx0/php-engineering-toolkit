"""Suggest a small skill shortlist from explicit task categories."""
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", nargs="+", choices=tuple(ROUTES))
    parser.add_argument("--framework", default="unknown",
                        choices=("unknown", "plain-php", "laravel", "symfony"))
    args = parser.parse_args()
    print(json.dumps(route(args.tasks, args.framework)))


if __name__ == "__main__":
    main()
