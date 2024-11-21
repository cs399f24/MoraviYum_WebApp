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
    description='API for food review app.',
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

# Get the ARN for the "fetchVendorFoods" lambda function
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='fetchVendorFoods')['Configuration']['FunctionArn']
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

# Create "fetch_all_vendors" resource
fetch_all_vendors = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='fetch_all_vendors'
)
fetch_all_vendors_resource_id = fetch_all_vendors["id"]

# Define the GET method for "fetch_all_vendors"
fetch_all_vendors_method = client.put_method(
    restApiId=api_id,
    resourceId=fetch_all_vendors_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# Set the method response for "fetch_all_vendors"
fetch_all_vendors_response = client.put_method_response(
    restApiId=api_id,
    resourceId=fetch_all_vendors_resource_id,
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

# Get the ARN for the "fetchAllVendors" lambda function
lambda_arn = lambda_client.get_function(FunctionName='fetchAllVendors')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set the integration for "fetch_all_vendors"
fetch_all_vendors_integration = client.put_integration(
    restApiId=api_id,
    resourceId=fetch_all_vendors_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create "add_food_item" resource
add_food_item = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='add_food_item'
)
add_food_item_resource_id = add_food_item["id"]

# Define the POST method for "add_food_item"
add_food_item_method = client.put_method(
    restApiId=api_id,
    resourceId=add_food_item_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

# Set the method response for "add_food_item"
add_food_item_response = client.put_method_response(
    restApiId=api_id,
    resourceId=add_food_item_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the "addFoodItem" lambda function
lambda_arn = lambda_client.get_function(FunctionName='addFoodItem')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set the integration for "add_food_item"
add_food_item_integration = client.put_integration(
    restApiId=api_id,
    resourceId=add_food_item_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create "update_food_item" resource
update_food_item = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='update_food_item'
)
update_food_item_resource_id = update_food_item["id"]

# Define the PUT method for "update_food_item"
update_food_item_method = client.put_method(
    restApiId=api_id,
    resourceId=update_food_item_resource_id,
    httpMethod='PUT',
    authorizationType='NONE'
)

# Set the method response for "update_food_item"
update_food_item_response = client.put_method_response(
    restApiId=api_id,
    resourceId=update_food_item_resource_id,
    httpMethod='PUT',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the "updateFoodItem" lambda function
lambda_arn = lambda_client.get_function(FunctionName='updateFoodItem')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set the integration for "update_food_item"
update_food_item_integration = client.put_integration(
    restApiId=api_id,
    resourceId=update_food_item_resource_id,
    httpMethod='PUT',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Create "delete_food_item" resource
delete_food_item = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='delete_food_item'
)
delete_food_item_resource_id = delete_food_item["id"]

# Define the DELETE method for "delete_food_item"
delete_food_item_method = client.put_method(
    restApiId=api_id,
    resourceId=delete_food_item_resource_id,
    httpMethod='DELETE',
    authorizationType='NONE'
)

# Set the method response for "delete_food_item"
delete_food_item_response = client.put_method_response(
    restApiId=api_id,
    resourceId=delete_food_item_resource_id,
    httpMethod='DELETE',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# Get the ARN for the "deleteFoodItem" lambda function
lambda_arn = lambda_client.get_function(FunctionName='deleteFoodItem')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Set the integration for "delete_food_item"
delete_food_item_integration = client.put_integration(
    restApiId=api_id,
    resourceId=delete_food_item_resource_id,
    httpMethod='DELETE',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

print("DONE")
