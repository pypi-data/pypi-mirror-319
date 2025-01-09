import requests
from base64 import b64encode

class GitHub:
    BASE_URL = "https://api.github.com"

    def __init__(self, access_token):
        if not access_token:
            raise ValueError("Access token must be provided.")
        self.access_token = access_token
        self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "details": response.json() if response.content else None}

    def get_user_info(self):
        response = self._make_request("GET", "/user")
        if "error" in response:
            print(f"Error fetching user info: {response['error']}")
            return None
        return response

    def list_repositories(self):
        return self._make_request("GET", "/user/repos")

    def create_repository(self, repo_name, private=True, description="", auto_init=True):
        data = {
            'name': repo_name,
            'private': private,
            'description': description,
            'auto_init': auto_init
        }
        response = self._make_request("POST", "/user/repos", data)
        if "error" in response:
            print(f"Error creating repository: {response['error']}")
            return None
        print(f"Repository '{repo_name}' created successfully.")
        return response

    def delete_repository(self, owner, repo):
        endpoint = f"/repos/{owner}/{repo}"
        response = self._make_request("DELETE", endpoint)
        if "error" in response:
            print(f"Error deleting repository: {response['error']}")
            return False
        print(f"Repository '{repo}' deleted successfully.")
        return True

    def create_issue(self, owner, repo, title, body=""):
        endpoint = f"/repos/{owner}/{repo}/issues"
        data = {
            'title': title,
            'body': body
        }
        response = self._make_request("POST", endpoint, data)
        if "error" in response:
            print(f"Error creating issue: {response['error']}")
            return None
        print(f"Issue '{title}' created successfully.")
        return response

    def list_issues(self, owner, repo):
        endpoint = f"/repos/{owner}/{repo}/issues"
        return self._make_request("GET", endpoint)

    def get_repository(self, owner, repo):
        endpoint = f"/repos/{owner}/{repo}"
        return self._make_request("GET", endpoint)

    def update_user_profile(self, name=None, bio=None, location=None):
        data = {key: value for key, value in {
            'name': name,
            'bio': bio,
            'location': location
        }.items() if value is not None}

        if not data:
            print("No data provided to update user profile.")
            return None

        response = self._make_request("PATCH", "/user", data)
        if "error" in response:
            print(f"Error updating profile: {response['error']}")
            return None
        print("Profile updated successfully.")
        return response

    def create_file(self, owner, repo, file_path, content, message):
        endpoint = f"/repos/{owner}/{repo}/contents/{file_path}"
        data = {
            'message': message,
            'content': b64encode(content.encode('utf-8')).decode('utf-8')
        }
        response = self._make_request("PUT", endpoint, data)
        if "error" in response:
            print(f"Error creating file: {response['error']}")
            return None
        print(f"File '{file_path}' created/updated successfully.")
        return response

    def get_available_licenses(self):
        response = self._make_request("GET", "/licenses")
        if "error" in response:
            print(f"Error fetching licenses: {response['error']}")
            return None
        return {license['spdx_id']: license['name'] for license in response}

    def get_gitignore_templates(self):
        return {
            'Python': "*.pyc\n__pycache__/\n",
            'Node': "node_modules/\n",
            'Java': "*.class\n*.jar\n",
            'Ruby': "*.gem\n*.rbc\n",
            'C++': "*.o\n*.out\n",
            'JavaScript': "node_modules/\n",
            'Visual Studio': "bin/\nobj/\n",
            'MacOS': ".DS_Store\n",
            'Windows': "Thumbs.db\n"
        }
