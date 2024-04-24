import boto3
import json
import botocore.exceptions

from core.database.models import AWSUsers
from flask_mongoengine import DoesNotExist

from core.createSession.giveMeClient import giveMeClient

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "USERNAME": {
        "value": "current-user",
        "required": "false",
        "description": "The current-user, a user to test or All. If no user put, it will test current-user."
    },
    "AUTO-ESCALATION": {
        "value": "false",
        "required": "true",
        "description": "If set to true, it will try to give you administrator access with the first possible method."
    }
}

description = "Test most common privilege escalation APIs to get privesc on the account."

calls = [
    'iam:GetAccountAuthorizationDetails',
    'iam:ListUsers',
    'iam:GetUser',
    'iam:ListGroupsForUser',
    'iam:ListUserPolicies',
    'iam:ListAttachedUserPolicies'
]

aws_command = "aws iam get-account-authorization-details --region <region> --profile <profile>"


# Begin privesc scanning
all_perms = [
    'iam:AddUserToGroup',
    'iam:AttachGroupPolicy',
    'iam:AttachRolePolicy',
    'iam:AttachUserPolicy',
    'iam:CreateAccessKey',
    'iam:CreatePolicyVersion',
    'iam:CreateLoginProfile',
    'iam:PassRole',
    'iam:PutGroupPolicy',
    'iam:PutRolePolicy',
    'iam:PutUserPolicy',
    'iam:SetDefaultPolicyVersion',
    'iam:UpdateAssumeRolePolicy',
    'iam:UpdateLoginProfile',
    'sts:AssumeRole',
    'ec2:RunInstances',
    'lambda:CreateEventSourceMapping',
    'lambda:CreateFunction',
    'lambda:InvokeFunction',
    'lambda:UpdateFunctionCode',
    'dynamodb:CreateTable',
    'dynamodb:PutItem',
    'glue:CreateDevEndpoint',
    'glue:UpdateDevEndpoint',
    'cloudformation:CreateStack',
    'datapipeline:CreatePipeline'
]

escalation_methods = {
    'privesc/aws_iam_create_policy_version': {
        'iam:CreatePolicyVersion': False
    },
    'privesc/aws_iam_set_default_policy_version': {
        'iam:SetDefaultPolicyVersion': False
    },
    'privesc/aws_iam_create_instance_with_existing_instance_profile': {
        'iam:PassRole': False,
        'ec2:RunInstances': False
    },
    'privesc/create_access_key': {
        'iam:CreateAccessKey': False
    },
    'privesc/aws_iam_create_login_profile': {
        'iam:CreateLoginProfile': False
    },
    'privesc/aws_iam_update_login_profile': {
        'iam:UpdateLoginProfile': False
    },
    'privesc/aws_iam_attach_user_policy': {
        'iam:AttachUserPolicy': False
    },
    'privesc/aws_iam_attach_group_policy': {
        'iam:AttachGroupPolicy': False
    },
    'privesc/aws_iam_attach_role_policy': {
        'iam:AttachRolePolicy': False,
        'sts:AssumeRole': False
    },
    'privesc/aws_iam_put_user_policy': {
        'iam:PutUserPolicy': False
    },
    'privesc/aws_iam_put_group_policy': {
        'iam:PutGroupPolicy': False
    },
    'privesc/aws_iam_put_role_policy': {
        'iam:PutRolePolicy': False,
        'sts:AssumeRole': False
    },
    'privesc/aws_iam_add_user_to_group': {
        'iam:AddUserToGroup': False
    },
    'privesc/aws_iam_update_role_policy': {
        'iam:UpdateAssumeRolePolicy': False,
        'sts:AssumeRole': False
    },
    'privesc/aws_lambda_create_function': {
        'iam:PassRole': False,
        'lambda:CreateFunction': False,
        'lambda:InvokeFunction': False
    },
    'privesc/aws_lambda_create_function_with_dynamo': {
        'iam:PassRole': False,
        'lambda:CreateFunction': False,
        'lambda:CreateEventSourceMapping': False,
        'dynamodb:CreateTable': False,
        'dynamodb:PutItem': False
    },
    'privesc/aws_lambda_create_function_with_new_dynamo': {
        'iam:PassRole': False,
        'lambda:CreateFunction': False,
        'lambda:CreateEventSourceMapping': False
    },
    'privesc/aws_glue_pass_role_to_glue_endpoint': {
        'iam:PassRole': False,
        'glue:CreateDevEndpoint': False
    },
    'privesc/aws_glue_update_role_of_glue_endpoint': {
        'glue:UpdateDevEndpoint': False
    },
    'privesc/aws_cloudformation_pass_role_to_cloud_formation': {
        'iam:PassRole': False,
        'cloudformation:CreateStack': False
    },
    'privesc/aws_datapipeline_pass_role_to_datapipeline': {
        'iam:PassRole': False,
        'datapipeline:CreatePipeline': False
    },
    'privesc/aws_datapipeline_update_role_of_datapipeline': {
        'lambda:UpdateFunctionCode': False
    }
}

def enum_current_user_privs(all_sessions, cred_prof, useragent, web_proxies):
    # Get Caller Identity
    stsProfile = giveMeClient(
        all_sessions,
        cred_prof,
        useragent,
        web_proxies,
        "sts"
    )
    response = stsProfile.get_caller_identity()

    usename = (response['Arn']).split("/")[-1]
    accountId = (response['Account']).split("/")[-1]
    accessKeyId = (response['UserId']).split("/")[-1]

    del(response)

    # Get IAM policy
    iamProfile = giveMeClient(
        all_sessions,
        cred_prof,
        useragent,
        web_proxies,
        "iam"
    )

def exploit(all_sessions, cred_prof, useragent, web_proxies):
    return enum_current_user_privs(all_sessions, cred_prof, useragent, web_proxies)
