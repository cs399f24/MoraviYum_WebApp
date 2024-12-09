#!/bin/bash

# Script to run create_s3.py and create_rds.py with proper environment setup

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check for .env file in .venv
if [ ! -f "../.venv/.env" ]; then
  # If not found in .venv, check in the main directory
  if [ ! -f "../.env" ]; then
    echo -e "${RED}Error: .env file not found in both .venv and main directory. Please create a .env file with the required environment variables.${NC}"
    exit 1
  fi
fi

# Check for Python
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.${NC}"
  exit 1
fi

# Install dependencies
echo -e "${GREEN}Installing required Python dependencies...${NC}"
pip install -q boto3 python-dotenv

# Run create_s3.py
echo -e "${GREEN}Running create_s3.py...${NC}"
python3 create_s3.py || { echo -e "${RED}create_s3.py execution failed.${NC}"; exit 1; }

# Run create_rds.py
echo -e "${GREEN}Running create_rds.py...${NC}"
python3 create_rds.py || { echo -e "${RED}create_rds.py execution failed.${NC}"; exit 1; }

echo -e "${GREEN}All tasks completed successfully.${NC}"
