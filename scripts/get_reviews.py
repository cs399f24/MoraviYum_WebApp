import json
import boto3
import mysql.connector

# Initialize RDS Data API client
rds_client = boto3.client('rds-data', region_name='us-east-1')

def get_secret(secret_name):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')
    
    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        # Secrets Manager stores the value as a JSON string, parse it
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def lambda_handler(event, context):
    """
    Lambda function to fetch all reviews from the 'reviews' table.
    """
    secrets = get_secret("prod/moraviyum/rds-new")
    
# Retrieve DB credentials from Secrets Manager
    DB_HOST = secrets.get("host")
    DB_NAME = secrets.get("dbname")
    DB_USERNAME = secrets.get("username")
    DB_PASSWORD = secrets.get("password")
    
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
        # Connect to the RDS instance
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, food_id, rating, review, time_stamp FROM reviews;")
        reviews = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Prepare response
        response['statusCode'] = 200
        response['body'] = json.dumps(reviews, default=str)
    
    except Exception as e:
        print(f"Error: {e}")
        response['body'] = json.dumps({"error": str(e)})
    
    return response
import json
import boto3
import mysql.connector

# Initialize RDS Data API client
rds_client = boto3.client('rds-data', region_name='us-east-1')

def get_secret(secret_name):
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')
    
    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        # Secrets Manager stores the value as a JSON string, parse it
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def lambda_handler(event, context):
    """
    Lambda function to fetch all reviews from the 'reviews' table.
    """
    secrets = get_secret("prod/moraviyum/rds-new")
    
# Retrieve DB credentials from Secrets Manager
    DB_HOST = secrets.get("host")
    DB_NAME = secrets.get("dbname")
    DB_USERNAME = secrets.get("username")
    DB_PASSWORD = secrets.get("password")
    
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
        # Connect to the RDS instance
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, food_id, rating, review, time_stamp FROM reviews;")
        reviews = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Prepare response
        response['statusCode'] = 200
        response['body'] = json.dumps(reviews, default=str)
    
    except Exception as e:
        print(f"Error: {e}")
        response['body'] = json.dumps({"error": str(e)})
    
    return response
