import requests

# === Config ===
GITHUB_OWNER = "shivamsingh163248"   # Your GitHub username
# GITHUB_TOKEN = ""  # Optional: GitHub personal access token (not required for public repos)
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

# === Compare commits and write to file ===
output_lines = []
for repo, old_commit in file1_commits.items():
    new_commit = file2_commits.get(repo)
    if not new_commit:
        continue
    if old_commit != new_commit:
        output_lines.append(f"\n🔹 Repo Changed: {repo}\n")
        output_lines.append(f"Old: {old_commit}\n")
        output_lines.append(f"New: {new_commit}\n")
        compare_url = f"https://github.com/{GITHUB_OWNER}/{repo}/compare/{old_commit}...{new_commit}"
        output_lines.append(f"Compare URL: View Changes ({compare_url})\n")

        # Call GitHub API (optional, for commit details)
        response = requests.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/compare/{old_commit}...{new_commit}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            output_lines.append(f"Commits Changed: {data['total_commits']}\n")
            for commit in data.get("commits", []):
                sha = commit["sha"][:7]
                msg = commit["commit"]["message"].split("\n")[0]
                author = commit["commit"]["author"]["name"]
                output_lines.append(f"  - {sha} | {author}: {msg}\n")
        else:
            output_lines.append(f"⚠️ Failed to fetch diff (status {response.status_code})\n")

# Write results to a file
with open("commit_changes_report.txt", "w", encoding="utf-8") as f:
    f.writelines(output_lines)
