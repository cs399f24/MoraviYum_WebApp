import boto3

# Variable for database identifier
db_identifier = "moraviyum"

# Create RDS client
rds_client = boto3.client('rds', region_name='us-east-1')

# Delete the RDS instance
try:
    response = rds_client.delete_db_instance(
        DBInstanceIdentifier=db_identifier,
        SkipFinalSnapshot=False
    )
    print(f"RDS instance '{db_identifier}' deletion initiated. Status: {response['DBInstance']['DBInstanceStatus']}")
except Exception as e:
    print(f"An error occurred: {e}")
