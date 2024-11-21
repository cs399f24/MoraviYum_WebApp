#!/bin/bash

# Get the RDS endpoint
DB_HOST=$(aws rds describe-db-instances --query "DBInstances[?DBInstanceIdentifier=='moraviyum'].Endpoint.Address" --output text)

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "Error: .env file not found!"
  exit 1
fi

# File paths for SQL dumps
CREATE_SQL="./database/create.sql"
INSERT_SQL="./database/insert.sql"

# Run create.sql
echo "Executing $CREATE_SQL..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$CREATE_SQL"
if [ $? -ne 0 ]; then
  echo "Error: Failed to execute $CREATE_SQL"
  exit 1
fi

# Run insert.sql
echo "Executing $INSERT_SQL..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$INSERT_SQL"
if [ $? -ne 0 ]; then
  echo "Error: Failed to execute $INSERT_SQL"
  exit 1
fi

echo "Database population completed successfully!"
