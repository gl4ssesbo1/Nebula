import sys

from core.database.models import AWSUsers
from flask_mongoengine import DoesNotExist

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE":{
		"value":"iam",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "USERNAME":{
		"value":"",
		"required":"false",
        "description":"A specific user to check."
	}
}

description = "List all users on the infrastructure and tries to get groups and policies."

calls = [
    'iam:GetAccountAuthorizationDetails',
    'iam:ListUsers',
    'iam:GetUser',
    'iam:ListGroupsForUser',
    'iam:ListUserPolicies',
    'iam:ListAttachedUserPolicies'
]

aws_command = "aws iam list-users --region <region> --profile <profile>"

def single_user(username, profile):
    try:
        # Get the user
        try:
            theuser = {}
            user_details = profile.get_account_authorization_details(Filter=['User'])
            print(user_details)
            for user in user_details['UserDetailList']:
                if user['UserName'] == username:
                    theuser = user
                    try:
                        user_policies = profile.list_user_policies(UserName=user['UserName'])
                        all_user_policies = user_policies['PolicyNames']
                        while user_policies['IsTruncated']:
                            marker = user_policies['Marker']
                            user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                            all_user_policies.extend(user_policies['PolicyNames'])

                        theuser['PolicyNames'] = all_user_policies
                    except:

                        pass

                    try:
                        user_groups = profile.list_user_policies(UserName=user['UserName'])
                        all_user_policies = user_groups['PolicyNames']
                        while user_groups['IsTruncated']:
                            marker = user_groups['Marker']
                            user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                            all_user_policies.extend(user_groups['PolicyNames'])

                        theuser['PolicyNames'] = all_user_policies
                        del user_groups

                    except:
                        break

                    del user_groups

        except:
            theuser = {}
            user_details = profile.get_user(UserName=username)
            if 'Tags' in user_details:
                theuser['Tags'] = user_details['Tags']

            if 'PermissionsBoundary' in user_details:
                theuser['PermissionsBoundary'] = user_details['PermissionsBoundary']

            del user

            try:
                user_groups = profile.list_groups_for_user(UserName=username)
                all_user_groups = user_groups['Groups']
                while user_groups['IsTruncated']:
                    marker = user_groups['Marker']
                    user_groups = profile.list_groups_for_user(UserName=username, Marker=marker)
                    all_user_groups.extend(user_groups['Groups'])

                del user_groups
                user_groups = []

                for group in all_user_groups:
                    user_groups.append(group['GroupName'])

                theuser['GroupList'] = user_groups
                del user_groups
            except:
                pass

            try:
                user_groups = profile.list_user_policies(UserName=username)
                all_user_attached_policies = user_groups['AttachedPolicies']
                while user_groups['IsTruncated']:
                    marker = user_groups['Marker']
                    user_groups = profile.list_groups_for_user(UserName=username, Marker=marker)
                    all_user_attached_policies.extend(user_groups['AttachedPolicies'])

                theuser['AttachedManagedPolicies'] = all_user_attached_policies
                del user_groups
            except:
                pass

            try:
                user_groups = profile.list_user_policies(UserName=username)
                all_user_policies = user_groups['PolicyNames']
                while user_groups['IsTruncated']:
                    marker = user_groups['Marker']
                    user_groups = profile.list_groups_for_user(UserName=username, Marker=marker)
                    all_user_policies.extend(user_groups['PolicyNames'])

                theuser['PolicyNames'] = all_user_policies
                del user_groups
            except:
                pass
        del user

        user_json = {
            "aws_username": theuser['UserName'],
            "aws_user_arn": theuser['Arn'],
            "aws_user_id": theuser['UserId'],
            "aws_user_create_date": theuser['CreateDate'],
            "aws_account_id": theuser['Arn'].split(":")[4],
            "aws_user_attached_policies": [],
            "aws_user_policies": [],
            "aws_user_path": theuser['Path'],
            "aws_user_groups": [],
            "aws_user_tags": []
        }

        if 'PasswordLastUsed' in theuser:
            user_json["aws_user_password_last_used"]: theuser['PasswordLastUsed']

        if 'PolicyNames' in theuser:
            user_json['aws_user_policies'] = theuser['PolicyNames']

        if 'GroupList' in theuser:
            user_json['aws_user_groups'] = theuser['GroupList']

        if 'UserPolicyList' in theuser:
            user_json['aws_user_policies'] = theuser['UserPolicyList']

        if 'AttachedManagedPolicies' in theuser:
            user_json['aws_user_attached_policies'] = theuser['AttachedManagedPolicies']

        if 'PermissionsBoundary' in theuser:
            user_json["aws_user_permission_boundary"] = theuser["PermissionsBoundary"]

        if 'Tags' in theuser:
            user_json['aws_user_tags'] = theuser['Tags']


        try:
            aws_user = AWSUsers.objects.get(aws_username=theuser['UserName'])
            aws_user.modify(**user_json)
            aws_user.save()

        except DoesNotExist:
            AWSUsers(**user_json).save()
            e = sys.exc_info()
            return {"error": "Error from module: {}".format(str(e))}, 500
        except:
            e = sys.exc_info()[1]
            if "AWSUsers matching query does not exist" in e:
                return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
            else:
                return {"error": "Error from module: {}".format(str(e))}, 500

        title_name = "UserName"
        return {title_name: user_json}, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500


