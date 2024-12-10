#!/bin/bash

# Load environment variables
source .env

S3_BUCKET_NAME=$S3_BUCKET_NAME
AMPLIFY_APP_NAME="MoraviYumApp"
ENV_FILE_PATH=".env"

echo "Creating Amplify app..."

# Create Amplify app
AMPLIFY_APP_ID=$(aws amplify create-app \
  --name "$AMPLIFY_APP_NAME" \
  --platform WEB \
  --query 'app.appId' \
  --output text)

if [ -z "$AMPLIFY_APP_ID" ]; then
  echo "Error: Failed to create Amplify app."
  exit 1
fi

echo "Amplify app created with ID: $AMPLIFY_APP_ID"

echo "Linking S3 bucket to Amplify app..."
aws amplify create-branch \
    --app-id "$AMPLIFY_APP_ID" \
    --branch-name "prod" \
    --stage "PRODUCTION" \
    --enable-auto-build \
    --environment-variables S3_BUCKET="$S3_BUCKET"

if [ $? -ne 0 ]; then
    echo "Error: Failed to link S3 bucket to Amplify app."
    exit 1
fi

echo "S3 bucket linked to 'prod' branch."

# Get default domain for Amplify app
echo "Fetching Amplify app domain..."
AMPLIFY_DOMAIN=$(aws amplify get-app \
  --app-id "$AMPLIFY_APP_ID" \
  --query 'app.defaultDomain' \
  --output text)

if [ -z "$AMPLIFY_DOMAIN" ]; then
  echo "Error: Failed to fetch Amplify domain."
  exit 1
fi

echo "Amplify app deployed. Domain: $AMPLIFY_DOMAIN"

# Update .env file with Amplify domain
echo "Updating .env file with Amplify domain..."
if grep -q "AMPLIFY_DOMAIN=" "$ENV_FILE_PATH"; then
    sed -i "s|^AMPLIFY_DOMAIN=.*|AMPLIFY_DOMAIN=https://$AMPLIFY_DOMAIN|" "$ENV_FILE_PATH"
else
    echo "AMPLIFY_DOMAIN=https://$AMPLIFY_DOMAIN" >> "$ENV_FILE_PATH"
fi

if [ $? -ne 0 ]; then
  echo "Error: Failed to update .env file."
  exit 1
fi

echo ".env file updated."
echo "Amplify App Setup Complete!"

