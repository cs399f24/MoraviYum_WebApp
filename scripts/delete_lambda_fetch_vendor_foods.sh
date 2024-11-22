if aws lambda delete-function --function-name fetch_vendor_foods >/dev/null 2>&1 ; then
    echo "DONE"
    rm fetch_vendor_foods.zip
else
    echo "Function does not exist"
fi