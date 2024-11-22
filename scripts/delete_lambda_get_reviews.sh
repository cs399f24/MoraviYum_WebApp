if aws lambda delete-function --function-name get_reviews >/dev/null 2>&1 ; then
    echo "DONE"
    rm get_reviews.zip
else
    echo "Function does not exist"
fi