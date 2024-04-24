import boto3
from moto import *
import sys
import json
from termcolor import colored
from pydoc import pipepager

SERVICES = [
    "ec2",
    "iam",
    "sts",
    "lambda",
    "dynamodb",
    "glue",
    "cloudformation",
    "datapipeline",
    "codestar",
    "sagemaker",
    "ssm"
]

DANGEROUS_POLICIES = {
    "cloudformation":[
        "cloudformation:CreateStack"
    ],

    "codestar":[
        "codestar:AssociateTeamMember",
        "codestar:CreateProject",
        "codestar:CreateProject",
        "codestar:CreateProjectFromTemplate"
    ],

    "datapipeline": [
        "datapipeline:CreatePipeline",
        "datapipeline:PutPipelineDefinition",
    ],

    "dynamodb": [
        "dynamodb:CreateTable",
        "dynamodb:PutItem",
    ],

    "ec2": [
        "ec2:RunInstances",
    ],

    "glue":[
        "glue:CreateDevEndpoint",
        "glue:UpdateDevEndpoint",
    ],

    "iam": [
        "iam:AddUserToGroup",
        "iam:AttachGroupPolicy",
        "iam:AttachRolePolicy",
        "iam:AttachUserPolicy",
        "iam:CreateAccessKey",
        "iam:CreateLoginProfile",
        "iam:CreatePolicyVersion",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PassRole",
        "iam:PutGroupPolicy",
        "iam:PutRolePolicy",
        "iam:PutUserPolicy",
        "iam:SetDefaultPolicyVersion",
        "iam:UpdateAssumeRolePolicy",
        "iam:UpdateLoginProfile",
    ],

    "lambda":[
        "lambda:AddPermission",
        "lambda:CreateEventSourceMapping",
        "lambda:CreateFunction",
        "lambda:CreateFunction",
        "lambda:CreateFunction",
        "lambda:InvokeFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
    ],

    "sagemaker": [
        "sagemaker:CreateNotebookInstance",
        "sagemaker:CreatePresignedNotebookInstanceUrl",
    ],

    "ssm":[
        "ssm:CreateDocument",
        "ssm:GetCommandInvocation",
        "ssm:ModifyDocumentPermission",
        "ssm:SendCommand",
        "ssm:StartSession",
        "ssm:UpdateDocument",
        "ssm:UpdateDocumentDefaultVersion",
        "ssm:UpdateDocumentMetadata"
    ],

    "sts": [
        "sts:AssumeRole"
    ]
}

# ---------------------------
# GetCallerIdentity
# ---------------------------
def get_user_arn(access_key_id, secret_key, region, session_token):
    if session_token == "":
        stscli = boto3.client("sts", region_name=region, aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_key)
    else:
        stscli = boto3.client("sts", region_name=region, aws_access_key_id=access_key_id,
                              aws_secret_access_key=secret_key, aws_session_token=session_token)

    return stscli.get_caller_identity()


# ---------------------------
# GetUID get user and user's policies
# ---------------------------
def get_user_and_user_policies(username, accesskey, secretkey, region, session_token):
    if session_token == "":
        iamcli = boto3.client("iam", region_name=region, aws_access_key_id=accesskey,
                              aws_secret_access_key=secretkey)
    else:
        iamcli = boto3.client("iam", region_name=region, aws_access_key_id=accesskey,
                              aws_secret_access_key=secretkey, aws_session_token=session_token)
    try:
        get_attached_user_policies = iamcli.list_attached_user_policies(
            UserName=username.split("/")[-1]
        )

        get_user_policies = iamcli.list_user_policies(
            UserName=username.split("/")[-1]
        )

        attached_policies = []
        inline_policies = []

        for attpolicy in get_attached_user_policies['AttachedPolicies']:
            attached_policies.append(attpolicy['PolicyArn'])

        for inpolicy in get_user_policies['PolicyNames']:
            inline_policies.append(inpolicy)

        return_dict = {}
        return_dict['AttchedPolicies'] = attached_policies
        return_dict['InlinePolicies'] = inline_policies

        return return_dict

    except:
        e = {"error": sys.exc_info()[1]}

        return e

# ---------------------------
# Get Each Policy
# ---------------------------


# ---------------------------
# IAM Privesc
# ---------------------------
@mock_iam
def test_create_user_policy(accesskey, secretkey, region):
    iam_user = boto3.client("iam", region_name=region, aws_access_key_id=accesskey, aws_secret_access_key=secretkey)

    # Create Policy Version
    iam_user.create_policy_version()

# ---------------------------
# main
# ---------------------------
def enum_privesc(profile_dict):
    region = profile_dict['region']
    access_key_id = profile_dict['access_key_id']
    secret_key = profile_dict['secret_key']
    session_token = ""
    if profile_dict['session_token']:
        session_token = profile_dict['session_token']

    username = get_user_arn(access_key_id, secret_key, region, session_token)['Arn']
    user_policies = get_user_and_user_policies(username, access_key_id, secret_key, region, session_token)

    if 'error' in user_policies:
        pass
    else:
        for key, value in user_policies:
            print(colored())