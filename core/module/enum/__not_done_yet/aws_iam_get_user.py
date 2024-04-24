from termcolor import colored
import sys
import json
from datetime import datetime
from pydoc import pipepager
import flask_mongoengine
from core.database.models import AWSUsers

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
	"SERVICE":{
		"value":"iam",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "USER":{
		"value":"",
		"required":"false",
        "description":"The user that will enumerate. If not added, all users will be attempted to be listed (provided we have ListUsers API Access) and we will get permissions of all users."
	}
}

description = "Enumerates the permissions of all users, groups, policies, roles or just any of them if required. The IAM whose credentials are provided needs to have IAMReadOnlyAccess, IAMFullAccess, or have permissions: "

aws_command = "aws iam get-user --user-name <user> --region <region> --profile <profile>"

#def exploit(profile, workspace):
def exploit(workspace):
    try:
        if not variables['USER']['value'] == "":
            # Chars allowed _+=,.@-
            '''
            user = profile.get_user(
                UserName=variables['USER']['value']
            )['User']
            '''

            user = {
                'Path': 'string',
                'UserName': 'string',
                'UserId': 'string',
                'Arn': 'string',
                'CreateDate': datetime(2015, 1, 1),
                'PasswordLastUsed': datetime(2015, 1, 1),
                'PermissionsBoundary': {
                    'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                    'PermissionsBoundaryArn': 'string'
                },
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ]
            }

            user_json = {
                "aws_username": user['UserName'],
                "aws_user_arn": user['Arn'],
                "aws_user_id": user['UserId'],
                "aws_user_create_date": user['CreateDate'],
                "aws_account_id": user['Arn'].split(":")[4],
                "aws_user_attached_policies": [],
                "aws_user_policies": [],
                "aws_user_groups": [],
                "aws_user_password_last_used": user['PasswordLastUsed'],
                "aws_user_tags": []
            }

            if 'PermissionsBoundary' in user:
                user_json["aws_user_permission_boundary"] = user["PermissionsBoundary"]

            if 'Tags' in user:
                user_json["aws_user_tags"] = user["Tags"]

            try:
                AWSUsers.objects(aws_user_id=user['UserId']).update(**user_json)
            except flask_mongoengine.DoesNotExist:
                AWSUsers(**user_json).save()

            title_name = "UserName"
            print(title_name)
            return {title_name: user}, 200

        else:

            all_users = []
            user_info = []
            '''
            users = profile.list_users()['Users']
            for user in users:
                all_users.append(user['UserName'])

            for user in all_users:
                username = profile.get_user(
                    UserName=user
                )['User']

                user_info.append(username)
            '''

            user_info = [
                {
                    'Path': 'string',
                    'UserName': 'string',
                    'UserId': 'strwwwwwing',
                    'Arn': 'arn:aws:iam::123456789012:user/Bob',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordLastUsed': datetime(2015, 1, 1),
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                {
                    'Path': 'string',
                    'UserName': 'staring',
                    'UserId': 'stdsadadsaring',
                    'Arn': 'arn:aws:iam::123456789012:user/Ann',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordLastUsed': datetime(2015, 1, 1),
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                {
                    'Path': 'string',
                    'UserName': 'sttring',
                    'UserId': 'strdadsadsadsadasing',
                    'Arn': 'arn:aws:iam::123456789012:user/Sid',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordLastUsed': datetime(2015, 1, 1),
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            ]

            #del user
            for user in user_info:
                print("user_info")
                print(user['Arn'])
                print(user['Arn'].split(":"))
                print(user['Arn'].split(":")[4])
                user_json = {
                    "aws_username": user['UserName'],
                    "aws_user_arn": user['Arn'],
                    "aws_user_id": user['UserId'],
                    "aws_user_create_date": user['CreateDate'],
                    "aws_account_id": user['Arn'].split(":")[4],
                    "aws_user_attached_policies": [],
                    "aws_user_path": user['Path'],
                    "aws_user_policies": [],
                    "aws_user_groups": [],
                    "aws_user_password_last_used": user['PasswordLastUsed'],
                    "aws_user_tags": []
                }
                if 'PermissionsBoundary' in user:
                    user_json["aws_user_permission_boundary"] = user["PermissionsBoundary"]

                if 'Tags' in user:
                    user_json["aws_user_tags"] = user["Tags"]

                try:
                    AWSUsers.objects(aws_user_id=user['UserId']).update(**user_json)
                except flask_mongoengine.DoesNotExist:
                    AWSUsers(**user_json).save()

                print(user_json)

            title_name = "UserName"
            print(title_name)
            return {title_name: user_info}, 200

    except:
        e = sys.exc_info()
        return {"error": str(e)}
