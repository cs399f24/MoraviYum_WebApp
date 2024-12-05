import json
import boto3
import mysql.connector

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
    Lambda function to fetch vendor foods based on query parameters.
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
        # Get query parameters
        vendor_name = event['queryStringParameters'].get('vendor', None)
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
        
        cursor = connection.cursor(dictionary=True)
        
        # SQL query to fetch vendor foods
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
                f.vendor = %s;
        """
        
        cursor.execute(sql_query, (vendor_name,))
        rows = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        connection.close()
        
        # Parse records into food list
        foods = [
            {
                "food_name": row['food_name'],
                "food_id": row['food_id'],
                "price": row['price'],
                "calories": row['calories'],
                "avg_rating": row['avg_rating'],
                "image_url": row['image_url'] if row['image_url'] else None
            }
            for row in rows
        ]
        
        # Update response
        response['statusCode'] = 200
        response['body'] = json.dumps(foods)

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        response['body'] = json.dumps({"error": f"MySQL error: {str(e)}"})
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        response['body'] = json.dumps({"error": f"Unexpected error: {str(e)}"})
    
    return response
