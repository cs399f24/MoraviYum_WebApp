import json
import mysql.connector
import boto3

# Function to retrieve secrets from AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def lambda_handler(event, context):
    # Handle preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type",
                'Access-Control-Allow-Methods': "OPTIONS,POST,GET",
                'Access-Control-Allow-Origin': "*"
            }
        }
    
    # Retrieve database credentials from Secrets Manager
    secrets = get_secret("prod/moraviyum/rds-new")
    DB_HOST = secrets.get("host")
    DB_NAME = secrets.get("dbname")
    DB_USERNAME = secrets.get("username")
    DB_PASSWORD = secrets.get("password")

    # Initialize the response template
    response = {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type",
            'Access-Control-Allow-Methods': "OPTIONS,POST,GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps({"error": "Internal server error"})
    }

    try:
        # Parse request body and handle JSON string
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        user_id = body.get('user_id')
        food_id = body.get('food')
        rating = body.get('rating')
        review_text = body.get('review')

        # Validate required fields
        if not all([user_id, food_id, rating, review_text]):
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Missing required fields."})
            return response

        # Connect to the RDS instance
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        # Insert the review into the database
        cursor = connection.cursor()
        query = '''
            INSERT INTO reviews (user_id, food_id, rating, review)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (user_id, food_id, rating, review_text))
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()

        # Return success response
        response['statusCode'] = 200
        response['body'] = json.dumps({"message": "Review submitted successfully!"})
        response['headers'] = {
            'Access-Control-Allow-Headers': "Content-Type",
            'Access-Control-Allow-Methods': "OPTIONS,POST,GET",
            'Access-Control-Allow-Origin': "*"
        }

    except Exception as e:
        print(f"Error: {e}")
        response['body'] = json.dumps({"error": str(e)})

    return response