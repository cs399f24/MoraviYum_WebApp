import boto3, json
import sys

client = boto3.client('apigateway', region_name='us-east-1')

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

# Create "fetch_vendor_foods" resource
fetch_vendor_foods = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='fetch_vendor_foods'
)
fetch_vendor_foods_resource_id = fetch_vendor_foods["id"]

# Define the GET method for "fetch_vendor_foods"
fetch_vendor_foods_method = client.put_method(
    restApiId=api_id,
    resourceId=fetch_vendor_foods_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# Set the method response for "fetch_vendor_foods"
fetch_vendor_foods_response = client.put_method_response(
    restApiId=api_id,
    resourceId=fetch_vendor_foods_resource_id,
    httpMethod='GET',
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

# Get the ARN for the "fetch_vendor_foods" lambda function
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='fetch_vendor_foods')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM role
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# Set the integration for "fetch_vendor_foods"
fetch_vendor_foods_integration = client.put_integration(
    restApiId=api_id,
    resourceId=fetch_vendor_foods_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create "get_reviews" resource
get_reviews = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='get_reviews'
)
get_reviews_resource_id = get_reviews["id"]

# Define the GET method for "get_reviews"
get_reviews_method = client.put_method(
    restApiId=api_id,
    resourceId=get_reviews_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# Set the method response for "get_reviews"
get_reviews_response = client.put_method_response(
    restApiId=api_id,
    resourceId=get_reviews_resource_id,
    httpMethod='GET',
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

# Get the ARN for the "get_reviews" lambda function
get_reviews_lambda_arn = lambda_client.get_function(FunctionName='get_reviews')['Configuration']['FunctionArn']
get_reviews_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{get_reviews_lambda_arn}/invocations'

# Set the integration for "get_reviews"
get_reviews_integration = client.put_integration(
    restApiId=api_id,
    resourceId=get_reviews_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=get_reviews_uri
)

print("DONE")
