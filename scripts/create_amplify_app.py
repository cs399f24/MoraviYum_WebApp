import boto3
import os
import dotenv

dotenv.load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
ENV_FILE_PATH = ".env"
AMPLIFY_APP_NAME = "MoraviYumApp"

# Initialize clients
amplify_client = boto3.client('amplify')

def create_amplify_app():
    print("Creating Amplify app...")
    response = amplify_client.create_app(
        name=AMPLIFY_APP_NAME,
        platform='WEB',
    )
    app_id = response['app']['appId']
    print(f"Amplify app created with ID: {app_id}")
    return app_id

def link_s3_bucket_to_amplify(app_id):
    print(f"Linking S3 bucket to Amplify app...")
    amplify_client.create_branch(
        appId=app_id,
        branchName='prod',
        framework='',
        stage='PRODUCTION',
        enableAutoBuild=False,
        environmentVariables={
            "S3_BUCKET": S3_BUCKET
        }
    )
    print(f"S3 bucket linked to 'prod' branch.")

def deploy_amplify_app(app_id):
    print(f"Deploying Amplify app ID: {app_id}...")
    response = amplify_client.get_app(appId=app_id)
    domain = response['app']['defaultDomain']
    print(f"App deployed. Domain: {domain}")
    return domain

def update_env_file(domain_url):
    print("Updating .env file with the amplify domain...")
    amplify_domain = f"https://{domain_url}"

    with open(ENV_FILE_PATH, 'a') as env_file:
        env_file.write(f"\nAMPLIFY_DOMAIN={amplify_domain}")
    print(".env file updated.")

# Create Amplify app
app_id = create_amplify_app()
        
# Link S3 bucket
link_s3_bucket_to_amplify(app_id)

# Deploy Amplify app
domain_url = deploy_amplify_app(app_id)

# Update .env file with domain URLs
update_env_file(domain_url)

print("Amplify App Created!")
