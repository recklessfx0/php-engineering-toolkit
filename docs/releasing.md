# Publishing and releasing

1. Review the license holder attribution and enable private vulnerability reporting in the GitHub repository settings.
2. Run `python scripts/validate_skills.py` and `python -m unittest discover -s tests -v`. Smoke-test local skill discovery in CLI and the IDE, then test plugin installation from a local marketplace.
3. Create an empty public GitHub repository named `php-engineering-toolkit`. Copy its actual Git URL and use it in the command below.
4. Review the staged files and commit, then push.

```sh
git add .
git diff --cached --check
git commit -m "Add PHP Engineering Toolkit for Codex"
git branch -M main
git remote add origin <actual-git-url>
git push -u origin main
```

5. Review the hosted Actions results. Update the changelog and plugin manifest together for each release. Tag the verified release commit and create a GitHub Release from the tag if desired.

Publishing a GitHub repository makes standalone installation from a checkout available. Plugin directory distribution is a separate submission. [Official plugin packaging and distribution guidance](https://developers.openai.com/plugins/build/plugins)
