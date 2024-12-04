import boto3
import sys
import time

# Initialize API Gateway, Lambda, Cognito, and IAM clients
client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam')
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# Check if the API already exists
response = client.get_rest_apis()
apis = response.get('items', [])

for api in apis:
    if api.get('name') == 'MoraviYum_API':
        print('API already exists')
        sys.exit(0)

# Create the API
response = client.create_rest_api(
    name='MoraviYum_API',
    description='API for MoraviYum Food Review App.',
    endpointConfiguration={
        'types': ['REGIONAL']
    }
)
api_id = response["id"]

# Get the root resource ID
resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# Reusable IAM role ARN
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

def create_resource_and_method(resource_path, http_method, lambda_function_name):
    """
    Helper function to create a resource, define its method, and set Lambda integration.
    """
    # Create resource
    resource = client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart=resource_path
    )
    resource_id = resource["id"]

    # Define method
    method = client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=http_method,
        authorizationType='NONE'
    )

    # Set the method response
    method_response = client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=http_method,
        statusCode='200',
        responseParameters={
            'method.response.header.Access-Control-Allow-Headers': True,
            'method.response.header.Access-Control-Allow-Origin': True,
            'method.response.header.Access-Control-Allow-Methods': True
        },
        responseModels={
            'application/json': 'Empty'
        }
    )

    # Get Lambda ARN
    lambda_arn = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']
    uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

    # Set Lambda integration
    integration = client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=http_method,
        credentials=lab_role,
        integrationHttpMethod='POST',
        type='AWS_PROXY',
        uri=uri
    )

# Create and integrate the "fetch_vendor_foods" resource
create_resource_and_method('fetch_vendor_foods', 'GET', 'fetch_vendor_foods')

# Create and integrate the "get_reviews" resource
create_resource_and_method('get_reviews', 'GET', 'get_reviews')

# Create and integrate the "get_user_handle" resource
create_resource_and_method('get_user_handle', 'GET', 'get_user_handle')

# Create and integrate the "menu" resource
create_resource_and_method('menu', 'GET', 'menu')

# Create and integrate the "submit_review" resource
create_resource_and_method('submit_review', 'POST', 'submit_review')

# Create and integrate the "review" resource
create_resource_and_method('review', 'GET', 'review')

# Create and integrate the "store_user_handle" resource
create_resource_and_method('store_user_handle', 'POST', 'store_user_handle')

print("DONE")
print(f"API Gateway ID: {api_id}")
