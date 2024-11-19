import pymysql
import os
import json
import uuid
import time

# Configuration for RDS
RDS_HOST = os.getenv('RDS_HOST')
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DB = os.getenv('RDS_DB')


def lambda_handler(event, context):
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')

    if path == '/get_reviews' and http_method == 'GET':
        return get_reviews()

    elif path == '/fetch_vendor_foods' and http_method == 'GET':
        vendor_name = event['queryStringParameters'].get('vendor', None)
        if vendor_name:
            return fetch_vendor_foods(vendor_name)
        else:
            return response(400, {"error": "Vendor name is required"})

    elif path == '/submit_review' and http_method == 'POST':
        body = json.loads(event['body'])
        return submit_review(body)

    else:
        return response(404, {"error": "Endpoint not found"})


def connect_to_rds():
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to RDS: {e}")
        raise


def get_reviews():
    try:
        connection = connect_to_rds()
        with connection.cursor() as cursor:
            query = "SELECT user_id, food_id, rating, review, time_stamp FROM reviews"
            cursor.execute(query)
            reviews = cursor.fetchall()
        connection.close()
        return response(200, reviews)
    except Exception as e:
        return response(500, {"error": str(e)})


def fetch_vendor_foods(vendor_name):
    try:
        connection = connect_to_rds()
        with connection.cursor() as cursor:
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
                    f.vendor = %s
            """
            cursor.execute(query, (vendor_name,))
            foods = cursor.fetchall()
        connection.close()
        return response(200, foods)
    except Exception as e:
        return response(500, {"error": str(e)})


def submit_review(body):
    try:
        user_id = body.get('user_id')
        food = body.get('food')
        rating = body.get('rating')
        review_text = body.get('review')

        if not all([user_id, food, rating, review_text]):
            return response(400, {"error": "All fields (user_id, food, rating, review) are required"})

        connection = connect_to_rds()
        with connection.cursor() as cursor:
            query = """
                INSERT INTO reviews (review_id, user_id, food_id, rating, review, time_stamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (str(uuid.uuid4()), user_id, food, int(rating), review_text, int(time.time())))
            connection.commit()
        connection.close()
        return response(200, {"message": "Review submitted successfully!"})
    except Exception as e:
        return response(500, {"error": str(e)})


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
