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
    'ssm:UpdateDocumentMetadata', 'iam:PutRolePolicy', 'glue:UpdateDevEndpoint', 'ssm:SendCommand',
    'sagemaker:CreatePresignedNotebookInstanceUrl', 'iam:PutUserPolicy', 'dynamodb:PutItem', 'ssm:UpdateDocument',
    'codestar:CreateProject', 'cloudformation:CreateStack', 'ssm:CreateDocument', 'lambda:AddPermission',
    'lambda:CreateEventSourceMapping', 'codestar:AssociateTeamMember', 'dynamodb:CreateTable',
    'iam:UpdateAssumeRolePolicy', 'ssm:ModifyDocumentPermission', 'iam:SetDefaultPolicyVersion', 'ec2:RunInstances',
    'lambda:UpdateFunctionCode', 'lambda:UpdateFunctionConfiguration', 'ssm:StartSession', 'iam:CreateAccessKey',
    'iam:PutGroupPolicy', 'lambda:InvokeFunction', 'ssm:UpdateDocumentDefaultVersion',
    'codestar:CreateProjectFromTemplate', 'glue:CreateDevEndpoint', 'sagemaker:CreateNotebookInstance',
    'iam:AddUserToGroup', 'ssm:GetCommandInvocation', 'iam:AttachRolePolicy', 'datapipeline:CreatePipeline',
    'iam:PassRole', 'iam:UpdateLoginProfile', 'datapipeline:PutPipelineDefinition', 'sts:AssumeRole',
    'iam:AttachGroupPolicy', 'iam:AttachUserPolicy', 'iam:CreatePolicyVersion', 'lambda:CreateFunction',
    'iam:CreateLoginProfile'
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

        arn = response['Arn']
        identityType = arn.split(":")[5].split("/")[0]

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
                aws_session_token=session_token
            )

        if identityType in [
            "user", "federated-user"
        ]:
            username = (response['Arn']).split("/")[-1]
            all_info = checkuser(client, username, response)

        else:
            rolename = (response['Arn']).split("/")[1]
            all_info = checkrole(client, rolename, response)


    except Exception as e:
        pass

    return all_info


def checkrole(client, rolename, response):
    all_info = {}
    all_info['UserId'] = response
    all_info['RoleName'] = rolename
    all_info['Arn'] = response['Arn']

    if not rolename == "":
        try:
            response = client.get_role(
                RoleName=rolename
            )
            del response['ResponseMetadata']

            all_info['RoleInfo'] = response

        except:
            pass

        try:
            response = client.list_role_policies(
                RoleName=rolename
            )

            while response['IsTruncated']:
                response.update(client.list_role_policies(
                    RoleName=rolename,
                    Marker=response['Marker']
                ))

            if response['ResponseMetadata']:
                del response['ResponseMetadata']

            all_info['RolePolicies'] = response['PolicyNames']

        except:
            pass

        try:
            response = client.list_attached_role_policies(
                RoleName=rolename
            )

            while response['IsTruncated']:
                response.update(client.list_attached_role_policies(
                    RoleName=rolename,
                    Marker=response['Marker']
                ))

            if response['ResponseMetadata']:
                del response['ResponseMetadata']

            all_info['AttachedPolicies'] = response['AttachedPolicies']

        except:
            pass

        try:
            db_data_role(all_info)

        except Exception as e:
            pass

    return all_info

def checkuser(client, username, response):
    all_info = {}
    all_info['UserID'] = response['UserId']
    all_info['UserName'] = username
    all_info['Arn'] = response['Arn']

    if not username == "":
        try:
            response = client.get_user(
                UserName=username
            )
            del response['ResponseMetadata']

            all_info['UserInfo'] = response

        except:
            
            pass

        try:
            response = client.list_user_policies(
                UserName=username
            )

            while response['IsTruncated']:
                response.update(client.list_user_policies(
                    UserName=username,
                    Marker=response['Marker']
                ))

            if response['ResponseMetadata']:
                del response['ResponseMetadata']

            all_info['UserPolicies'] = response['PolicyNames']

        except:
            
            pass

        try:
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

        except:
            
            pass

        try:
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
                try:
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
                except:
                    
                    pass

                try:
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
                except:
                    
                    pass

                policies = []
                for pol in group['AttachedPolicies']:
                    try:
                        response = client.get_policy(
                            PolicyArn=pol['PolicyArn']
                        )
                        if response['ResponseMetadata']:
                            del response['ResponseMetadata']
                        policies.append(response)
                        group['AttachedPolicies'] = policies

                    except:
                        
                        pass

        except:
            
            pass
        try:
            db_data_user(all_info)


        except Exception as e:
            pass

    
    return all_info


def db_data_role(all_info):
    return_data = {}

    try:
        return_data['aws_username'] = all_info['RoleName']
    except KeyError:
        pass

    try:
        return_data['aws_role_arn'] = all_info['RoleInfo']['Role']['Arn']
    except KeyError:
        pass

    try:
        return_data['aws_role_id'] = all_info['RoleInfo']['Role']['RoleId']
    except KeyError:
        pass

    try:
        return_data['aws_role_path'] = all_info['RoleInfo']['Role']['Path']
    except KeyError:
        pass

    try:
        return_data['aws_role_create_date'] = all_info['RoleInfo']['Role']['CreateDate']
    except KeyError:
        pass

    try:
        return_data['aws_role_create_date'] = all_info['RoleInfo']['Role']['CreateDate']
    except KeyError:
        pass

    try:
        return_data['aws_account_id'] = all_info['RoleID']['Account']
    except KeyError:
        pass

    try:
        return_data['aws_role_attached_policies'] = all_info['AttachedPolicies']
    except KeyError:
        pass

    try:
        return_data['aws_role_policies'] = all_info['InlinePolicies']
    except KeyError:
        pass

    return return_data


def db_data_user(all_info):
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
