# scraper.py


import requests
from typing import List, Dict, Optional
from config import Config

class GitHubScraper:
    """
    Scrapes code from GitHub repositories.
    """

    def __init__(self):
        """
        Initializes the GitHub scraper with necessary headers.
        """
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }


    def get_user_repos(self, username: str) -> List[Dict]:
        """
        Fetches repositories for a given GitHub user.

        Args:
            username (str): The GitHub username.

        Returns:
            List[Dict]: A list of repositories.
        """
        url = f"{Config.GITHUB_API_URL}/users/{username}/repos"
        response = requests.get(url, headers=self.headers, params={"per_page": Config.MAX_REPOS_PER_USER})
        
        # Debugging: Print the API response
        print("API Response:", response.json())
        
        return response.json()


    def get_repo_files(self, owner: str, repo: str) -> List[Dict]:
        """
        Fetches files from a GitHub repository.

        Args:
            owner (str): The owner of the repository.
            repo (str): The name of the repository.

        Returns:
            List[Dict]: A list of files in the repository.
        """
        url = f"{Config.GITHUB_API_URL}/repos/{owner}/{repo}/contents"
        response = requests.get(url, headers=self.headers, params={"per_page": Config.MAX_FILES_PER_REPO}, timeout=10)
        return response.json()

    def get_file_content(self, file_url: str) -> Optional[str]:
        """
        Fetches the content of a file from GitHub.

        Args:
            file_url (str): The URL of the file.

        Returns:
            Optional[str]: The content of the file, or None if the file is not a text file.
        """
        response = requests.get(file_url, headers=self.headers)
        if response.status_code == 200 and "text" in response.headers.get("Content-Type", ""):
            return response.text
        return None