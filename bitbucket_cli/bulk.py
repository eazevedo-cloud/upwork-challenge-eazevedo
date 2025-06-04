import yaml
from colorama import Fore
import requests

def bulk_create_projects_and_repositories(projects_api, repos_api, branch_api, yaml_file_path, workspace, debug=False):
    try:
        with open(yaml_file_path, "r") as file:
            data = yaml.safe_load(file)

        for project_data in data.get("projects", []):
            project_key = project_data["key"]
            name = project_data["name"]
            description = project_data.get("description", "")

            print(f"{Fore.CYAN}Creating project: {name} (Key: {project_key})")
            project_result = projects_api.create_project(workspace, project_key, name, description)

            if project_result["success"]:
                print(f"{Fore.GREEN}{project_result['message']}")
            elif "already exists" in project_result["message"]:
                print(f"{Fore.YELLOW}{project_result['message']}")
            else:
                print(f"{Fore.RED}{project_result['message']}")
                continue

            for repo_data in project_data.get("repositories", []):
                repo_slug = repo_data["slug"]
                is_private = repo_data.get("is_private", True)
                branches = repo_data.get("branches", "")
                print(f"{Fore.CYAN}Creating repository: {repo_slug} in project {project_key}")
                repo_result = repos_api.create_repository(workspace, project_key, repo_slug, is_private)
                if repo_result["success"]:
                    print(f"{Fore.GREEN}{repo_result['message']}")
                    # Initial commit to allow branch creation
                    commit_result = repos_api.push_initial_commit(workspace, repo_slug, branch="main")
                    if commit_result.get("success"):
                        print(f"{Fore.GREEN}  Initial file committed to '{repo_slug}'.")
                    else:
                        print(f"{Fore.RED}  Failed to commit initial file to '{repo_slug}': {commit_result.get('message')}")
                    # Branch creation logic
                    if branches:
                        branch_list = []
                        if isinstance(branches, str):
                            branch_list = [b.strip() for b in branches.split(";") if b.strip()]
                        elif isinstance(branches, list):
                            branch_list = branches
                        for branch in branch_list:
                            branch_result = repos_api.create_branch(workspace, repo_slug, branch)
                            # Hide the error if the branch already exists
                            error_message = branch_result.get('message', '')
                            if branch_result.get("success"):
                                print(f"{Fore.GREEN}  Branch '{branch}' created.")
                            elif "BRANCH_ALREADY_EXISTS" in error_message or "Branch \"main\" already exists" in error_message:
                                # Silently skip or optionally print a yellow info message
                                pass
                            else:
                                print(f"{Fore.RED}  Failed to create branch '{branch}': {error_message}")
                    # Protect the main branch if it was created
                    if branch_list and "main" in branch_list:
                        # Optionally, add this check before protecting the branch
                        branch_check_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches/main"
                        branch_check_resp = requests.get(branch_check_url, headers=branch_api.auth.get_headers())
                        if branch_check_resp.status_code == 200:
                            protect_result = branch_api.protect_branch(workspace, repo_slug, branch_name="main")
                            if protect_result.get("success"):
                                print(f"{Fore.GREEN}  Branch 'main' protected (PRs required).")
                            else:
                                print(f"{Fore.RED}  Failed to protect 'main': {protect_result.get('message')}")
                        else:
                            print(f"{Fore.RED}  Main branch does not exist yet in '{repo_slug}'. Cannot apply protection.")
                elif "already exists" in repo_result["message"]:
                    print(f"{Fore.YELLOW}{repo_result['message']}")
                else:
                    print(f"{Fore.RED}{repo_result['message']}")
        print(f"{Fore.GREEN}Bulk creation process completed successfully.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{yaml_file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error parsing YAML file: {e}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred during bulk creation: {e}")

def bulk_delete_projects_and_repositories(projects_api, repos_api, yaml_file_path, workspace):
    try:
        with open(yaml_file_path, "r") as file:
            data = yaml.safe_load(file)

        for project_data in data.get("projects", []):
            project_key = project_data["key"]
            print(f"{Fore.CYAN}Deleting repositories in project: {project_key}")
            for repo_data in project_data.get("repositories", []):
                repo_slug = repo_data["slug"]
                print(f"{Fore.CYAN}  Deleting repository: {repo_slug}")
                result = repos_api.delete_repository(workspace, repo_slug)
                if result:
                    print(f"{Fore.GREEN}    Repository '{repo_slug}' deleted successfully.")
                else:
                    print(f"{Fore.YELLOW}    Repository '{repo_slug}' could not be deleted or does not exist.")

            # Optionally, delete the project itself after deleting repos
            print(f"{Fore.CYAN}Deleting project: {project_key}")
            project_deleted = projects_api.delete_project(workspace, project_key)
            if project_deleted:
                print(f"{Fore.GREEN}  Project '{project_key}' deleted successfully.")
            else:
                print(f"{Fore.YELLOW}  Project '{project_key}' could not be deleted or does not exist.")

        print(f"{Fore.GREEN}Bulk deletion process completed successfully.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{yaml_file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error parsing YAML file: {e}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred during bulk deletion: {e}")

class BitbucketBranchPermissions:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = "https://api.bitbucket.org/2.0"

    def protect_branch(self, workspace, repo_slug, branch_name="main"):
        """
        Protect a branch so only pull requests can update it (no direct pushes).
        """
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}/branch-restrictions"
        payload = {
            "kind": "push",
            "pattern": branch_name,
            "users": [],
            "groups": [],
            "value": None
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=payload)
        if response.status_code in (200, 201):
            return {"success": True, "message": f"Branch '{branch_name}' protected in '{repo_slug}'."}
        else:
            print(f"DEBUG: {response.status_code} {response.text}")  # Add this line
            return {"success": False, "message": response.text}