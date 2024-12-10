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
    # Split the resource_path into parts (e.g., 'menu/{vendor}' -> ['menu', '{vendor}'])
    path_parts = resource_path.split('/')
    
    # Initialize parentId as root_id
    parent_id = root_id

    # Create resources for each path part
    for path_part in path_parts:
        # Check if the resource already exists under the current parent
        resources = client.get_resources(restApiId=api_id)['items']
        existing_resource = next(
            (res for res in resources if 'pathPart' in res and res['pathPart'] == path_part and res['parentId'] == parent_id),
            None
        )

        if existing_resource:
            # If the resource already exists, get its ID
            parent_id = existing_resource['id']
        else:
            # Create the resource
            resource = client.create_resource(
                restApiId=api_id,
                parentId=parent_id,
                pathPart=path_part
            )
            parent_id = resource["id"]

    # Define method for the resource (GET, POST, etc.)
    client.put_method(
        restApiId=api_id,
        resourceId=parent_id,
        httpMethod=http_method,
        authorizationType='NONE'  # Modify if you use authorization
    )

    # Set the method response for CORS headers (if needed)
    client.put_method_response(
        restApiId=api_id,
        resourceId=parent_id,
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

    # Set the Lambda integration for the method
    client.put_integration(
        restApiId=api_id,
        resourceId=parent_id,
        httpMethod=http_method,
        credentials=lab_role,  # The IAM role that API Gateway assumes to invoke Lambda
        integrationHttpMethod='POST',
        type='AWS_PROXY',
        uri=uri
    )

def deploy_api(stage_name):
    """
    Deploy the API Gateway to the specified stage.
    """
    client.create_deployment(
        restApiId=api_id,
        stageName=stage_name,
        description=f"Deployment for {stage_name} stage."
    )
    print(f"API deployed to stage: {stage_name}")

# Create and integrate the "menu/{vendor}" resource with dynamic vendor path
create_resource_and_method('menu/{vendor}', 'GET', 'menu')

# Create and integrate the "get_reviews" resource
create_resource_and_method('get_reviews', 'GET', 'get_reviews')

# Create and integrate the "submit_review" resource
create_resource_and_method('submit_review', 'POST', 'submit_review')

# Deploy the API to a stage (e.g., 'prod' stage)
deploy_api('prod')

print("DONE")
print(f"API Gateway ID: {api_id}")