def all_users(profile):
    try:
        # List Users
        iam_details = profile.list_users()
        while iam_details['IsTruncated']:
            iam_details = profile.list_users(Marker=iam_details['Marker'])

        json_data = iam_details['Users']

        a = {
            "UserDetailList": [
                {
                    "Path": "/",
                    "UserName": "admin",
                    "UserId": "AIDAURL7BRNWVWIKSI2ZM",
                    "Arn": "arn:aws:iam::312188439405:user/admin",
                    "CreateDate": "2021-10-29 15:57:00+00:00",
                    "GroupList": [],
                    "AttachedManagedPolicies": [
                        {
                            "PolicyName": "AdministratorAccess",
                            "PolicyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
                        }
                    ],
                    "Tags": []
                },
                {
                    "Path": "/",
                    "UserName": "testuser1",
                    "UserId": "AIDAURL7BRNW6AD3LYUKC",
                    "Arn": "arn:aws:iam::312188439405:user/testuser1",
                    "CreateDate": "2021-12-11 19:58:23+00:00",
                    "GroupList": [],
                    "AttachedManagedPolicies": [
                        {
                            "PolicyName": "AlexaForBusinessFullAccess",
                            "PolicyArn": "arn:aws:iam::aws:policy/AlexaForBusinessFullAccess"
                        },
                        {
                            "PolicyName": "AlexaForBusinessDeviceSetup",
                            "PolicyArn": "arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup"
                        }
                    ],
                    "Tags": [
                        {
                            "Key": "key",
                            "Value": "value"
                        }
                    ]
                }
            ]
        }

        # Get all users
        try:
            user_details = profile.get_account_authorization_details(Filter=['User'])
            print(user_details)
            for u_details in user_details['UserDetailList']:
                for user in json_data:
                    if 'GroupList' in u_details:
                        user['GroupList'] = u_details['GroupList']

                    if 'UserPolicyList' in u_details:
                        user['UserPolicyList'] = u_details['UserPolicyList']

                    if 'AttachedManagedPolicies' in u_details:
                        user['AttachedManagedPolicies'] = u_details['AttachedManagedPolicies']

                    if 'Tags' in u_details:
                        user['Tags'] = u_details['Tags']

                    if 'PermissionsBoundary' in u_details:
                        user['PermissionsBoundary'] = u_details['PermissionsBoundary']

                    try:
                        user_groups = profile.list_user_policies(UserName=user['UserName'])
                        all_user_policies = user_groups['PolicyNames']
                        while user_groups['IsTruncated']:
                            marker = user_groups['Marker']
                            user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                            all_user_policies.extend(user_groups['PolicyNames'])

                        user['PolicyNames'] = all_user_policies
                        del user_groups

                    except:
                        break
        except:
            for user in json_data:
                user_details = profile.get_user(UserName=user['UserName'])
                if 'Tags' in user_details:
                    user['Tags'] = user_details['Tags']

                if 'PermissionsBoundary' in user_details:
                    user['PermissionsBoundary'] = user_details['PermissionsBoundary']

            del user

            for user in json_data:
                try:
                    user_groups = profile.list_groups_for_user(UserName=user['UserName'])
                    all_user_groups = user_groups['Groups']
                    while user_groups['IsTruncated']:
                        marker = user_groups['Marker']
                        user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                        all_user_groups.extend(user_groups['Groups'])

                    del user_groups
                    user_groups = []

                    for group in all_user_groups:
                        user_groups.append(group['GroupName'])

                    user['GroupList'] = user_groups
                    del user_groups
                except:
                    break

            for user in json_data:
                try:
                    user_groups = profile.list_user_policies(UserName=user['UserName'])
                    all_user_attached_policies = user_groups['AttachedPolicies']
                    while user_groups['IsTruncated']:
                        marker = user_groups['Marker']
                        user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                        all_user_attached_policies.extend(user_groups['AttachedPolicies'])

                    user['AttachedManagedPolicies'] = all_user_attached_policies
                    del user_groups
                except:
                    break

            for user in json_data:
                try:
                    user_groups = profile.list_user_policies(UserName=user['UserName'])
                    all_user_policies = user_groups['PolicyNames']
                    while user_groups['IsTruncated']:
                        marker = user_groups['Marker']
                        user_groups = profile.list_groups_for_user(UserName=user['UserName'], Marker=marker)
                        all_user_policies.extend(user_groups['PolicyNames'])

                    user['PolicyNames'] = all_user_policies
                    del user_groups
                except:
                    break
        del user

        for user in json_data:
            user_json = {
                "aws_username": user['UserName'],
                "aws_user_arn": user['Arn'],
                "aws_user_id": user['UserId'],
                "aws_user_create_date": user['CreateDate'],
                "aws_account_id": user['Arn'].split(":")[4],
                "aws_user_attached_policies": [],
                "aws_user_policies": [],
                "aws_user_path": user['Path'],
                "aws_user_groups": [],
                "aws_user_tags": []
            }
            if 'PasswordLastUsed' in user:
                user_json["aws_user_password_last_used"]: user['PasswordLastUsed']

            if 'PolicyNames' in user:
                user_json['aws_user_policies'] = user['PolicyNames']

            if 'GroupList' in user:
                user_json['aws_user_groups'] = user['GroupList']

            if 'UserPolicyList' in user:
                user_json['aws_user_policies'] = user['UserPolicyList']

            if 'AttachedManagedPolicies' in user:
                user_json['aws_user_attached_policies'] = user['AttachedManagedPolicies']

            if 'PermissionsBoundary' in user:
                user_json["aws_user_permission_boundary"] = user["PermissionsBoundary"]

            if 'Tags' in user:
                user_json['aws_user_tags'] = user['Tags']

            try:
                aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
                aws_user.modify(**user_json)
                aws_user.save()

            except DoesNotExist:
                AWSUsers(**user_json).save()
                e = sys.exc_info()
                return {"error": "Error from module: {}".format(str(e))}, 500
            except:
                e = sys.exc_info()[1]
                if "AWSUsers matching query does not exist" in e:
                    return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
                else:
                    return {"error": "Error from module: {}".format(str(e))}, 500

        title_name = "UserName"
        return {title_name: json_data}, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500

def exploit(profile):
    username = variables['USERNAME']['value']

    if username == "":
        return all_users(profile)
    else:
        return single_user(username, profile)