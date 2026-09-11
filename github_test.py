from pathlib import Path
from dotenv import dotenv_values
from github import Github, Auth

BASE_DIR = Path(__file__).resolve().parent
config = dotenv_values(BASE_DIR / ".env")

token = config.get("GITHUB_TOKEN")
owner = config.get("GITHUB_OWNER")
repo_name = config.get("GITHUB_REPO")

print("=" * 55)
print("DVPS40 GITHUB PERMISSION TEST")
print("=" * 55)

print("Owner :", owner)
print("Repo  :", repo_name)
print("Token :", "FOUND" if token else "MISSING")

try:
    github = Github(auth=Auth.Token(token))

    user = github.get_user()
    print("\nAuthenticated user:", user.login)

    repo = github.get_repo(f"{owner}/{repo_name}")

    print("Repository:", repo.full_name)
    print("Default branch:", repo.default_branch)

    print("\nRepository permissions:")
    print("Admin :", repo.permissions.admin)
    print("Push  :", repo.permissions.push)
    print("Pull  :", repo.permissions.pull)

except Exception as e:
    print("\nERROR:")
    print(e)