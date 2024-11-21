import json
import boto3
import os

# Initialize RDS Data API client
rds_client = boto3.client('rds-data', region_name='us-east-1')

# Database and secret configuration
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']
SECRET_ARN = os.environ['SECRET_ARN']
RDS_DB_NAME = os.environ['RDS_DB_NAME']

def lambda_handler(event, context):
    """
    Lambda function to fetch vendor foods based on query parameters.
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
        # Get query parameters
        vendor_name = event['queryStringParameters'].get('vendor', None)
        if not vendor_name:
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Vendor name is required"})
            return response

        # SQL query
        sql_query = """
            SELECT 
                f.food_name, 
                f.food_id, 
                f.price, 
                f.calories, 
                f.avg_rating, 
                i.image_url
            FROM 
                foods f
            LEFT JOIN 
                images i ON f.food_id = i.food_id
            WHERE 
                f.vendor = :vendor_name;
        """

        # Execute SQL query
        query_result = rds_client.execute_statement(
            resourceArn=DB_CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=RDS_DB_NAME,
            sql=sql_query,
            parameters=[
                {'name': 'vendor_name', 'value': {'stringValue': vendor_name}}
            ]
        )

        # Parse records
        records = query_result.get('records', [])
        foods = [
            {
                "food_name": row[0]['stringValue'],
                "food_id": row[1]['stringValue'],
                "price": row[2]['doubleValue'],
                "calories": row[3]['longValue'],
                "avg_rating": row[4]['doubleValue'],
                "image_url": row[5].get('stringValue', None)
            }
            for row in records
        ]

        # Update response
        response['statusCode'] = 200
        response['body'] = json.dumps(foods)

    except Exception as e:
        response['body'] = json.dumps({"error": str(e)})

    return response
