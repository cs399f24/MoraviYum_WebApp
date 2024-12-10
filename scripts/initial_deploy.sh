#!/bin/bash

# Script to deploy all AWS resources for the initial setup

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AWS initial deployment...${NC}"

# Deploy Lambda functions
echo -e "${GREEN}Creating Lambda functions...${NC}"
./create_all_lambdas.sh || { echo -e "${RED}Lambda creation failed.${NC}"; exit 1; }

# Deploy API Gateway
echo -e "${GREEN}Creating API Gateway resources...${NC}"
python3 create_api.py || { echo -e "${RED}API Gateway creation failed.${NC}"; exit 1; }

# Deploy API Gateway Authorizers
echo -e "${GREEN}Creating API Gateway authorizers...${NC}"
python3 create_authorizer.py || { echo -e "${RED}Authorizer creation failed.${NC}"; exit 1; }

# Deploy Cognito resources
echo -e "${GREEN}Creating Cognito resources...${NC}"
python3 create_cognito.py || { echo -e "${RED}Cognito creation failed.${NC}"; exit 1; }

# Deploy Amplify app
echo -e "${GREEN}Creating Amplify app...${NC}"
python3 create_amplify_app.py || { echo -e "${RED}Amplify app creation failed.${NC}"; exit 1; }

echo -e "${GREEN}AWS initial deployment completed successfully.${NC}"
