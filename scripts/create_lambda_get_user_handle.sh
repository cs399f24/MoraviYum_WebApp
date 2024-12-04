if aws lambda get-function --function-name get_user_handle >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip get_user_handle.zip get_user_handle.py
aws lambda create-function --function-name get_user_handle \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://get_user_handle.zip \
  --handler get_user_handle.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name get_user_handle
aws lambda publish-version --function-name get_user_handle
