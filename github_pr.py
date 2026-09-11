from pathlib import Path
from dotenv import dotenv_values
import requests

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

config = dotenv_values(ENV_FILE)

GITHUB_TOKEN = config.get("GITHUB_TOKEN")
GITHUB_OWNER = config.get("GITHUB_OWNER")
GITHUB_REPO = config.get("GITHUB_REPO")
BASE_BRANCH = config.get("BASE_BRANCH", "main")


def create_pull_request(branch_name, title, body):

    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is missing from .env")

    if not GITHUB_OWNER:
        raise RuntimeError("GITHUB_OWNER is missing from .env")

    if not GITHUB_REPO:
        raise RuntimeError("GITHUB_REPO is missing from .env")

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/pulls"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "title": title,
        "body": body,
        "head": branch_name,
        "base": BASE_BRANCH
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=20
    )

    if response.status_code == 201:

        result = response.json()

        print("\n========================================")
        print("AUTOMATIC PULL REQUEST CREATED")
        print("========================================")

        print("PR Number :", result["number"])
        print("PR Title  :", result["title"])
        print("PR URL    :", result["html_url"])

        return result["html_url"]

    else:

        print("\nGitHub PR creation failed.")
        print("Status :", response.status_code)
        print("Response:", response.text)

        raise RuntimeError(
            f"GitHub PR creation failed: "
            f"{response.status_code}"
        )


if __name__ == "__main__":

    print("=" * 55)
    print("DVPS40 GITHUB PULL REQUEST TEST")
    print("=" * 55)

    create_pull_request(
        "dvps40-auto-fix",
        "DVPS40: Automated AI Auto-Fix",
        """## DVPS40 Automated Auto-Fix

DVPS40 detected a deployment/server error and automatically:

- Analyzed the error
- Generated an AI diagnosis
- Generated an AI fix
- Applied the fix
- Committed the change
- Pushed the fix to a dedicated branch

### Branch

`dvps40-auto-fix`

Please review the automated fix before merging.
"""
    )