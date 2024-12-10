#!/bin/bash

# Script to clean up all AWS resources by calling specific Python and Bash scripts

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AWS resource cleanup...${NC}"

# Run the delete_rds.py script
echo -e "${GREEN}Deleting RDS instances...${NC}"
python3 delete_rds.py || { echo -e "${RED}RDS cleanup failed.${NC}"; exit 1; }

# Run the delete_s3.py script
echo -e "${GREEN}Deleting S3 buckets...${NC}"
python3 delete_s3.py || { echo -e "${RED}S3 bucket cleanup failed.${NC}"; exit 1; }

# Run the delete_api.py script
echo -e "${GREEN}Deleting API Gateway resources...${NC}"
python3 delete_api.py || { echo -e "${RED}API Gateway cleanup failed.${NC}"; exit 1; }

# Run the delete_all_lambdas.sh script
echo -e "${GREEN}Deleting Lambda functions...${NC}"
./delete_all_lambdas.sh || { echo -e "${RED}Lambda cleanup failed.${NC}"; exit 1; }

echo -e "${GREEN}AWS resource cleanup completed successfully.${NC}"
