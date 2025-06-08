import subprocess
import sys
import os

PROGRESS_FILE = "progress.log"
README_FILE = "README.md"
LOG_START = "<!-- PROGRESS_LOG_START -->"
LOG_END = "<!-- PROGRESS_LOG_END -->"
FEATURE_BRANCH = "test-learn-logic-smile-detect/ullas"

def get_progress_log():
    try:
        content = subprocess.check_output(
            ["git", "show", f"origin/{FEATURE_BRANCH}:{PROGRESS_FILE}"],
            stderr=subprocess.STDOUT
        ).decode()
        return content.strip()
    except subprocess.CalledProcessError:
        print(f"Error: Cannot find {PROGRESS_FILE} in {FEATURE_BRANCH}")
        sys.exit(1)

def update_readme(progress_content):
    with open(README_FILE, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if LOG_START in line:
            start_idx = i
        elif LOG_END in line:
            end_idx = i
            break

    if start_idx is None or end_idx is None or end_idx <= start_idx:
        print(f"Error: Could not find proper log markers in {README_FILE}")
        sys.exit(1)

    new_lines = (
        lines[: start_idx + 1]
        + [progress_content + "\n"]
        + lines[end_idx:]
    )

    with open(README_FILE, "w", encoding="utf-8-sig") as f:
        f.writelines(new_lines)

def git_commit_push():
    subprocess.run(["git", "add", README_FILE], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Update progress log from {FEATURE_BRANCH}"], check=True
    )
    subprocess.run(["git", "push", "origin", "main"], check=True)

def main():
    branch = (
        subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()
    )
    if branch != "main":
        print("Switch to main branch first: git checkout main")
        sys.exit(1)

    subprocess.run(["git", "pull", "origin", "main"], check=True)

    progress_content = get_progress_log()
    update_readme(progress_content)
    git_commit_push()
    print("README.md progress log updated successfully!")

if __name__ == "__main__":
    main()
