import boto3
import sys
import time
from botocore.exceptions import ClientError

# Initialize API Gateway client
client = boto3.client('apigateway', region_name='us-east-1')

# Check if the API exists
response = client.get_rest_apis()
apis = response.get('items', [])

api_id = None
for api in apis:
    if api.get('name') == 'MoraviYum_API':
        api_id = api.get('id')
        print(f"Found API with ID: {api_id}")
        break

if not api_id:
    print("Error: API 'MoraviYum_API' not found.")
    sys.exit(1)

# Get all resources and delete them, excluding the root resource
resources = client.get_resources(restApiId=api_id)
for resource in resources.get('items', []):
    resource_id = resource['id']
    
    # Skip deleting the root resource
    if resource['path'] == '/':
        continue

    try:
        # Try to delete the resource
        print(f"Attempting to delete resource with ID: {resource_id}")
        
        # Double check if the resource exists before attempting deletion
        resource_check = client.get_resource(restApiId=api_id, resourceId=resource_id)
        
        # If resource exists, proceed with deletion
        if resource_check:
            client.delete_resource(restApiId=api_id, resourceId=resource_id)
            print(f"Deleted resource with ID: {resource_id}")
        time.sleep(1)  # Add a 1-second delay between deletions
    except ClientError as e:
        if e.response['Error']['Code'] == 'TooManyRequestsException':
            print("Too many requests. Retrying...")
            time.sleep(5)  # Add a longer delay before retrying the deletion
        elif e.response['Error']['Code'] == 'NotFoundException':
            # If resource not found, skip it
            print(f"Resource with ID {resource_id} not found. Skipping...")
        else:
            print(f"Error deleting resource with ID {resource_id}: {e}")

# Delete the API itself
try:
    client.delete_rest_api(restApiId=api_id)
    print(f"API 'MoraviYum_API' with ID {api_id} deleted successfully.")
except ClientError as e:
    if e.response['Error']['Code'] == 'TooManyRequestsException':
        print("Too many requests. Retrying deletion of the API...")
        time.sleep(5)  # Add a delay before retrying the API deletion
        client.delete_rest_api(restApiId=api_id)
        print(f"API 'MoraviYum_API' with ID {api_id} deleted successfully after retry.")
    else:
        print(f"Error deleting API with ID {api_id}: {e}")
