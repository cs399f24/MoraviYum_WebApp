# MoraviYum Food Review Web App

An online web application designed for Moravian University students to help each other out by sharing their thoughts and opinions on the various foods provided on campus!

Project designed for *CSCI 399: Cloud Computing.*

## Contributers
- [Christine Colvin](https://github.com/christinecolvin)
- [Jack Drabic](https://github.com/JackJack7890)
- [Rafael Garcia Jr.](https://github.com/RGJ-713)
- [Michael Romero](https://github.com/MichaelRomero1)

## MoraviYum Architecture
![architecture](architecture.PNG)

## How It Works

Moravian students are greeted to a homepage where they can log in with their university email accounts.

![homepage](MoraviYum_home.png)

Once logged in, the user can then select one of two dining locations from the Moravian campus, "The B&G Cafe" or "DeLight's Cafe". They can select these locations and be presented a list of various food vendors from that location.

Once a vendor is selected, they can then select the food they want to leave a review and leave a rating from 1-5.

![reviewpage](MoraviYum_review.png)

# Tutorial - Deploy The App on Amazon Web Services (AWS)

### 1. Create a Cloud9 environment
First, open up the [AWS Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home?region=us-east-1#/) IDE and create a new Cloud9 environment by clicking the orange **`Create environment`** button.

Once you've given it a name, scroll down to the **`Network settings`** section at the bottom of the page and select **`Secure Shell (SSH)`**.

Once done, click the orange **`Create`** button to create the environment.

### 2. Clone the repo
Once you are all set up and have entered your Cloud9 environment, press the green **<> Code** button to gain a link to clone the repository.

Then, clone the repository with the following command:

```
git clone https://github.com/cs399f24/MoraviYum_WebApp.git
```

Once cloned, enter the **`MoraviYum_WebApp`** repository with the following command:

```
cd MoraviYum_WebApp
```

# Additional Info

### `.env` file
Certain scripts add to a `.env` file that hold your credentials. Should you feel the need to edit this manually, the `.env` must contain the following:
```
RDS_USERNAME='<FILL-IN-HERE>'
RDS_PASSWORD='<FILL-IN-HERE>'
RDS_DB_NAME='<FILL-IN-HERE>'
S3_BUCKET_NAME='<FILL-IN-HERE>'
AMPLIFY_DOMAIN='<FILL-IN-HERE>'
API_GATEWAYURL='<FILL-IN-HERE>'
USER_EMAIL='<FILL-IN-HERE>'
NEW_USERNAME='<FILL-IN-HERE>'
TEMP_PASS='<FILL-IN-HERE>'
```

