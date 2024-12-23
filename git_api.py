import requests

api_url = "https://api.github.com"
username = input("Enter GitHub username: ")

headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "ed-freitas"
}

repos_url = f"{api_url}/users/{username}/repos"
r = requests.get(repos_url, headers=headers)

if r.status_code == 200:
    repositories = r.json()
    print(f"Repos for {username}: ")
    for repo in repositories:
        repo_name = repo["name"]
        repos_description = repo["description"]
        repo_stars = repo["stargazers_count"]
        repo_forks = repo["forks_count"]
        print(f"Repo: {repo_name}")
        print(f"Description: {repos_description}")
        print(f"Stars: {repo_stars}")
        print(f"Forks: {repo_forks}")
        print("-" * 30)
else:
    print("Error fetching repos")