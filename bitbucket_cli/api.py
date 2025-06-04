import requests
import json

class BitbucketAPI:
    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = 'https://api.bitbucket.org/2.0'

def obtain_access_token(self, authorization_code):
    # Exchange authorization code for access token
    token_url = 'https://bitbucket.org/site/oauth2/access_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'https://localhost:3000/callback',
        'client_id': self.client_id,
        'client_secret': self.client_secret
    }
    response = requests.post(token_url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
    
    if response.status_code == 200:
        self.access_token = response.json()['access_token']
        print(f"Access token obtained: {self.access_token}")
    else:
        print(f"Failed to obtain access token: {response.text}")

    def create_repository(self, project_key, repo_name, is_private=True):
        # Example of using the access token for API calls
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'scm': 'git',
            'project': {'key': project_key},
            'name': repo_name,
            'is_private': is_private
        }
        response = requests.post(f'{self.base_url}/repositories', headers=headers, json=data)
        if response.status_code == 201:
            print(f"Repository {repo_name} created successfully.")
        else:
            print(f"Failed to create repository: {response.text}")

    # Implement other methods similarly

