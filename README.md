# Bitbucket CLI

A modular, easy-to-maintain Python command-line interface for managing Bitbucket Cloud projects, repositories, users, permissions, and branch protections.  
This tool is designed for automation, bulk operations, and interactive management of Bitbucket resources.

---

## 🚀 Features

- **Create and delete Bitbucket projects and repositories**
- **Bulk creation and deletion from YAML files**
- **Set and revoke user permissions on repositories**
- **List repositories, users, and their permissions in tabular format**
- **Configure and enforce branch protections (require PRs)**
- **Highly modular codebase for easy extension and maintenance**

---

## 📦 Installation

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/bitbucket_cli.git
cd bitbucket_cli
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure your environment

Copy the example environment file and fill in your Bitbucket credentials:

```sh
cp bitbucket_cli/.env_example bitbucket_cli/.env
```

Edit `.env` and set:
- `BITBUCKET_WORKSPACE`
- `BITBUCKET_USERNAME`
- `BITBUCKET_APP_PASSWORD`
- (Optional) `BITBUCKET_CLIENT_ID` and `BITBUCKET_CLIENT_SECRET` for OAuth

### 4. Run as a Python script

```sh
python main.py
```

### 5. (Optional) Install as a CLI tool

To install as a Python module and use the `bitbucket_cli` command globally:

```sh
pip install -e .
```

Now you can run:

```sh
bitbucket_cli
```

---

## 🗂️ Project Structure

```
bitbucket_cli/
    __init__.py
    api.py
    auth.py
    branch_permissions.py
    bulk.py
    cli.py
    groups.py
    projects.py
    repositories.py
    users.py
    projects_and_repos.yaml
main.py
setup.py
requirements.txt
.env
```

- **Each major Bitbucket resource (projects, repositories, users, permissions) is in its own module.**
- **Bulk operations and CLI logic are separated for clarity and maintainability.**

---

## 🖥️ Menu Overview

When you run the CLI, you'll see:

```
Bitbucket CLI Menu:
1. Create a project
2. Create a repo
3. Delete repo
4. Set user permission to repo
5. Revoke user permission from repo
6. List repos, users and their permissions
7. Configure branch permissions
8. Bulk create projects and repositories from YAML file
9. Bulk delete projects and repositories from YAML file
0. Exit
```

### Menu Item Details

#### 1. **Create a project**
- Prompts for project key, name, and description.
- Creates a new Bitbucket project in your workspace.

#### 2. **Create a repo**
- Prompts for project key, repository slug, and privacy (default: private).
- Creates a new repository under the specified project.

#### 3. **Delete repo**
- Prompts for project key.
- Lists all repositories in the project.
- Allows deletion of one, multiple (semicolon-separated), or all repositories interactively.

#### 4. **Set user permission to repo**
- Prompts for repository slug, username, and permission (`read`, `write`, `admin`).
- Grants the specified user the chosen permission on the repository.

#### 5. **Revoke user permission from repo**
- Prompts for repository slug and username.
- Removes the user's access to the repository.

#### 6. **List repos, users and their permissions**
- Prompts for project key.
- Lists all repositories in the project.
- For each repository, displays users and their permissions in a tabular format.

#### 7. **Configure branch permissions**
- Prompts for repository slug, branch name, and (optionally) an exempt user.
- Applies branch protection (e.g., require pull requests for changes).

#### 8. **Bulk create projects and repositories from YAML file**
- Prompts for a YAML file path (see example below).
- Creates projects, repositories, and branches in bulk.
- Pushes an initial commit to each repository to enable branch creation.
- Protects the `main` branch to require PRs.

#### 9. **Bulk delete projects and repositories from YAML file**
- Prompts for a YAML file path.
- Deletes all listed repositories and projects in bulk.

#### 0. **Exit**
- Exits the CLI.

---

## 📝 Example YAML for Bulk Operations

```yaml
projects:
  - key: PROJ1
    name: Project 1
    description: "Project 1 - Created by bulk process"
    repositories:
      - slug: web
        is_private: true
        branches: main;dev;uat;qa
      - slug: mobile
        is_private: true
        branches: "main;dev"
```

---

## 🛠️ Modularity & Maintainability

- **Each resource (projects, repos, users, permissions) is a separate Python module.**
- **Bulk operations are handled in `bulk.py` for clarity.**
- **Authentication is centralized in `auth.py`.**
- **CLI logic is in `cli.py` and can be extended easily.**
- **All API calls are wrapped in classes for easy testing and extension.**

---

## 🧪 Testing

Unit tests are provided in the `tests/` directory.  
Run them with:

```sh
python -m unittest discover tests
```

---

## 🛡️ Security

- **Never commit your real `.env` file!**  
  Use `.env_example` for sharing configuration templates.

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Please open an issue to discuss your ideas or report bugs.

---

## 📄 License

MIT License

---

**Enjoy your automated Bitbucket management!**