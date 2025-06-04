import requests

class BitbucketProjects:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = "https://api.bitbucket.org/2.0"

    def create_project(self, workspace, project_key, name, description):
        url = f"{self.base_url}/workspaces/{workspace}/projects"
        payload = {"key": project_key, "name": name, "description": description}
        response = requests.post(url, headers=self.auth.get_headers(), json=payload)
        if response.status_code == 201:
            return {"success": True, "message": f"Project '{name}' (Key: {project_key}) created successfully."}
        elif response.status_code == 400 and "already exists" in response.json().get("error", {}).get("message", "").lower():
            return {"success": False, "message": f"Project '{name}' (Key: {project_key}) already exists."}
        else:
            return {"success": False, "message": f"Failed to create project '{name}' (Key: {project_key}). Error: {response.text}"}

    def delete_project(self, workspace, project_key):
        url = f"{self.base_url}/workspaces/{workspace}/projects/{project_key}"
        response = requests.delete(url, headers=self.auth.get_headers())
        return response.status_code == 204