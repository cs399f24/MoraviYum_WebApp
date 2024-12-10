import boto3
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()
AMPLIFY_DOMAIN = os.getenv('AMPLIFY_DOMAIN')
APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
USER_POOL_ID = os.getenv('USER_POOL_ID')

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

try:
    # Update the app client with the new callback URL
    response = cognito_client.update_user_pool_client(
        UserPoolId=USER_POOL_ID,
        ClientId=APP_CLIENT_ID,
        CallbackURLs=[f'{AMPLIFY_DOMAIN}/callback.html']
    )
    print(f"Updated Callback URL for App Client ID {APP_CLIENT_ID}")
except Exception as e:
    print(f"Error updating Callback URL: {e}")