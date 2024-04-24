import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import sys
from moto import *

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
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"OTHERVARIABLE": {
		"value": "",
		"required": "true/false",
        "description":"Another variable to set"
	}
}
description = "Description of your Module"

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

# The exploit function is like the main() of the module. This is called 
# from the module

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""

def list_dictionary(d, n_tab):
	global output
	if isinstance(d, list):
		n_tab += 1
		for i in d:
			if not isinstance(i, list) and not isinstance(i, dict):
				output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
			else:
				list_dictionary(i, n_tab)
	elif isinstance(d, dict):
		n_tab+=1
		for key, value in d.items():
			if not isinstance(value, dict) and not isinstance(value, list):
				output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
			else:
				output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
				list_dictionary(value, n_tab)

def exploit(profile, workspace):
	n_tab = 0
	global output

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_instances".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	response = {
		"Test":"",
		"ResponseData":""
	}
	json_data = response['Test']
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	title_name = ""
	if isinstance(json_data, list):
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		for data in json_data:
			output += colored("{}: {}\n".format(title_name, data[title_name]), "yellow", attrs=['bold'])
			list_dictionary(data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	else:
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
		list_dictionary(json_data, n_tab)
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	pipepager(output, "less -R")

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
    "iam:CreatePolicyVersion",
    "iam:SetDefaultPolicyVersion",
    "iam:PassRole",
    "ec2:RunInstances",
    "iam:CreateAccessKey",
    "iam:CreateLoginProfile",
    "iam:UpdateLoginProfile",
    "iam:AttachUserPolicy",
    "iam:AttachGroupPolicy",
    "iam:AttachRolePolicy",
    "iam:PutUserPolicy",
    "iam:PutGroupPolicy",
    "iam:PutRolePolicy",
    "iam:AddUserToGroup",
    "iam:UpdateAssumeRolePolicy",
    "sts:AssumeRole",
    "iam:PassRole",
    "lambda:CreateFunction",
    "lambda:InvokeFunction",
    "iam:PassRole",
    "lambda:CreateFunction",
    "lambda:AddPermission",
    "iam:PassRole",
    "lambda:CreateFunction",
    "lambda:CreateEventSourceMapping",
    "dynamodb:PutItem",
    "dynamodb:CreateTable",
    "lambda:UpdateFunctionCode",
    "iam:PassRole",
    "glue:CreateDevEndpoint",
    "glue:UpdateDevEndpoint",
    "iam:PassRole",
    "cloudformation:CreateStack",
    "iam:PassRole",
    "datapipeline:CreatePipeline",
    "datapipeline:PutPipelineDefinition",
    "codestar:CreateProjectFromTemplate",
    "codestar:CreateProject",
    "iam:PassRole",
    "codestar:CreateProject",
    "codestar:AssociateTeamMember",
    "lambda:UpdateFunctionConfiguration",
    "sagemaker:CreateNotebookInstance",
    "sagemaker:CreatePresignedNotebookInstanceUrl",
    "iam:PassRole",
    "sagemaker:CreatePresignedNotebookInstanceUrl",
    "ssm:SendCommand",
    "ssm:GetCommandInvocation",
    "ssm:StartSession",
    "ssm:UpdateDocument",
    "ssm:CreateDocument",
    "ssm:UpdateDocumentDefaultVersion",
    "ssm:UpdateDocumentMetadata",
    "ssm:ModifyDocumentPermission"
]

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