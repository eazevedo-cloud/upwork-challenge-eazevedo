import requests


class BitbucketGroups:
    def __init__(self, auth):
        """
        Initialize the BitbucketGroups class with authentication details.
        :param auth: An object responsible for providing authentication headers.
        """
        self.auth = auth

    # Removed `list_groups` method

    # Removed `create_group` method
    def move_user_to_group(self, workspace, username, group_slug):
        """
        Move a user to a different group in a workspace.
        :param workspace: The workspace ID.
        :param username: The username of the user to move.
        :param group_slug: The slug of the group to move the user to.
        :return: A success message or an error message.
        """
        url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/permissions/groups/{group_slug}/members"
        payload = {"username": username}
        try:
            response = requests.post(url, json=payload, headers=self.auth.get_headers())
            if response.status_code in [200, 201]:
                return {"message": f"User '{username}' moved to group '{group_slug}' successfully."}
            else:
                return {
                    "error": f"Failed to move user to group. Status code: {response.status_code}",
                    "details": response.json(),
                }
        except Exception as e:
            return {"error": f"An exception occurred: {str(e)}"}
