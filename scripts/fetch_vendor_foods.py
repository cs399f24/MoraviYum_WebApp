import json
import mysql.connector
import boto3

# Initialize Secrets Manager and RDS Data API client
def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def lambda_handler(event, context):
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
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps({"error": "Internal server error"})
    }

    try:
        # Parse query parameters
        vendor_name = event.get("queryStringParameters", {}).get("vendor")
        if not vendor_name:
            response['statusCode'] = 400
            response['body'] = json.dumps({"error": "Vendor name is required"})
            return response

        # Connect to the RDS instance
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        # Perform the query
        cursor = connection.cursor(dictionary=True)
        query = """
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
            f.vendor = %s;
        """
        cursor.execute(query, (vendor_name,))
        rows = cursor.fetchall()
        
        # Format the response
        response['statusCode'] = 200
        response['body'] = json.dumps(rows, default=str)

        # Close the connection
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")
        response['body'] = json.dumps({"error": str(e)})
    
    return response
