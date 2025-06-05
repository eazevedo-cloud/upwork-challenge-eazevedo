## Bitbucket CLI

A modular, easy-to-maintain Python command-line interface for managing Bitbucket Cloud projects, repositories, users, permissions, and branch protections.  
This tool is designed for automation, bulk operations, and interactive management of Bitbucket resources.

---

## 🚀 Features

* **Create and delete Bitbucket projects and repositories**
* **Bulk creation and deletion from YAML files**
* **Set and revoke user permissions on repositories**
* **List repositories, users, and their permissions in tabular format**
* **Configure and enforce branch protections (require PRs)**
* **Highly modular codebase for easy extension and maintenance**

---

## 📦 Installation

### 1\. Clone the repository

```plaintext
git clone https://github.com/eazevedo-cloud/upwork-challenge-eazevedo.git
cd upwork-challenge-eazevedo
```

### 2\. Create a VirtualEnv and Install dependencies

```plaintext
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3\. Configure your environment

Copy the example environment file and fill in your Bitbucket credentials:

```plaintext
cp bitbucket_cli/.env_example bitbucket_cli/.env
```

Edit `.env` and set:

* `BITBUCKET_WORKSPACE`
* `BITBUCKET_USERNAME`
* `BITBUCKET_APP_PASSWORD`
* (Optional) `BITBUCKET_CLIENT_ID` and `BITBUCKET_CLIENT_SECRET` for OAuth

### 4\. Run as a Python script

```plaintext
python main.py
```

### 5\. (Optional) Install as a CLI tool

To install as a Python module and use the `bitbucket_cli` command globally:

```plaintext
pip install -e .
```

Now you can run:

```plaintext
bitbucket_cli
```

---

## 🗂️ Project Structure

```plaintext
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

* **Each major Bitbucket resource (projects, repositories, users, permissions) is in its own module.**
* **Bulk operations and CLI logic are separated for clarity and maintainability.**

---

## 🖥️ Menu Overview

When you run the CLI, you'll see:

```plaintext
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

#### 1\. **Create a project**

* Prompts for project key, name, and description.
* Creates a new Bitbucket project in your workspace.

#### 2\. **Create a repo (basic mode)**

* Prompts for project key, repository slug, and privacy (default: private).
* Creates a new repository under the specified project.

#### 3\. **Delete repo**

* Prompts for project key.
* Lists all repositories in the project.
* Allows deletion of one, multiple (semicolon-separated), or all repositories interactively.

#### 4\. **Set user permission to repo**

* Prompts for repository slug, username, and permission (`read`, `write`, `admin`).
* Grants the specified user the chosen permission on the repository.

#### 5\. **Revoke user permission from repo**

* Prompts for repository slug and username.
* Removes the user's access to the repository.

#### 6\. **List repos, users and their permissions**

* Prompts for project key.
* Lists all repositories in the project.
* For each repository, displays users and their permissions in a tabular format.

#### 7\. **Configure branch permissions**

* Prompts for repository slug, branch name, and (optionally) an exempt user.
* Applies branch protection (e.g., require pull requests for changes).

#### 8\. **Bulk create projects and repositories from YAML file**

* Prompts for a YAML file path (see example below).
* Creates projects, repositories, and branches in bulk.
* Pushes an initial commit to each repository to enable branch creation.
* Protects the `main` branch to require PRs.

#### 9\. **Bulk delete projects and repositories from YAML file**

* Prompts for a YAML file path.
* Deletes all listed repositories and projects in bulk.

#### 0\. **Exit**

* Exits the CLI.

---

## 📝 Example YAML for Bulk Operations

```plaintext
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

* **Each resource (projects, repos, users, permissions) is a separate Python module.**
* **Bulk operations are handled in** `**bulk.py**` **for clarity.**
* **Authentication is centralized in** `**auth.py**`**.**
* **CLI logic is in** `**cli.py**` **and can be extended easily.**
* **All API calls are wrapped in classes for easy testing and extension.**

---

## 🧪 Testing

Unit tests are provided in the `tests/` directory.  
Run them with:

```plaintext
python -m unittest discover tests
```

Expected result:

![](https://33333.cdn.cke-cs.com/kSW7V9NHUXugvhoQeFaf/images/4b8bd44c9ec82961e2b0e0aa8f5c45b07d849eca5c7bbb2e.png)

---

## 🛡️ Security

*   **Never commit your real** `**.env**` **file!**  
    Use `.env_example` for sharing configuration templates.

---

## 🛣️ Roadmap

There are some improvements and future enhancements for the Bitbucket CLI:

1. **Error Handling Enhancements**
    * Implement more robust error handling mechanisms, including retries for transient errors and detailed logging for failures.
2. **OAuth Implementation**
    * Fully implement OAuth for better security and flexibility in authentication, including refreshing tokens automatically.
3. **Improved CLI User Interface**
    * Enhance the CLI interface with better prompts, clearer error messages, and support for command-line arguments using libraries like `argparse` or `click`.
4. **Configuration Management**
    * Introduce centralized configuration management to handle environment variables more efficiently and support multiple environments (e.g., development, staging, production).
5. **Expanded Testing**
    * Increase the test coverage by adding edge case scenarios and integration tests to simulate real-world API interactions.
6. **Logging and Monitoring**
    * Integrate a logging framework to capture detailed logs for debugging and monitoring.
    * Add monitoring for API usage and performance metrics.
7. **Security Enhancements**
    * Ensure sensitive data is never logged or exposed in error messages.
    * Validate all user inputs to prevent injection attacks or malformed requests.
8. **Scalability Improvements**
    * Refactor the codebase to support asynchronous operations for better performance with large datasets or high API call volumes.
    * Optimize API call patterns to minimize latency and reduce redundant requests.
9. **Bulk Operations Improvements**
    * Add validation for YAML files to ensure proper structure before processing.
    * Provide detailed error reports for bulk operations, indicating which items succeeded and which failed.
10. **Real-Time Feedback**  
    \* Provide real-time progress updates for long-running operations, such as bulk actions.

---

These improvements aim to make the Bitbucket CLI more robust, user-friendly, and scalable while ensuring it meets the evolving needs of its users.

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Please open an issue to discuss your ideas or report bugs.

---

## 📄 License

MIT License

---

**Enjoy your automated Bitbucket management!**