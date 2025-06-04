import os
from dotenv import load_dotenv
from colorama import Fore, init

from .auth import BitbucketAuth
from .projects import BitbucketProjects
from .repositories import BitbucketRepositories
from .users import BitbucketUsers
from .branch_permissions import BitbucketBranchPermissions
from .bulk import bulk_create_projects_and_repositories, bulk_delete_projects_and_repositories

init(autoreset=True)

def main():
    load_dotenv()
    workspace = os.getenv("BITBUCKET_WORKSPACE")
    if not workspace:
        print(f"{Fore.RED}Error: BITBUCKET_WORKSPACE is not set in the .env file.")
        return

    auth = BitbucketAuth()
    projects_api = BitbucketProjects(auth)
    repos_api = BitbucketRepositories(auth)
    users_api = BitbucketUsers(auth)
    branch_api = BitbucketBranchPermissions(auth)

    print("\nBitbucket CLI Menu:")
    print("1. Create a project")
    print("2. Create a repo")
    print("3. Delete repo")
    print("4. Set user permission to repo")
    print("5. Revoke user permission from repo")
    print("6. List repos, users and their permissions")
    print("7. Configure branch permissions")
    print("8. Bulk create projects and repositories from YAML file")
    print("9. Bulk delete projects and repositories from YAML file")
    print("0. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        project_key = input("Project Key: ")
        name = input("Project Name: ")
        description = input("Description: ")
        result = projects_api.create_project(workspace, project_key, name, description)
        if result["success"]:
            print(f"{Fore.GREEN}{result['message']}")
        else:
            print(f"{Fore.RED}{result['message']}")
    elif choice == "2":
        project_key = input("Project Key: ")
        repo_slug = input("Repository Slug: ")
        is_private = input("Is private? (Yes/no) - Default Yes: ").lower() != "no"
        result = repos_api.create_repository(workspace, project_key, repo_slug, is_private)
        if result.get("success"):
            print(f"{Fore.GREEN}{result['message']}")
        elif result.get("already_exists"):
            print(f"{Fore.YELLOW}{result['message']}")
        else:
            print(f"{Fore.RED}{result['message']}")
    elif choice == "3":
        repos_api.delete_repositories_interactive(workspace)
    elif choice == "4":
        repo_slug = input("Repository Slug: ")
        username = input("Username: ")
        permission = input("Permission (read/write/admin): ")
        print(users_api.add_user_to_repo(workspace, repo_slug, username, permission))
    elif choice == "5":
        repo_slug = input("Repository Slug: ")
        username = input("Username: ")
        print(users_api.remove_user_from_repo(workspace, repo_slug, username))
    elif choice == "6":
        from tabulate import tabulate

        project_key = input("Project Key: ")
        repos_response = repos_api.list_repositories(workspace, project_key)
        if not repos_response.get("success"):
            print(f"{Fore.RED}{repos_response.get('message', 'Failed to fetch repositories.')}")
        else:
            table = []
            for repo in repos_response["repositories"]:
                repo_slug = repo["slug"]
                users_response = users_api.list_users_and_permissions(workspace, repo_slug)
                if users_response.get("success"):
                    for user_perm in users_response["users"]:
                        table.append([
                            repo["name"],
                            user_perm["username"],
                            user_perm["permission"]
                        ])
                else:
                    table.append([repo["name"], "-", "Failed to fetch users"])
            print(tabulate(
                table,
                headers=["Repository", "User", "Permission"],
                tablefmt="fancy_grid"
            ))
    elif choice == "7":
        repo_slug = input("Repository Slug: ")
        branch_name = input("Branch Name: ")
        exempt_user = input("Exempt User (optional): ")
        print(branch_api.configure_branch_permission(workspace, repo_slug, branch_name, exempt_user))
    elif choice == "8":
        yaml_file = input("Enter the path to the YAML file: ")
        bulk_create_projects_and_repositories(projects_api, repos_api, branch_api, yaml_file, workspace, debug=True)
    elif choice == "9":
        yaml_file = input("Enter the path to the YAML file: ")
        bulk_delete_projects_and_repositories(projects_api, repos_api, yaml_file, workspace)
    elif choice == "0":
        print("Exiting CLI.")
    else:
        print(f"{Fore.RED}Invalid choice. Try again.")

if __name__ == "__main__":
    main()
