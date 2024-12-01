import boto3
import dotenv
import os

dotenv.load_dotenv()
AMPLIFY_DOMAIN = os.getenv('AMPLIFY_DOMAIN')
API_GATEWAYURL = os.getenv('API_GATEWAYURL')
USER_EMAIL = os.getenv('USER_EMAIL')
NEW_USERNAME = os.getenv('NEW_USERNAME')
TEMP_PASS = os.getenv('TEMP_PASS')

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# Create a user pool
response = cognito_client.create_user_pool(
    PoolName='moraviyum_user_pool',
    Policies={
        'PasswordPolicy': {
            'MinimumLength': 8,
            'RequireUppercase': True,
            'RequireLowercase': True,
            'RequireNumbers': True,
            'RequireSymbols': True,
            'TemporaryPasswordValidityDays': 7
        }
    },
    AutoVerifiedAttributes=['email'],  # Email is auto-verified
    AliasAttributes=[],  # No aliases enabled
    UsernameAttributes=[],  # Username-based authentication
    UsernameConfiguration={
        'CaseSensitive': True
    },
    AccountRecoverySetting={
        'RecoveryMechanisms': [
            {'Priority': 1, 'Name': 'verified_email'}  # Recovery via email
        ]
    }
)

user_pool_id = response['UserPool']['Id']
print(f"Created User Pool with ID: {user_pool_id}")


# Create an app client
app_client_response = cognito_client.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName='moraviyum_app_client',
    GenerateSecret=False,  # Public client
    AllowedOAuthFlows=['implicit'],
    AllowedOAuthScopes=['email', 'openid'],
    AllowedOAuthFlowsUserPoolClient=True,
    CallbackURLs=[f'{AMPLIFY_DOMAIN}/callback.html'],
    LogoutURLs=[f'{AMPLIFY_DOMAIN}/review.html'],
    ExplicitAuthFlows=[
        'ALLOW_REFRESH_TOKEN_AUTH',
        'ALLOW_CUSTOM_AUTH',
        'ALLOW_USER_SRP_AUTH',
        'ALLOW_USER_PASSWORD_AUTH'
    ]
)

app_client_id = app_client_response['UserPoolClient']['ClientId']
print(f"Created App Client with ID: {app_client_id}")


# Configure a domain for the hosted UI
cognito_client.create_user_pool_domain(
    Domain='moraviyum-cloud-computing',
    UserPoolId=user_pool_id
)
print("Hosted UI domain configured")


# Create a resource server
resource_server_response = cognito_client.create_resource_server(
    UserPoolId=user_pool_id,
    Identifier=f'{API_GATEWAYURL}/prod/review',
    Name='moraviyum_resource_server',
    Scopes=[
        {'ScopeName': 'review', 'ScopeDescription': 'Access to review page'}
    ]
)

print("Resource server created")

# Add a new user to the User Pool
new_user_email = USER_EMAIL
new_user_username = NEW_USERNAME
try:
    new_user_response = cognito_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=new_user_username,
        UserAttributes=[
            {'Name': 'email', 'Value': new_user_email},
            {'Name': 'email_verified', 'Value': 'true'}  # Set email as verified
        ],
        TemporaryPassword=TEMP_PASS,  # User must change this password on first login
        MessageAction='SUPPRESS'  # Don't send invitation email
    )
    print(f"Added new user with username: {new_user_username}")
except Exception as e:
    print(f"Error adding new user: {e}")