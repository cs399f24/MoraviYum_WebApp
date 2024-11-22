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
    Lambda function to submit a food review.
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
        user_id = body.get('user_id')
        food_id = body.get('food')
        rating = body.get('rating')
        review_text = body.get('review')

        # Validate input
        if not all([user_id, food_id, rating, review_text]):
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Missing required fields"})
            return response

        # SQL query for inserting the review
        sql_query = """
            INSERT INTO reviews (user_id, food_id, rating, review)
            VALUES (:user_id, :food_id, :rating, :review_text);
        """

        # Execute SQL query
        rds_client.execute_statement(
            resourceArn=DB_CLUSTER_ARN,
            secretArn=SECRET_ARN,
            database=RDS_DB_NAME,
            sql=sql_query,
            parameters=[
                {'name': 'user_id', 'value': {'stringValue': user_id}},
                {'name': 'food_id', 'value': {'stringValue': food_id}},
                {'name': 'rating', 'value': {'longValue': int(rating)}},
                {'name': 'review_text', 'value': {'stringValue': review_text}}
            ]
        )

        # Update response
        response['statusCode'] = 200
        response['body'] = json.dumps({"message": "Review submitted successfully!"})

    except Exception as e:
        # Update response with error details
        response['body'] = json.dumps({"error": str(e)})

    return response
