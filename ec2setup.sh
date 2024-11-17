#!/bin/bash

mysql_password=$(aws secretsmanager get-secret-value \
    --secret-id arn:aws:secretsmanager:us-east-1:062080672614:secret:prod/moraviyum/rds-3fB00w \
    --query 'SecretString' \
    --output text | jq -r '.password')

mysql_username=$(aws secretsmanager get-secret-value \
    --secret-id arn:aws:secretsmanager:us-east-1:062080672614:secret:prod/moraviyum/rds-3fB00w \
    --query 'SecretString' \
    --output text | jq -r '.user_name')

echo ""
echo "Populating the database..."
cd database

echo ""
echo "Creating tables..."
mysql -u $mysql_username -p$mysql_password < create.sql

echo ""
echo "Inserting data..."
mysql -u $mysql_username -p$mysql_password MoraviYum < insert.sql
cd ..

# Step #4: Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi # Close if statement

# Step #5: Install requirements
echo ""
echo "Setting up virtual environment and installing requirements..."
source .venv/bin/activate
pip install -r requirements.txt

# Step #6: Create .env file
echo ""
echo "Creating .env file..."

flask_secret_key=$(python3 -c "import secrets; print(secrets.token_hex())")
echo "FLASK_SECRET_KEY=\"$flask_secret_key\"" >> .env
echo ""

echo ""
echo "Creating MariaDB connection details..."
echo "MYSQL_USERNAME=\"$mysql_username\"" >> .env
echo "MYSQL_PASSWORD=\"$mysql_password\"" >> .env

echo "MYSQL_HOST=\"moraviyum-database.c6ear6iqzuqu.us-east-1.rds.amazonaws.com\"" >> .env

echo "MYSQL_DATABASE=\"MoraviYum\"" >> .env

sudo /home/ec2-user/MoraviYum_WebApp/.venv/bin/gunicorn -w4 --bind 0.0.0.0:80 --chdir /home/ec2-user/MoraviYum_WebApp server:app
