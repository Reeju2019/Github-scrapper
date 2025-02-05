# database.py

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from config import Config

class Database:
    """
    Handles interactions with Amazon DynamoDB.
    """

    def __init__(self):
        """
        Initializes the DynamoDB connection.
        """
        self.client = boto3.client(
            "dynamodb",
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION,
        )
        self.table_name = Config.DYNAMODB_TABLE

    def save_code(self, key: str, code: str) -> None:
        """
        Saves code to DynamoDB with a unique key.

        Args:
            key (str): The unique identifier for the code.
            code (str): The code to be saved.
        """
        try:
            self.client.put_item(
                TableName=self.table_name,
                Item={
                    "Key": {"S": key},  # Primary key
                    "Code": {"S": code},  # Attribute for storing code
                },
            )
            print(f"Saved: {key}")
        except NoCredentialsError:
            print("AWS credentials not found.")
        except ClientError as e:
            error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
            print(f"Error saving to DynamoDB: {error_message}")

    def get_code(self, key: str) -> str:
        """
        Retrieves code from DynamoDB using a key.

        Args:
            key (str): The unique identifier for the code.

        Returns:
            str: The code associated with the key.
        """
        try:
            response = self.client.get_item(
                TableName=self.table_name,
                Key={"Key": {"S": key}},
            )
            if "Item" in response:
                return response["Item"]["Code"]["S"]
            return ""
        except NoCredentialsError:
            print("AWS credentials not found.")
            return ""
        except ClientError as e:
            error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
            print(f"Error retrieving from DynamoDB: {error_message}")
            return ""