import boto3
import dotenv
import os

dotenv.load_dotenv()

# Variables for database configuration
RDS_USERNAME = os.getenv('RDS_USERNAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DB_NAME = os.getenv('RDS_DB_NAME')
SECURITY_GROUP_ID = os.getenv('SECURITY_GROUP_ID')

db_identifier = "moraviyum"
master_username = RDS_USERNAME
master_password = RDS_PASSWORD
db_name = RDS_DB_NAME
db_instance_class = "db.t3.micro"
engine = "mysql"
public_access = True
backup_retention = 1  # Number of days to retain backups
storage_type = "gp2"  # General Purpose SSD
region = "us-east-1"

# Create RDS client
ec2_client = boto3.client('ec2', region_name=region)
rds_client = boto3.client('rds', region_name=region)

def get_default_vpc():
    vpcs = ec2_client.describe_vpcs()
    for vpc in vpcs['Vpcs']:
        if vpc.get('IsDefault', False):  # Check if the VPC is the default
            print(f"Default VPC found: {vpc['VpcId']}")
            return vpc['VpcId']
    raise Exception("No default VPC found in the region.")

def create_security_group(vpc_id):
    try:
        response = ec2_client.create_security_group(
            GroupName="NewRDSAccessGroup",
            Description="Security group for RDS instance",
            VpcId=vpc_id
        )
        security_group_id = response['GroupId']
        print(f"New security group created: {security_group_id}")
        return security_group_id
    except Exception as e:
        print(f"Error creating security group: {e}")
        raise

def allow_inbound_mysql(security_group_id):
    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 3306,
                    'ToPort': 3306,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Temporarily allow acess everywhere for testing
                }
            ]
        )
        print(f"Inbound MySQL rule added to security group {security_group_id}.")
    except Exception as e:
        print(f"Error adding inbound rule: {e}")
        raise

# Create the RDS instance
try:

    # Get the default VPC
    default_vpc_id = get_default_vpc()

    # Create a new security group
    new_security_group_id = create_security_group(default_vpc_id)

    # Add inbound rule for MySQL
    allow_inbound_mysql(new_security_group_id)

    response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_identifier,
        DBInstanceClass=db_instance_class,
        Engine=engine,
        AllocatedStorage=20,
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        BackupRetentionPeriod=backup_retention,
        StorageType=storage_type,
        PubliclyAccessible=public_access,
        VpcSecurityGroupIds=[SECURITY_GROUP_ID],
        DBName=db_name,
        MultiAZ=False,
        AutoMinorVersionUpgrade=True
    )
    print(f"RDS instance '{db_identifier}' creation initiated. Please wait for it to become available.")
except Exception as e:
    print(f"An error occurred: {e}")
