import unittest
from unittest.mock import patch, MagicMock
from bitbucket_cli.cli import (
    BitbucketAuth,
    BitbucketProjects,
    BitbucketRepositories,
    BitbucketUsers,
    BitbucketBranchPermissions,
)


class TestBitbucketCLI(unittest.TestCase):
    def setUp(self):
        self.auth = MagicMock()
        self.auth.get_headers.return_value = {"Authorization": "Basic dummy_token"}
        self.workspace = "test_workspace"

    @patch("os.getenv")
    def test_bitbucket_auth(self, mock_getenv):
        mock_getenv.side_effect = lambda key: {
            "BITBUCKET_USERNAME": "test_user",
            "BITBUCKET_APP_PASSWORD": "test_password",
        }.get(key)
        auth = BitbucketAuth()
        headers = auth.get_headers()
        self.assertIn("Authorization", headers)
        self.assertIn("Basic", headers["Authorization"])

    def test_create_project_success(self):
        projects_api = BitbucketProjects(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            result = projects_api.create_project(
                self.workspace, "TEST", "Test Project", "Description"
            )
            self.assertTrue(result["success"])

    def test_create_project_already_exists(self):
        projects_api = BitbucketProjects(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {
                "error": {"message": "Project already exists"}
            }
            result = projects_api.create_project(
                self.workspace, "TEST", "Test Project", "Description"
            )
            self.assertFalse(result["success"])
            self.assertIn("already exists", result["message"].lower())

    def test_delete_project_success(self):
        projects_api = BitbucketProjects(self.auth)
        with patch("requests.delete") as mock_delete:
            mock_delete.return_value.status_code = 204
            result = projects_api.delete_project(self.workspace, "TEST")
            self.assertTrue(result)

    def test_create_repository_success(self):
        repos_api = BitbucketRepositories(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            result = repos_api.create_repository(
                self.workspace, "TEST", "test-repo", True
            )
            self.assertTrue(result["success"])

    def test_create_repository_already_exists(self):
        repos_api = BitbucketRepositories(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {
            "error": {"message": "Repository already exists"}
        }
            result = repos_api.create_repository(
                self.workspace, "TEST", "test-repo", True
            )
            self.assertFalse(result["success"])
            self.assertTrue(result["already_exists"])

    def test_list_repositories_success(self):
        repos_api = BitbucketRepositories(self.auth)
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "values": [{"slug": "test-repo", "name": "Test Repo"}]
            }
            result = repos_api.list_repositories(self.workspace, "TEST")
            self.assertTrue(result["success"])
            self.assertEqual(len(result["repositories"]), 1)

    def test_delete_repository_success(self):
        repos_api = BitbucketRepositories(self.auth)
        with patch("requests.delete") as mock_delete:
            mock_delete.return_value.status_code = 204
            result = repos_api.delete_repository(self.workspace, "test-repo")
            self.assertTrue(result)

    def test_add_user_to_repo(self):
        users_api = BitbucketUsers(self.auth)
        with patch("requests.put") as mock_put:
            mock_put.return_value.status_code = 201
            result = users_api.add_user_to_repo(
                self.workspace, "test-repo", "test_user", "admin"
            )
            self.assertIn("message", result)

    def test_remove_user_from_repo(self):
        users_api = BitbucketUsers(self.auth)
        with patch("requests.delete") as mock_delete:
            mock_delete.return_value.status_code = 204
            result = users_api.remove_user_from_repo(
                self.workspace, "test-repo", "test_user"
            )
            self.assertIn("message", result)

    def test_list_users_and_groups(self):
        users_api = BitbucketUsers(self.auth)
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "values": [
                    {
                        "user": {"nickname": "test_user", "display_name": "Test User"},
                        "workspace": {"name": "Test Workspace"},
                    }
                ]
            }
            result = users_api.list_users_and_groups(self.workspace)
            self.assertIn("Test User", result)

    def test_protect_branch_success(self):
        branch_api = BitbucketBranchPermissions(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            result = branch_api.protect_branch(
                self.workspace, "test-repo", "main"
            )  # Corrected method name
            self.assertTrue(result["success"])  # Check if the branch protection was successful

    def test_protect_branch_failure(self):
        branch_api = BitbucketBranchPermissions(self.auth)
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.text = "Invalid request"
            result = branch_api.protect_branch(self.workspace, "test-repo", "main")
            self.assertFalse(result["success"])
            self.assertIn("Invalid request", result["message"])
