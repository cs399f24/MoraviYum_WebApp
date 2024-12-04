if aws lambda get-function --function-name submit_review >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip submit_review.zip submit_review.py
aws lambda create-function --function-name submit_review \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://submit_review.zip \
  --handler submit_review.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name submit_review
aws lambda publish-version --function-name submit_review