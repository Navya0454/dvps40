import subprocess


def run_git(command):
    """Run a Git command and return its output."""

    print(f"\n> git {' '.join(command)}")

    result = subprocess.run(
        ["git"] + command,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())

        raise RuntimeError(
            f"Git command failed: git {' '.join(command)}"
        )

    return result.stdout.strip()


def create_fix_branch():

    branch_name = "dvps40-auto-fix"

    # Get latest information from GitHub
    run_git(["fetch", "origin"])

    # Switch to main
    run_git(["checkout", "main"])

    # Update main
    run_git(["pull", "origin", "main"])

    # Create fix branch
    try:
        run_git(["checkout", "-b", branch_name])

        print(f"\nCreated branch: {branch_name}")

    except RuntimeError:

        # Branch already exists
        run_git(["checkout", branch_name])

        print(f"\nUsing existing branch: {branch_name}")

    return branch_name


def commit_and_push(branch_name, commit_message):

    print("\n--- CHANGED FILES ---")

    run_git(["status", "--short"])

    # Add all changes
    run_git(["add", "."])

    # Commit
    run_git([
        "commit",
        "-m",
        commit_message
    ])

    # Push branch to GitHub
    run_git([
        "push",
        "-u",
        "origin",
        branch_name
    ])

    print("\nGitHub push successful!")


if __name__ == "__main__":

    print("=" * 55)
    print("DVPS40 GITHUB AUTO-FIX TEST")
    print("=" * 55)

    try:

        branch = create_fix_branch()

        print("\n--------------------------------")
        print("GitHub Auto-Fix branch ready!")
        print("--------------------------------")

        print("Branch:", branch)

    except Exception as e:

        print("\nGitHub Auto-Fix failed.")
        print("Error:", e)