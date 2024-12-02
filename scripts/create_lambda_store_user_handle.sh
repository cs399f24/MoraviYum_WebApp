if aws lambda get-function --function-name store_user_handle >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip store_user_handle.zip lambda_store_user_handle.py
aws lambda create-function --function-name review \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://store_user_handle.zip \
  --handler store_user_handle.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name store_user_handle
aws lambda publish-version --function-name store_user_handle