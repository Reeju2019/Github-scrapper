# main.py

from scraper import GitHubScraper
from database import Database
from config import Config

def main():
    """
    Main function to scrape GitHub code and store it in the database.
    """
    scraper = GitHubScraper()
    db = Database()

    # Example: Scrape repositories for a specific user
    username = "reeju2019"
    repos = scraper.get_user_repos(username)

    for repo in repos:
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        files = scraper.get_repo_files(owner, repo_name)

        for file in files:
            if file["type"] == "file":
                file_content = scraper.get_file_content(file["download_url"])
                if file_content:
                    # Save the file content to the database
                    key = f"{owner}/{repo_name}/{file['name']}"
                    db.save_code(key, file_content)
                    print(f"Saved: {key}")

if __name__ == "__main__":
    main()