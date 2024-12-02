if aws lambda delete-function --function-name get_user_handle >/dev/null 2>&1 ; then
    echo "DONE"
    rm get_user_handle.zip
else
    echo "Function does not exist"
fi