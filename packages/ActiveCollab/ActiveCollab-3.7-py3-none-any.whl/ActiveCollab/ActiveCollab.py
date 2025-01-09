import requests
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Connect:
    def __init__(self , host_url , login_email , login_password):
        # Ensure the base URL is correctly handled
        self.host_url = host_url.rstrip('/')
        url = f'{self.host_url}/api/v1/issue-token'
        headers = {"Content-Type": "application/json"}
        data = {
            "username": login_email ,
            "password": login_password ,
            "client_name": "My ActiveCollab App" ,
            "client_vendor": "ACME Inc" ,
        }

        try:
            logging.info(f"Authenticating with URL: {url}")
            response = requests.post(url , headers=headers , json=data , timeout=10)

            if response.status_code == 200:
                self.token = response.json().get('token' , None)
                if not self.token:
                    logging.error("Authentication succeeded but token is missing.")
                    sys.exit("Authentication failed: Missing token.")

            else:
                logging.error(f"Authentication failed: {response.status_code} - {response.text}")
                sys.exit("Authentication failed.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during authentication: {e}")
            sys.exit("Authentication failed.")

    def _make_request(self, method, endpoint, **kwargs):
        """Helper method to make HTTP requests."""
        url = f'{self.host_url}{endpoint}'
        headers = kwargs.pop('headers', {})
        headers.update({"X-Angie-AuthApiToken": self.token})
        try:
            response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            sys.exit("HTTP request failed.")

    def list_projects(self):
        """Fetch a list of all projects."""
        try:
            projects_data = self._make_request("GET", "/api/v1/projects")
            projects = [
                {"id": proj["id"], "name": proj["name"], "members": proj["members"]}
                for proj in projects_data
            ]
            return projects
        except Exception as e:
            logging.error(f"Error while fetching projects: {e}")
            return []

    def list_project_tasklist(self, project_id):
        """Fetch a list of task lists for a specific project."""
        try:
            projects_data = self._make_request("GET", f"/api/v1/projects/{project_id}/task-lists")
            projects_tasklist = [
                {"id": tasklist["id"], "name": tasklist["name"]}
                for tasklist in projects_data
            ]
            return projects_tasklist
        except Exception as e:
            logging.error(f"Error while fetching task lists for project {project_id}: {e}")
            return []

    def list_users(self):
        """Fetch a list of all users."""
        try:
            users_data = self._make_request("GET", "/api/v1/users")
            users = [
                {"id": user["id"], "name": user["first_name"], "email": user["email"]}
                for user in users_data
            ]
            return users
        except Exception as e:
            logging.error(f"Error while fetching users: {e}")
            return []

    def project_detail(self, project_id):
        """Fetch details of a specific project."""
        try:
            project_data = self._make_request("GET", f"/api/v1/projects/{project_id}")
            project_detail = {
                "id": project_data["single"]["id"],
                "name": project_data["single"]["name"],
                "members": project_data["single"]["members"]
            }
            return project_detail
        except Exception as e:
            logging.error(f"Error while fetching project details for {project_id}: {e}")
            return {}

    def add_note_in_project(self, project_id, note_title, note_content):
        """Add a note to a specific project."""
        data = {"name": note_title, "body": note_content}
        try:
            note_response = self._make_request(
                "POST", f"/api/v1/projects/{project_id}/notes", json=data
            )
            return self.host_url + note_response["single"]["url_path"]
        except Exception as e:
            logging.error(f"Error while adding note to project {project_id}: {e}")
            return None

    def add_task_in_project(self, project_id, task_title, task_description, task_assignee):
        """Add a task to a specific project."""
        data = {
            "name": task_title,
            "assignee_id": task_assignee,
            "body": task_description
        }
        try:
            task_response = self._make_request(
                "POST", f"/api/v1/projects/{project_id}/tasks", json=data
            )
            return self.host_url + task_response["single"]["url_path"]
        except Exception as e:
            logging.error(f"Error while adding task to project {project_id}: {e}")
            return None
