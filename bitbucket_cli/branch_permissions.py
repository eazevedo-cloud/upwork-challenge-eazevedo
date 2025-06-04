import requests

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
            return {"success": False, "message": response.text}
