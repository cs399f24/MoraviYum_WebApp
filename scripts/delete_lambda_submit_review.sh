if aws lambda delete-function --function-name submit_review >/dev/null 2>&1 ; then
    echo "DONE"
    rm submit_review.zip
else
    echo "Function does not exist"
fi