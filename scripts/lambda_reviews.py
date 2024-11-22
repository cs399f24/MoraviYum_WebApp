import json
from jinja2 import Environment, FileSystemLoader

def lambda_handler(event, context):
    # Configure Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("review.html")
    
    # Render the template
    user_handle = event.get('queryStringParameters', {}).get('user_handle', '')
    rendered_template = template.render(user_handle=user_handle)
    
    # Return the response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": rendered_template
    }