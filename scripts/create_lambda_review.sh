if aws lambda get-function --function-name review >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip review.zip lambda_reviews.py
aws lambda create-function --function-name review \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://review.zip \
  --handler review.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name review
aws lambda publish-version --function-name review