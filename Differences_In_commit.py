# Let's compare the two provided files to identify differences in commit IDs for each repo.

file1_path = "/mnt/data/letest_comit 1.txt"
file2_path = "/mnt/data/letest_commit.txt"

# Load files into dictionaries for easy comparison
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

file1_commits = load_commit_file(file1_path)
file2_commits = load_commit_file(file2_path)

# Find differences
differences = []
for repo in file1_commits:
    if repo in file2_commits:
        if file1_commits[repo] != file2_commits[repo]:
            differences.append((repo, file1_commits[repo], file2_commits[repo]))

num_changed = len(differences)

import pandas as pd
df_diff = pd.DataFrame(differences, columns=["Repository", "Commit in File1", "Commit in File2"])

import ace_tools as tools; tools.display_dataframe_to_user("Commit Differences", df_diff)

num_changed, df_diff.head()
