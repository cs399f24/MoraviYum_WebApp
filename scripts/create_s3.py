import boto3
import dotenv
import os

dotenv.load_dotenv()

s3_bucket_name = os.getenv('S3_BUCKET_NAME')

# Initialize the S3 client for us-east-1
s3_client = boto3.client('s3', region_name='us-east-1')

# Create the bucket (no LocationConstraint needed for us-east-1)
s3_client.create_bucket(Bucket=s3_bucket_name)
print(f"Bucket '{s3_bucket_name}' created successfully in us-east-1.")

# Update bucket ACL to disable ACLs (Object Ownership is defaulted to Bucket Owner Enforced)
print("Bucket ACLs disabled (private).")

# Turn off "Block all public access"
public_access_block_config = {
    'BlockPublicAcls': False,
    'IgnorePublicAcls': False,
    'BlockPublicPolicy': False,
    'RestrictPublicBuckets': False,
}
s3_client.put_public_access_block(
    Bucket=s3_bucket_name,
    PublicAccessBlockConfiguration=public_access_block_config
)
print("Public access settings updated (Block all public access turned off).")

# Set up bucket encryption
encryption_config = {
    'Rules': [
        {
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            },
            'BucketKeyEnabled': True
        }
    ]
}
s3_client.put_bucket_encryption(
    Bucket=s3_bucket_name,
    ServerSideEncryptionConfiguration=encryption_config
)
print("Bucket encryption enabled with Amazon S3 managed keys (SSE-S3).")

# Upload files from the templates folder
templates_folder = '../templates'
for file_name in os.listdir(templates_folder):
    file_path = os.path.join(templates_folder, file_name)
    try:
        s3_client.upload_file(file_path, s3_bucket_name, file_name)
        print(f"Uploaded file '{file_name}' to bucket '{s3_bucket_name}'.")
    except Exception as e:
        print(f"Failed to upload file '{file_name}': {e}")

# Upload files from the static folder
static_folder = '../static'
for file_name in os.listdir(static_folder):
    file_path = os.path.join(static_folder, file_name)
    try:
        s3_client.upload_file(file_path, s3_bucket_name, f"static/{file_name}")
        print(f"Uploaded file '{file_name}' to bucket '{s3_bucket_name}/static/'.")
    except Exception as e:
        print(f"Failed to upload file '{file_name}': {e}")

# Upload images from the images folder
images_folder = '../images'
for file_name in os.listdir(images_folder):
    file_path = os.path.join(images_folder, file_name)
    try:
        s3_client.upload_file(file_path, s3_bucket_name, {file_name})
        print(f"Uploaded image '{file_name}' to bucket '{s3_bucket_name}/'.")
    except Exception as e:
        print(f"Failed to upload image '{file_name}': {e}")

print("All files uploaded successfully.")