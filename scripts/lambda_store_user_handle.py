import json
import boto3
import os

# Initialize RDS Data API client
rds_client = boto3.client('rds-data', region_name='us-east-1')

# Database and secret configuration
DB_CLUSTER_ARN = os.getenv('DB_CLUSTER_ARN')
SECRET_ARN = os.getenv('SECRET_ARN')
RDS_DB_NAME = os.getenv('RDS_DB_NAME')

def lambda_handler(event, context):
    """
    Lambda function to store user handle in the database.
    """
    # Initialize response template
    response = {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "POST",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps({"error": "Internal server error"})
    }

    try:
        # Parse request body
        body = json.loads(event['body'])
        user_handle = body.get('user_handle')

        # Validate input
        if not user_handle:
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Missing user_handle"})
            return response

        # SQL query to insert user_handle
        sql_query = """
            INSERT INTO usernames (user_handle)
            VALUES (:user_handle);
        """

        # Execute SQL query
        rds_client.execute_statement(
            resourceArn=DB_CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=RDS_DB_NAME,
            sql=sql_query,
            parameters=[
                {'name': 'user_handle', 'value': {'stringValue': user_handle}}
            ]
        )

        # Update response for successful insertion
        response['statusCode'] = 200
        response['body'] = json.dumps({
            "message": "User handle stored successfully!",
            "redirect_url": f"/review?user_handle={user_handle}"
        })

    except Exception as e:
        # Update response with error details
        response['body'] = json.dumps({"error": str(e)})

    return response
