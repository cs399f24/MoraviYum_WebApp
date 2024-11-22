if aws lambda delete-function --function-name review >/dev/null 2>&1 ; then
    echo "DONE"
    rm review.zip
else
    echo "Function does not exist"
fi