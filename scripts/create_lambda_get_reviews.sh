if aws lambda get-function --function-name get_reviews >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip get_reviews.zip get_reviews.py
aws lambda create-function --function-name get_reviews \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://get_reviews.zip \
  --handler get_reviews.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name get_reviews
aws lambda publish-version --function-name get_reviews
