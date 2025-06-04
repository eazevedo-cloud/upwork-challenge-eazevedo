import base64
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class BitbucketAuth:
    def __init__(self):
        self.username = os.getenv("BITBUCKET_USERNAME")
        self.app_password = os.getenv("BITBUCKET_APP_PASSWORD")

    def get_headers(self):
        """
        Returns the authentication headers for Bitbucket API requests.
        """
        credentials = f"{self.username}:{self.app_password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
