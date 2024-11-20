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
s3_client.put_bucket_acl(Bucket=s3_bucket_name, ACL='private')
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

print("Bucket created with specified configurations.")