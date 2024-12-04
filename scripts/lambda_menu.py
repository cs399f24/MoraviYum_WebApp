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
    Lambda function to fetch menu items for a specific vendor.
    """
    # Initialize response template
    response = {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps({"error": "Internal server error"})
    }

    try:
        # Extract vendor name from path parameters
        vendor = event['pathParameters'].get('vendor')
        if not vendor:
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Vendor name is required"})
            return response

        # SQL query to fetch menu items
        sql_query = """
            SELECT f.food_name, f.price, f.calories, i.image_url
            FROM foods f
            LEFT JOIN images i ON f.food_id = i.food_id
            WHERE f.vendor = :vendor;
        """

        # Execute SQL query
        result = rds_client.execute_statement(
            resourceArn=DB_CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=RDS_DB_NAME,
            sql=sql_query,
            parameters=[
                {'name': 'vendor', 'value': {'stringValue': vendor}}
            ]
        )

        # Format the results
        records = result.get('records', [])
        menu_list = [
            {
                'food_name': record[0].get('stringValue', None),
                'price': record[1].get('doubleValue', None),
                'calories': record[2].get('longValue', None),
                'image_url': record[3].get('stringValue', None)
            }
            for record in records
        ]

        # Successful response
        response['statusCode'] = 200
        response['body'] = json.dumps(menu_list)

    except Exception as e:
        # Update response with error details
        response['body'] = json.dumps({"error": str(e)})

    return response
