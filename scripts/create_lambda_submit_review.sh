#!/bin/bash

# Check if the Lambda function already exists
if aws lambda get-function --function-name submit_review >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

# Get the IAM role ARN for Lambda
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Create a temporary directory for packaging the Lambda function
PACKAGE_DIR=$(mktemp -d)
echo "Created temporary directory: $PACKAGE_DIR"

# Copy the Lambda function code to the package directory
cp submit_review.py $PACKAGE_DIR/

# Install the necessary MySQL dependency into the package directory
pip install mysql-connector-python -t $PACKAGE_DIR/

# Create the deployment package (ZIP file) in the current directory
cd $PACKAGE_DIR
zip -r submit_review.zip .
mv submit_review.zip ..
cd ..

# Clean up the temporary directory
rm -rf $PACKAGE_DIR

# Create the Lambda function
aws lambda create-function --function-name submit_review \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://submit_review.zip \
  --handler submit_review.lambda_handler

# Wait for the function to become active
aws lambda wait function-active --function-name submit_review

# Publish a new version of the function
aws lambda publish-version --function-name submit_review

echo "Lambda function 'submit_review' created and published successfully."
