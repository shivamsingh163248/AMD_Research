import requests

# === Config ===
GITHUB_OWNER = "shivamsingh163248"   # Replace with your GitHub org/username
GITHUB_TOKEN = "GitHub personal access token"  # Optional: GitHub personal access token
file1_path = "Latest_Commit.txt"
file2_path = "Latest_commit1.txt"

# === Function to load commits ===
def load_commit_file(filepath):
    repo_dict = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            repo, commit = line.split(":", 1)
            repo_dict[repo.strip()] = commit.strip()
    return repo_dict

# === Load commit data ===
file1_commits = load_commit_file(file1_path)
file2_commits = load_commit_file(file2_path)

# === Setup Requests headers ===
headers = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

# === Compare commits ===
for repo, old_commit in file1_commits.items():
    new_commit = file2_commits.get(repo)
    if not new_commit:
        continue
    if old_commit != new_commit:
        print(f"\n🔹 Repo Changed: {repo}")
        print(f"   Old: {old_commit}")
        print(f"   New: {new_commit}")

        compare_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/compare/{old_commit}...{new_commit}"
        print(f"   Compare URL: {compare_url}")

        # Call GitHub API
        response = requests.get(compare_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"   Commits Changed: {data['total_commits']}")

            # Show commits summary
            for commit in data.get("commits", []):
                sha = commit["sha"][:7]
                msg = commit["commit"]["message"].split("\n")[0]
                author = commit["commit"]["author"]["name"]
                print(f"     - {sha} | {author}: {msg}")

            # Summarize file changes
            added, modified, removed = [], [], []
            for f in data.get("files", []):
                status = f["status"]
                filename = f["filename"]
                if status == "added":
                    added.append(filename)
                elif status == "modified":
                    modified.append(filename)
                elif status == "removed":
                    removed.append(filename)

            if added:
                print("   ✅ Files Added:")
                for f in added:
                    print(f"      + {f}")
            if modified:
                print("   🔄 Files Modified:")
                for f in modified:
                    print(f"      * {f}")
            if removed:
                print("   ❌ Files Removed:")
                for f in removed:
                    print(f"      - {f}")

        else:
            print(f"   ⚠️ Failed to fetch diff (status {response.status_code})")
