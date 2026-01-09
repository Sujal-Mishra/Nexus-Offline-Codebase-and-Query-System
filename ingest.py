import os
import json
from git import Repo

EXTENSIONS = (".py", ".js", ".java", ".cpp")

def clone_repo(url):
    if not os.path.exists("repo"):
        Repo.clone_from(url, "repo")

def read_code():
    chunks = []

    for root, _, files in os.walk("repo"):
        for file in files:
            if file.endswith(EXTENSIONS):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        if len(code) > 100:
                            chunks.append({
                                "file": path,
                                "code": code
                            })
                except:
                    pass
    return chunks

if __name__ == "__main__":
    url = input("GitHub repo URL: ")
    clone_repo(url)

    os.makedirs("data", exist_ok=True)
    chunks = read_code()

    with open("data/chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"✅ Saved {len(chunks)} code files")
