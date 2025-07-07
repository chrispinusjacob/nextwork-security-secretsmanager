# config.py — Secure version using AWS Secrets Manager
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = "aws-access-key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        raise

# ✅ Safely retrieve credentials from Secrets Manager
credentials = get_secret()

# ✅ Extract values with fallback for AWS_REGION
AWS_ACCESS_KEY_ID = credentials.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = credentials.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = credentials.get("AWS_REGION", boto3.session.Session().region_name or "us-east-1")
