#!/bin/bash

# Check if the Lambda function already exists
if aws lambda get-function --function-name store_user_handle >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

# Get the IAM role ARN for Lambda
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Create a temporary directory for packaging the Lambda function
PACKAGE_DIR=$(mktemp -d)
echo "Created temporary directory: $PACKAGE_DIR"

# Copy the Lambda function code to the package directory
cp store_user_handle.py $PACKAGE_DIR/

# Install the necessary MySQL dependency into the package directory
pip install mysql-connector-python -t $PACKAGE_DIR/

# Create the deployment package (ZIP file) in the current directory
cd $PACKAGE_DIR
zip -r store_user_handle.zip .
mv store_user_handle.zip ..
cd ..

# Clean up the temporary directory
rm -rf $PACKAGE_DIR

# Create the Lambda function
aws lambda create-function --function-name store_user_handle \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://store_user_handle.zip \
  --handler store_user_handle.lambda_handler

# Wait for the function to become active
aws lambda wait function-active --function-name store_user_handle

# Publish a new version of the function
aws lambda publish-version --function-name store_user_handle

echo "Lambda function 'store_user_handle' created and published successfully."
