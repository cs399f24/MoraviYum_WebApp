import boto3
import dotenv
import os

dotenv.load_dotenv()
CALLBACKURL = os.getenv('CALLBACKURL')
LOGOUTURL = os.getenv('LOGOUTURL')
API_GATEWAYURL = os.getenv('API_GATEWAYURL')

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
    AllowedOAuthFlows=['implicit'],  # Enable implicit grant
    AllowedOAuthScopes=['email', 'openid'],  # Scopes
    AllowedOAuthFlowsUserPoolClient=True,
    CallbackURLs=[f'{CALLBACKURL}/callback.html'],
    LogoutURLs=[f'{LOGOUTURL}/review.html'],
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

# FIX THESE LATER
hosted_ui_url = f"https://moraviyum-cloud-computing.auth.us-east-1.amazoncognito.com/login?client_id={app_client_id}&response_type=token&scope=email+openid&redirect_uri=https://staging.d1u8wmi9k660nd.amplifyapp.com/callback.html"
print(f"Hosted UI URL: {hosted_ui_url}")