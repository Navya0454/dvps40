from log_analyzer import analyze_log
from ai_engine import diagnose_with_groq, generate_fix
from fix_applier import apply_fix
from git_autofix import commit_and_push
from github_pr import create_pull_request

import re
import subprocess
from datetime import datetime


def create_new_branch():
    branch_name = "dvps40-auto-fix-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return branch_name


def main():
    print("=" * 60)
    print("DVPS40 - AUTONOMOUS AUTO-FIXING DEVOPS BOT")
    print("=" * 60)

    print("\nPaste your deployment/server error below.")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    log = "\n".join(lines)

    if not log.strip():
        return

    print("\n[1/6] Analyzing error...")

    result = analyze_log(log)

    print("\n[2/6] Asking Groq AI to diagnose the problem...")

    groq_result = diagnose_with_groq(log)

    print("\n[3/6] Generating AI fix...")

    fix_result = generate_fix(log, groq_result)

    print("\n[4/6] Applying AI fix...")

    fix_applied = False

    if "ModuleNotFoundError" in log:
        match = re.search(
            r"No module named ['\"]([^'\"]+)['\"]",
            log
        )

        if match:
            package_name = match.group(1)

            changed = apply_fix(
                "INSTALL_PACKAGE",
                package_name
            )

            if changed:
                fix_applied = True

    if not fix_applied:
        print("\nNo automatic fix was applied.")
        return

    print("\n[5/6] Committing and pushing AI fix to GitHub...")

    branch_name = create_new_branch()

    commit_and_push(
        branch_name,
        "DVPS40: Apply AI-generated auto-fix"
    )

    print("\n[6/6] Creating automatic Pull Request...")

    pr_title = "DVPS40: Automated AI Auto-Fix"

    pr_body = (
        "## DVPS40 Automated AI Auto-Fix\n\n"
        "### Detected Error\n\n"
        "```text\n"
        + log +
        "\n```\n\n"
        "### AI Diagnosis\n\n"
        + groq_result +
        "\n\n"
        "### AI Generated Fix\n\n"
        + fix_result +
        "\n\n"
        "### Automated Actions\n\n"
        "- Error analyzed\n"
        "- Groq AI diagnosis completed\n"
        "- AI fix generated\n"
        "- Fix applied\n"
        "- Git commit created\n"
        "- Changes pushed to GitHub\n"
        "- Pull Request created automatically\n\n"
        "### Branch\n\n"
        "`"
        + branch_name +
        "`\n"
    )

    pr_url = create_pull_request(
        branch_name,
        pr_title,
        pr_body
    )

    print("\n========================================")
    print("LIVE PULL REQUEST CREATED")
    print("========================================")
    print(pr_url)
    print("========================================")


if __name__ == "__main__":
    main()