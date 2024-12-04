import boto3
import sys

# Initialize API Gateway and Cognito clients
apigateway_client = boto3.client('apigateway', region_name='us-east-1')
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# API name and user pool name
api_name = "MoraviYum_API"
authorizer_name = "moraviyum_user_pool_authorizer"
user_pool_name = "moraviyum_user_pool"

def get_api_id(api_name):
    """
    Retrieve the API ID for the given API name.
    """
    apis = apigateway_client.get_rest_apis().get('items', [])
    for api in apis:
        if api.get('name') == api_name:
            return api['id']
    print(f"Error: API '{api_name}' not found.")
    sys.exit(1)

def get_user_pool_arn(user_pool_name):
    """
    Retrieve the ARN for the given Cognito User Pool.
    """
    user_pools = cognito_client.list_user_pools(MaxResults=10)['UserPools']
    for pool in user_pools:
        if pool['Name'] == user_pool_name:
            account_id = boto3.client('sts').get_caller_identity()['Account']
            return f"arn:aws:cognito-idp:us-east-1:{account_id}:userpool/{pool['Id']}"
    print(f"Error: User pool '{user_pool_name}' not found.")
    sys.exit(1)

def create_authorizer(api_id, authorizer_name, user_pool_arn):
    """
    Create a Cognito User Pool Authorizer for the given API.
    """
    response = apigateway_client.create_authorizer(
        restApiId=api_id,
        name=authorizer_name,
        type="COGNITO_USER_POOLS",
        providerARNs=[user_pool_arn],
        identitySource="method.request.header.Authorization"
    )
    return response

def main():
    # Step 1: Get API ID
    api_id = get_api_id(api_name)
    
    # Step 2: Get Cognito User Pool ARN
    user_pool_arn = get_user_pool_arn(user_pool_name)

    # Step 3: Create Authorizer
    print(f"Creating authorizer '{authorizer_name}' for API '{api_name}'...")
    authorizer = create_authorizer(api_id, authorizer_name, user_pool_arn)
    
    print("DONE")
    print(f"API Gateway ID: {api_id}")
    print(f"API Gateway Authorizer ID: {authorizer['id']}")
    print(f"Using Cognito User Pool ARN: {user_pool_arn}")

if __name__ == "__main__":
    main()
