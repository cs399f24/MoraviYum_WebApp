if aws lambda get-function --function-name menu >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip menu.zip lambda_menu.py
aws lambda create-function --function-name menu \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://menu.zip \
  --handler menu.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name menu
aws lambda publish-version --function-name menu
