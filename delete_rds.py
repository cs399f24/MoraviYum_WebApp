import boto3

# Variable for database identifier
db_identifier = "moraviyum"
security_group_name = "MoraviYumRDSGroup"

# Create RDS client
rds_client = boto3.client('rds', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Delete the RDS instance
try:
    response = rds_client.delete_db_instance(
        DBInstanceIdentifier=db_identifier,
        SkipFinalSnapshot=True
    )
    print(f"RDS instance '{db_identifier}' deletion initiated. Status: {response['DBInstance']['DBInstanceStatus']}")

    # Wait for RDS instance to be deleted
    print("Waiting for RDS instance to be deleted...")
    waiter = rds_client.get_waiter('db_instance_deleted')
    waiter.wait(DBInstanceIdentifier=db_identifier)
    print(f"RDS instance '{db_identifier}' has been deleted.")
    
    # Delete the security group
    print(f"Deleting security group '{security_group_name}'...")
    security_groups = ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [security_group_name]}])
    if security_groups['SecurityGroups']:
        security_group_id = security_groups['SecurityGroups'][0]['GroupId']
        ec2_client.delete_security_group(GroupId=security_group_id)
        print(f"Security group '{security_group_name}' deleted successfully.")
    else:
        print(f"Security group '{security_group_name}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
