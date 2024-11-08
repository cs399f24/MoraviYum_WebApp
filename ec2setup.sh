#!/bin/bash

# Step 1: Install MariaDB
echo "Installing MariaDB..."
sudo dnf install -y mariadb105-server

# Start MariaDB service
echo "Starting MariaDB service..."
sudo systemctl start mariadb

# Secure MySQL installation
echo "Securing MariaDB installation..."
echo "Creating MariaDB user \"root\"..."

read -sp "Create a password for \"root\" user: " root_password
sudo mysql_secure_installation <<EOF

# Enter password for "root" when prompted
$root_password
# Switch to socket authentication
n
# Change root password
n
# Remove anonymous users
Y
# Disallow root login remotely
Y
# Remove test database and access to it
Y
# Reload privilege tables
Y
EOF

# Step #2: Create the 'MoraviYum' database.
echo ""
echo "MariaDB user \"root\" has been created."

echo ""
echo "Allowing \"root\" user to connect to MariaDB..."
sudo mysql -u root -p -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$root_password';"

echo ""
echo "Populating the database..."
cd database

echo ""
echo "Creating tables..."
mysql -u root -p < create.sql

echo ""
echo "Inserting data..."
mysql -u root -p MoraviYum < insert.sql
cd ..

echo ""
echo "Restarting and enabling MariaDB service..."
sudo systemctl restart mariadb
sudo systemctl enable mariadb

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

read -sp "Enter your flask secret key: " flask_secret_key
echo "FLASK_SECRET_KEY=\"$flask_secret_key\"" >> .env
echo ""

echo ""
echo "Creating MariaDB connection details..."
read -p "Enter your MariaDB username: " mysql_username
echo "MYSQL_USERNAME=\"$mysql_username\"" >> .env

read -sp "Enter your MariaDB password: " mysql_password
echo "MYSQL_PASSWORD=\"$mysql_password\"" >> .env

echo "MYSQL_HOST=\"localhost\"" >> .env

echo "MYSQL_DATABASE=\"MoraviYum\"" >> .env

sudo /home/ec2-user/MoraviYum_WebApp/.venv/bin/gunicorn -w4 --bind 0.0.0.0:80 --chdir /home/ec2-user/MoraviYum_WebApp server:app
