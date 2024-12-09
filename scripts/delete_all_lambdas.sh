#!/bin/bash

# Ensure all delete scripts are executable
echo "Setting executable permissions for delete scripts..."
chmod +x ./delete_*

# Check if chmod was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to set executable permissions for delete scripts. Exiting."
  exit 1
fi

# Array of delete scripts to execute
delete_scripts=(
  "./delete_lambda_fetch_vendor_foods.sh"
  "./delete_lambda_menu.sh"
  "./delete_lambda_get_reviews.sh"
  "./delete_lambda_submit_review.sh"
)

# Execute each script in the array
for script in "${delete_scripts[@]}"; do
  echo "Running $script..."
  $script
  if [ $? -ne 0 ]; then
    echo "Warning: $script encountered an issue but will continue."
  fi
done

echo "All delete scripts executed successfully, with possible warnings."
