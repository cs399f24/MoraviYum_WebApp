import boto3
import dotenv
import os

dotenv.load_dotenv()

# Variables for database configuration
RDSUSERNAME = os.getenv('RDS_USERNAME')
RDSPASSWORD = os.getenv('RDS_PASSWORD')
RDSDBNAME = os.getenv('RDS_DB_NAME')
SECURITY_GROUP_ID = os.getenv('SECURITY_GROUP_ID')

db_identifier = "moraviyum"
master_username = RDSUSERNAME
master_password = RDSPASSWORD
db_name = RDSDBNAME
db_instance_class = "db.t3.micro"
engine = "mysql"
public_access = True
backup_retention = 7  # Number of days to retain backups
storage_type = "gp2"  # General Purpose SSD

# Create RDS client
rds_client = boto3.client('rds', region_name='us-east-1')

# Create the RDS instance
try:
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
