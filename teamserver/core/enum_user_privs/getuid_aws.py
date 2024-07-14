import boto3
import botocore
from datetime import datetime
import json
from termcolor import colored
import sys


from core.database.models import AWSUsers
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

DANGEROUS_POLICIES = [
    "cloudformation:CreateStack",

    "codestar:AssociateTeamMember",
    "codestar:CreateProject",
    "codestar:CreateProject",
    "codestar:CreateProjectFromTemplate",

    "datapipeline:CreatePipeline",
    "datapipeline:PutPipelineDefinition",

    "dynamodb:CreateTable",
    "dynamodb:PutItem",

    "ec2:RunInstances",

    "glue:CreateDevEndpoint",
    "glue:UpdateDevEndpoint",

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

    "lambda:AddPermission",
    "lambda:CreateEventSourceMapping",
    "lambda:CreateFunction",
    "lambda:CreateFunction",
    "lambda:CreateFunction",
    "lambda:InvokeFunction",
    "lambda:UpdateFunctionCode",
    "lambda:UpdateFunctionConfiguration",

    "sagemaker:CreateNotebookInstance",
    "sagemaker:CreatePresignedNotebookInstanceUrl",
    "sagemaker:CreatePresignedNotebookInstanceUrl",

    "ssm:CreateDocument",
    "ssm:GetCommandInvocation",
    "ssm:ModifyDocumentPermission",
    "ssm:SendCommand",
    "ssm:StartSession",
    "ssm:UpdateDocument",
    "ssm:UpdateDocumentDefaultVersion",
    "ssm:UpdateDocumentMetadata",

    "sts:AssumeRole"
]

def getuid(profile_dict, workspace):
    region = profile_dict['aws_region']
    access_key_id = profile_dict['aws_access_key']
    secret_key = profile_dict['aws_secret_key']
    session_token = ""

    if "aws_session_token" in profile_dict:
        session_token = profile_dict['aws_session_token']

    username = ""
    all_info = {}

    try:
        if "session_token" in profile_dict:
            client = boto3.client(
                "sts",
                region_name=region,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key
            )
        else:
            client = boto3.client(
                "sts",
                region_name=region,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token
            )

        try:
            response = client.get_caller_identity()
        except Exception as e:
            return {"error": "Invalid Credentials"}

        del response['ResponseMetadata']

        all_info['UserID'] = response
        all_info['UserName'] = (response['Arn']).split("/")[-1]

        del client
        username = (response['Arn']).split("/")[-1]

        if "session_token" in profile_dict:
            client = boto3.client(
                "iam",
                region_name=region,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key
            )
        else:
            client = boto3.client(
                "iam",
                region_name=region,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key,
                aws_session_token = session_token
            )

        if not username == "":
            response = client.get_user(
                UserName=username
            )
            del response['ResponseMetadata']

            all_info['UserInfo'] = response

            response = client.list_attached_user_policies(
                UserName=username
            )

            while response['IsTruncated']:
                response.update(client.list_attached_user_policies(
                    UserName=username,
                    Marker=response['Marker']
                ))

            if response['ResponseMetadata']:
                del response['ResponseMetadata']

            all_info['AttachedPolicies'] = response['AttachedPolicies']

        groups_for_users = client.list_groups_for_user(
            UserName=username
        )
        groups_json_data = groups_for_users['Groups']
        while groups_for_users['IsTruncated']:
            groups_for_users = client.list_groups_for_user(
                UserName=username,
                Marker=groups_for_users['Marker']
            )
            groups_json_data.extend(groups_for_users['Groups'])

        all_info['UserGroups'] = groups_json_data

        for group in all_info['UserGroups']:
            group_response = client.list_group_policies(
                GroupName=group['GroupName']
            )
            group['InlinePolicies'] = group_response['PolicyNames']

            while group_response['IsTruncated']:
                group_response = client.list_group_policies(
                    GroupName=group['GroupName'],
                    Marker=groups_for_users['Marker']
                )
                group['InlinePolicies'].extend(group_response['PolicyNames'])

            del group_response

            group_response = client.list_attached_group_policies(
                GroupName=group['GroupName']
            )

            group['AttachedPolicies'] = group_response['AttachedPolicies']
            while group_response['IsTruncated']:
                group_response = client.list_attached_group_policies(
                    GroupName=group['GroupName'],
                    Marker=groups_for_users['Marker']
                )
                (group['AttachedPolicies']).extend(group_response['AttachedPolicies'])

            policies = []
            for pol in group['AttachedPolicies']:
                response = client.get_policy(
                    PolicyArn=pol['PolicyArn']
                )
                if response['ResponseMetadata']:
                    del response['ResponseMetadata']
                policies.append(response)
            group['AttachedPolicies'] = policies

        try:
            db_data(all_info)


        except Exception as e:
            pass

    except Exception as e:
        pass
    return all_info

def db_data(all_info):
    return_data = {}

    try:
        return_data['aws_username'] = all_info['UserName']
    except KeyError:
        pass

    try:
        return_data['aws_user_arn'] = all_info['UserInfo']['User']['Arn']
    except KeyError:
        pass

    try:
        return_data['aws_user_id'] = all_info['UserInfo']['User']['UserId']
    except KeyError:
        pass

    try:
        return_data['aws_user_path'] = all_info['UserInfo']['User']['Path']
    except KeyError:
        pass

    try:
        return_data['aws_user_create_date'] = all_info['UserInfo']['User']['CreateDate']
    except KeyError:
        pass

    try:
        return_data['aws_user_create_date'] = all_info['UserInfo']['User']['CreateDate']
    except KeyError:
        pass

    try:
        return_data['aws_account_id'] = all_info['UserID']['Account']
    except KeyError:
        pass

    try:
        return_data['aws_user_attached_policies'] = all_info['AttachedPolicies']
    except KeyError:
        pass

    try:
        return_data['aws_user_policies'] = all_info['InlinePolicies']
    except KeyError:
        pass

    try:
        return_data['aws_user_groups'] = all_info['UserGroups']
    except KeyError:
        pass

    return return_data


'''
def enum_privesc(policies):
    full_policies = []
    other_policies = []
    for policy in policies:
        if "Read" in policy:
            pass
        elif "Full" in policy:
            full_policies.append(policy)
        else:
            other_policies.append(policy)

    del policy
    for policy in full_policies:
'''