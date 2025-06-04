import requests
from tabulate import tabulate  # Ensure tabulate is imported

class BitbucketUsers:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = "https://api.bitbucket.org/2.0"

    def add_user_to_repo(self, workspace, repo_slug, username, permission):
        """
        Add a user to a repository with specific permission.
        Permissions: 'read', 'write', 'admin'
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/permissions-config/users/{username}"
        payload = {"permission": permission}
        response = requests.put(url, json=payload, headers=self.auth.get_headers())
        if response.status_code in [200, 201]:
            return {"message": f"User '{username}' added to repository '{repo_slug}' with '{permission}' permission."}
        else:
            return response.json()

    def remove_user_from_repo(self, workspace, repo_slug, username):
        """
        Remove a user's access to a repository.
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/permissions-config/users/{username}"
        response = requests.delete(url, headers=self.auth.get_headers())
        if response.status_code == 204:
            return {"message": f"User '{username}' removed from repository '{repo_slug}'."}
        else:
            return response.json()

    def list_users_and_groups(self, workspace):
        """
        List all users in a workspace and their current groups.
        """
        url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/members"
        response = requests.get(url, headers=self.auth.get_headers())

        if response.status_code == 200:
            members = response.json().get("values", [])
            table_data = []  # Prepare data for tabular output
            for member in members:
                table_data.append([
                    member["user"]["nickname"],  # Use 'nickname' instead of 'username'
                    member["user"]["display_name"],
                    member["workspace"]["name"],
                ])

            # Define table headers
            headers = ["Nickname", "Display Name", "Workspace Name"]

            # Return the table as a string
            return tabulate(table_data, headers=headers, tablefmt="grid")
        else:
            # Handle non-JSON responses gracefully
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return {
                    "error": f"Failed to parse response. Status Code: {response.status_code}, Response: {response.text}"
                }

    def list_users_and_permissions(self, workspace, repo_slug):
        url = f"{self.base_url}/repositories/{workspace}/{repo_slug}/permissions-config/users"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 200:
            data = response.json()
            users = [
                {
                    "username": user["user"]["nickname"] if "nickname" in user["user"] else user["user"]["username"],
                    "permission": user["permission"]
                }
                for user in data.get("values", [])
            ]
            return {"success": True, "users": users}
        else:
            return {
                "success": False,
                "message": f"Failed to fetch users for repository '{repo_slug}'. Error: {response.text}"
            }