import requests
from colorama import Fore
from tabulate import tabulate
from datetime import datetime
import base64
import os
import tempfile
import subprocess

class BitbucketRepositories:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = "https://api.bitbucket.org/2.0"

    def create_repository(self, workspace, project_key, repo_slug, is_private=True):
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}"
        payload = {
            "scm": "git",
            "project": {"key": project_key},
            "is_private": is_private  # Default is True
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=payload)

        if response.status_code == 201:
            repo_details = response.json()
            return {
                "success": True,
                "message": f"Repository '{repo_slug}' created successfully in project '{project_key}'.",
                "details": repo_details
            }
        elif response.status_code == 200:
            repo_details = response.json()
            created = repo_details.get("created_on")
            updated = repo_details.get("updated_on")
            try:
                if created and updated:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    # Thats a funny workaround. Bitbucket API takes a while to 'forget' a repo name after deletion.
                    # That behaviour was detected during massive code testing.
                    # So, if the repo was just deleted, the timestamps will be very close and creation will fail.
                    # Not pretty, but it definitely works! haha
                    if abs((updated_dt - created_dt).total_seconds()) < 2:
                        return {
                            "success": True,
                            "message": f"Repository '{repo_slug}' created successfully in project '{project_key}'.",
                            "details": repo_details
                        }
            except Exception:
                pass
            return {
                "success": False,
                "already_exists": True,
                "message": f"Repository '{repo_slug}' already exists in project '{project_key}'.",
                "details": repo_details
            }
        elif response.status_code == 400:
            error_message = response.json().get("error", {}).get("message", "").lower()
            if "already exists" in error_message:
                return {
                    "success": False,
                    "already_exists": True,
                    "message": f"Repository '{repo_slug}' already exists in project '{project_key}'."
                }
        return {
            "success": False,
            "message": f"Failed to create repository '{repo_slug}' in project '{project_key}'.",
            "error_details": response.json()
        }

    def list_repositories(self, workspace, project_key):
        url = f"{self.base_url}/repositories/{workspace}?q=project.key=\"{project_key}\""
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 200:
            data = response.json()
            repos = [
                {"slug": repo["slug"], "name": repo.get("name", repo["slug"])}
                for repo in data.get("values", [])
            ]
            return {"success": True, "repositories": repos}
        else:
            return {
                "success": False,
                "message": f"Failed to fetch repositories for project '{project_key}'. Error: {response.text}"
            }

    def delete_repository(self, workspace, repo_slug):
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}"
        response = requests.delete(url, headers=self.auth.get_headers())
        return response.status_code == 204

    def delete_repositories_interactive(self, workspace):
        project_key = input("Project Key: ")
        repos_response = self.list_repositories(workspace, project_key)
        if not repos_response.get("success"):
            print(f"{Fore.RED}{repos_response.get('message', 'Failed to fetch repositories.')}")
            return

        repos = repos_response["repositories"]
        if not repos:
            print(f"{Fore.YELLOW}No repositories found in project '{project_key}'.")
            return

        print(tabulate(
            [[repo["slug"], repo["name"]] for repo in repos],
            headers=["Slug", "Name"],
            tablefmt="fancy_grid"
        ))

        repo_input = input("Enter repository slug(s) to delete (separate with ';') or type 'All' to delete all: ").strip()
        if repo_input.lower() == "all":
            to_delete = [repo["slug"] for repo in repos]
        else:
            to_delete = [slug.strip() for slug in repo_input.split(";") if slug.strip()]

        for repo_slug in to_delete:
            result = self.delete_repository(workspace, repo_slug)
            if result:
                print(f"{Fore.GREEN}Repository '{repo_slug}' deleted successfully.")
            else:
                print(f"{Fore.RED}Failed to delete repository '{repo_slug}'.")

    def create_branch(self, workspace, repo_slug, branch_name, from_branch="main"):
        """
        Create a branch in the given repository, from the specified base branch (default: main).
        """
        # Get the latest commit hash from the base branch
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}/refs/branches/{from_branch}"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code != 200:
            return {"success": False, "message": f"Base branch '{from_branch}' not found."}
        target_hash = response.json().get("target", {}).get("hash")
        if not target_hash:
            return {"success": False, "message": f"Could not determine commit hash for '{from_branch}'."}

        # Create the new branch
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}/refs/branches"
        payload = {
            "name": branch_name,
            "target": {"hash": target_hash}
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=payload)
        if response.status_code in (200, 201):
            return {"success": True}
        else:
            return {"success": False, "message": response.text}
    # Create an initial commit with a file in the given repository and branch.
    # That allows the bulk creation of repositories with branches
    # Another workaround, but not related to Bitbucket, but to Gitflow nature
    def commit_initial_file(self, workspace, repo_slug, branch="main", filename="DELETEME", content="Temporary file for branch creation"):
        """
        Create an initial commit with a file in the given repository and branch.
        """
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}/src"
        files = {
            filename: content
        }
        data = {
            "branch": branch,
            "message": f"Initial commit with {filename}"
        }
        response = requests.post(url, headers=self.auth.get_headers(), data=data, files={filename: (filename, content)})
        if response.status_code in (200, 201):
            return {"success": True}
        else:
            return {"success": False, "message": response.text}

    def push_initial_commit(self, workspace, repo_slug, branch="main", filename="DELETEME", content="Temporary file for branch creation"):
        """
        Clone the repo, create a file, commit, and push to create the default branch.
        """
        from dotenv import load_dotenv
        load_dotenv()  # Ensure .env is loaded

        username = os.getenv("BITBUCKET_USERNAME")
        app_password = os.getenv("BITBUCKET_APP_PASSWORD")
        if not username or not app_password:
            return {"success": False, "message": "Missing BITBUCKET_USERNAME or BITBUCKET_APP_PASSWORD in environment."}

        repo_url = f"https://{username}:{app_password}@bitbucket.org/{workspace}/{repo_slug}.git"

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                subprocess.check_call(
                    ["git", "clone", repo_url, tmpdir],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                file_path = os.path.join(tmpdir, filename)
                with open(file_path, "w") as f:
                    f.write(content)
                subprocess.check_call(["git", "-C", tmpdir, "add", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", f"Initial commit with {filename}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.check_call(["git", "-C", tmpdir, "branch", "-M", branch], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.check_call(["git", "-C", tmpdir, "push", "origin", branch], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"success": True}
            except subprocess.CalledProcessError as e:
                return {"success": False, "message": str(e)}