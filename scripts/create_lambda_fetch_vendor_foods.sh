if aws lambda get-function --function-name fetch_vendor_foods >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip fetch_vendor_foods.zip lambda_fetch_vendor_foods.py
aws lambda create-function --function-name fetch_vendor_foods \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://fetch_vendor_foods.zip \
  --handler fetch_vendor_foods.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name fetch_vendor_foods
aws lambda publish-version --function-name fetch_vendor_foods
