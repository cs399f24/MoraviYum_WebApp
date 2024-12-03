import json

def lambda_handler(event, context):
    """
    Lambda function to extract and return the 'user_handle' from the incoming request payload.
    """
    # Default response
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
        # Parse the JSON body from the event
        body = json.loads(event.get('body', '{}'))
        user_handle = body.get('user_handle')

        # Validate the user_handle
        if not user_handle:
            raise ValueError("Missing 'user_handle' in the request payload.")

        # Log and return the user_handle
        print(f"Received user_handle: {user_handle}")
        response['statusCode'] = 200
        response['body'] = json.dumps({"user_handle": user_handle})

    except Exception as e:
        # Handle exceptions and include the error message in the response
        response['body'] = json.dumps({"error": str(e)})

    return response
