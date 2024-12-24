import requests

class ArtifactoryClient:
    def __init__(self, base_url, token):
        """
        Initializes the ArtifactoryClient with the base URL and authentication token.

        Args:
            base_url (str): The base URL of the Artifactory
            token (str): Authentication token accessing the API.
        """
        self.base_url= base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    @staticmethod
    def prompt_for_token():
        """
        Prompts the user for their authentication token.

        Returns:
            str: The entered token.
        """
        return input("Enter your Artifactory authentication token: ")

    def ping(self):
        url = f"{base_url}/api/system/ping"
        response = self.session.get(url)
        return response.text

    def get_version(self):
        url = f"{base_url}/api/system/version"
        response = self.session.get(url)
        return response.json()

    def create_user(self, username, email):
        url = f"{base_url}/api/security/users/{username}"
        payload = {
            "email": email,
            "password": "defaultPassword123",
            "admin": False
        }
        response = self.session.put(url, json=payload)
        return response.json()

    def delete_user(self, username):
        url = f"{base_url}/api/security/users/{username}"
        response = self.session.delete(url)
        return response.status_code

    def list_repositories(self):
        url = f"{base_url}/api/repositories"
        response = self.session.get(url)
        return response.json()
