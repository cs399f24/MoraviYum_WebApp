import boto3
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Get bucket name from environment variables
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

# Initialize the S3 client
s3_client = boto3.client('s3')

# Initialize the S3 resource (for object iteration)
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(s3_bucket_name)

# Delete all objects in the bucket
print(f"Deleting all objects in the bucket '{s3_bucket_name}'...")
bucket.object_versions.delete()  # Deletes both current and versioned objects
print("All objects deleted.")

# Delete the bucket
print(f"Deleting the bucket '{s3_bucket_name}'...")
s3_client.delete_bucket(Bucket=s3_bucket_name)
print(f"Bucket '{s3_bucket_name}' deleted successfully.")

