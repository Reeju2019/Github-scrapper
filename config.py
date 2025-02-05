# config.py

class Config:
    """
    Configuration settings for the GitHub scraper and database.
    """
    MAX_REPOS_PER_USER = 100  # Maximum number of repositories to scrape per user
    MAX_FILES_PER_REPO = 100  # Maximum number of files to scrape per repository
    GITHUB_API_URL = "https://api.github.com"

    # AWS DynamoDB Configuration
    AWS_REGION = "eu-north-1"  # Replace with your preferred region
    DYNAMODB_TABLE = "github_code"