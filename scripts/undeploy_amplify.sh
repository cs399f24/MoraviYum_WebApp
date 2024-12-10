#!/bin/bash

# Script to delete an AWS Amplify app

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Amplify app deletion...${NC}"

# Function to delete the Amplify app
delete_amplify_app() {
    local amplify_app_id=$1

    echo -e "${GREEN}Deleting Amplify app: ${amplify_app_id}...${NC}"

    # List branches associated with the Amplify app and delete them
    branches=$(aws amplify list-branches --app-id "$amplify_app_id" --query 'branches[*].branchName' --output text)
    for branch in $branches; do
        echo -e "${GREEN}Deleting branch: ${branch}...${NC}"
        aws amplify delete-branch --app-id "$amplify_app_id" --branch-name "$branch" || {
            echo -e "${RED}Failed to delete branch: ${branch}${NC}"
            exit 1
        }
    done

    # Delete the Amplify app
    aws amplify delete-app --app-id "$amplify_app_id" || {
        echo -e "${RED}Failed to delete Amplify app: ${amplify_app_id}${NC}"
        exit 1
    }

    echo -e "${GREEN}Amplify app ${amplify_app_id} deleted successfully.${NC}"
}

# Prompt for the Amplify App ID
read -p "Enter the Amplify App ID to delete: " app_id

if [ -z "$app_id" ]; then
    echo -e "${RED}Amplify App ID is required. Exiting.${NC}"
    exit 1
fi

# Call the delete function
delete_amplify_app "$app_id"

echo -e "${GREEN}Amplify app deletion completed.${NC}"
