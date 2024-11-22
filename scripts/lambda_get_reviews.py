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
    Lambda function to fetch all reviews from the 'reviews' table.
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
        # SQL query to fetch all reviews
        sql_query = """
            SELECT 
                user_id, 
                food_id, 
                rating, 
                review, 
                time_stamp 
            FROM 
                reviews;
        """

        # Execute SQL query using the RDS Data API
        query_result = rds_client.execute_statement(
            resourceArn=DB_CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=RDS_DB_NAME,
            sql=sql_query
        )

        # Parse records from the query result
        records = query_result.get('records', [])
        reviews = [
            {
                "user_id": row[0]['stringValue'],
                "food_id": row[1]['stringValue'],
                "rating": row[2]['doubleValue'],
                "review": row[3]['stringValue'],
                "time_stamp": row[4]['stringValue']
            }
            for row in records
        ]

        # Update response
        response['statusCode'] = 200
        response['body'] = json.dumps(reviews)

    except Exception as e:
        response['body'] = json.dumps({"error": str(e)})

    return response
