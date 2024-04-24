import sys

import botocore.exceptions

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

aws_command = "aws iam get-account-authorization-details --region <region> --profile <profile>"

def single_user(profile, username):
    try:
        # Get all users
        try:
            acc_auth = profile.get_account_authorization_details()

            user_details = acc_auth['UserDetailList']
            group_details = acc_auth['GroupDetailList']

            json_data = {}

            user_found = 0

            for user in user_details:
                if user['UserName'] == username:
                    json_data = user
                    json_data['GroupPolicyList'] = {}
                    json_data['GroupAttachedManagedPolicies'] = {}
                    user_found = 1

            if user_found == 0:
                return {"error":"User not found. Like, who the hell is this motherfucker?"}, 404
            user_found = 0

            # Get access key last used
            try:
                access_key_last_used = profile.get_access_key_last_used(
                    AccessKeyId=json_data['UserId']
                )
                user_details['AccessKeyLastUsed'] = access_key_last_used

            except:
                pass

            # Get Group Inline Policies
            for user_group in json_data['GroupList']:
                for group in group_details:
                    if user_group == group['GroupName']:
                        json_data['GroupPolicyList'][user_group] = group['GroupPolicyList']

            # Get Group Attached Policies
            for user_group in user_details['GroupList']:
                for group in group_details:
                    if user_group == group['GroupName']:
                        user['GroupAttachedManagedPolicies'][user_group] = group['AttachedManagedPolicies']


            del user
            del group
            all_users_info = user_details
            del user_details
            del group_details

        except:
            # List Users
            iam_details = {}

            user_found = 0

            try:
                iam_det = profile.list_users()
                while iam_det['IsTruncated']:
                    iam_det = profile.list_users(Marker=iam_det['Marker'])

                for user in iam_det['Users']:
                    if user['UserName'] == username:
                        iam_details = user
                        user_found = 1
                        break

                if user_found == 0:
                    return {"error": "User not found. Like, who the hell is this motherfucker?"}, 404
                user_found = 0

            except botocore.exceptions.ClientError:
                try:
                    iam_details = profile.get_user(Username=username)['User']
                except botocore.exceptions.ClientError:
                    return {"error": "You have no access on either GetAccountAuthorizationDetails, ListUsers, or GetUser. That, or you have no internet connection, but you must have fixed it. I hope."}, 500
            else:
                return {"error": "User not found. Like, who the hell is this motherfucker?"}, 404

            # Get Groups of user
            try:
                user_groups = profile.list_groups_for_user(UserName=iam_details['UserName'])
                all_user_groups = user_groups['Groups']
                while user_groups['IsTruncated']:
                    marker = user_groups['Marker']
                    user_groups = profile.list_groups_for_user(UserName=iam_details['UserName'], Marker=marker)
                    all_user_groups.extend(user_groups['Groups'])

                del user_groups
                user_groups = []

                for group in all_user_groups:
                    user_groups.append(group['GroupName'])

                iam_details['GroupList'] = user_groups
                del user_groups

                # List Group Policies
                for group in iam_details['GroupList']:
                    try:
                        group_attached_policies = profile.list_group_policies(
                            GroupName=group
                        )

                        while group_attached_policies['IsTruncated']:
                            group_attached_policies.update(profile.list_group_policies(
                                GroupName=group,
                                Marker=group_attached_policies['Marker']
                            ))

                        if group_attached_policies['ResponseMetadata']:
                            del group_attached_policies['ResponseMetadata']

                        iam_details['PolicyNames'] = group_attached_policies['PolicyNames']
                    except:
                        break

                    # List Attached Group Policies
                    for group in iam_details['GroupList']:
                        try:
                            group_attached_policies = profile.list_attached_group_policies(
                                GroupName=group
                            )

                            while group_attached_policies['IsTruncated']:
                                group_attached_policies.update(profile.list_attached_group_policies(
                                    GroupName=group,
                                    Marker=group_attached_policies['Marker']
                                ))


                            if group_attached_policies['ResponseMetadata']:
                                del group_attached_policies['ResponseMetadata']

                            user['AttachedPolicies'] = group_attached_policies['AttachedPolicies']
                        except:
                            break

            except:
                pass

            try:
                user_policies = profile.list_user_policies(
                    UserName=iam_details['UserName']
                )

                while user_policies['IsTruncated']:
                    user_policies.update(profile.list_user_policies(
                        UserName=iam_details['UserName'],
                        Marker=user_policies['Marker']
                    ))

                if user_policies['ResponseMetadata']:
                    del user_policies['ResponseMetadata']

                iam_details['PolicyNames'] = user_policies['PolicyNames']
            except:
                pass

            try:
                user_attached_policies = profile.list_attached_user_policies(
                    UserName=iam_details['UserName']
                )

                while user_attached_policies['IsTruncated']:
                    user_attached_policies.update(profile.list_attached_user_policies(
                        UserName=iam_details['UserName'],
                        Marker=user_attached_policies['Marker']
                    ))

                if user_attached_policies['ResponseMetadata']:
                    del user_attached_policies['ResponseMetadata']

                iam_details['AttachedPolicies'] = user_attached_policies['AttachedPolicies']
            except:
                pass
            all_users_info = iam_details

        user_json = {
            "aws_username": all_users_info['UserName'],
            "aws_user_arn": all_users_info['Arn'],
            "aws_user_id": all_users_info['UserId'],
            "aws_user_create_date": all_users_info['CreateDate'],
            "aws_account_id": all_users_info['Arn'].split(":")[4],
            "aws_user_access_to_login_profile": [],
            "aws_user_managed_attached_policies": [],
            "aws_user_policies": [],
            "aws_user_path": all_users_info['Path'],
            "aws_user_groups": [],
            "aws_user_tags": []
        }
        if 'PasswordLastUsed' in all_users_info:
            user_json["aws_user_password_last_used"] = all_users_info['PasswordLastUsed']
            user_json["aws_user_access_to_login_profile"] = True
        else:
            user_json["aws_user_access_to_login_profile"] = False

        if 'PolicyNames' in all_users_info:
            user_json['aws_user_policies'] = all_users_info['PolicyNames']

        if 'GroupList' in all_users_info:
            user_json['aws_user_groups'] = all_users_info['GroupList']

        if 'UserPolicyList' in all_users_info:
            (user_json['aws_user_policies']).extend(all_users_info['UserPolicyList'])

        if 'AttachedManagedPolicies' in all_users_info:
            user_json['aws_user_managed_attached_policies'] = all_users_info['AttachedManagedPolicies']

        if 'AttachedPolicies' in all_users_info:
            user_json['aws_user_attached_policies'] = all_users_info['AttachedPolicies']

        if 'PermissionsBoundary' in all_users_info:
            user_json["aws_user_permission_boundary"] = all_users_info["PermissionsBoundary"]

        if 'Tags' in all_users_info:
            user_json['aws_user_tags'] = all_users_info['Tags']

        try:
            aws_user = AWSUsers.objects.get(aws_username=user_json['aws_username'])
            aws_user.modify(**user_json)
            aws_user.save()

        except DoesNotExist:
            AWSUsers(**user_json).save()

        except:
            e = sys.exc_info()[1]
            if "AWSUsers matching query does not exist" in e:
                return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
            else:
                return {"error": "Error from module: {}".format(str(e))}, 500

        title_name = "UserName"
        return {title_name: all_users_info}, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500

def all_users(profile):
    all_users_info = []
    try:
        # Get all users
        try:
            acc_auth = profile.get_account_authorization_details()
            user_details = acc_auth['UserDetailList']
            group_details = acc_auth['GroupDetailList']

            # Get access key last used
            for user in user_details:
                try:
                    access_key_last_used = profile.get_access_key_last_used(
                        AccessKeyId=user['UserId']
                    )
                    user_details['AccessKeyLastUsed'] = access_key_last_used
                except:
                    break

            # Get Group Inline Policies
            for user in user_details:
                for user_group in user_details['GroupList']:
                    for group in group_details:
                        if user_group == group['GroupName']:
                            user['GroupPolicyList'] = group['GroupPolicyList']

            # Get Group Attached Policies
            for user in user_details:
                for user_group in user_details['GroupList']:
                    for group in group_details:
                        if user_group == group['GroupName']:
                            user['GroupAttachedManagedPolicies'] = group['AttachedManagedPolicies']

            del user
            del group
            all_users_info = user_details
            del user_details
            del group_details
        except:
            # List Users
            iam_details = profile.list_users()
            while iam_details['IsTruncated']:
                iam_details = profile.list_users(Marker=iam_details['Marker'])

            json_data = iam_details['Users']

            # Get Groups of user
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

                    # List Group Policies
                    for group in user['GroupList']:
                        try:
                            group_attached_policies = profile.list_group_policies(
                                GroupName=group
                            )

                            while group_attached_policies['IsTruncated']:
                                group_attached_policies.update(profile.list_group_policies(
                                    GroupName=group,
                                    Marker=group_attached_policies['Marker']
                                ))

                            print(group_attached_policies)
                            if group_attached_policies['ResponseMetadata']:
                                del group_attached_policies['ResponseMetadata']

                            user['PolicyNames'] = group_attached_policies['PolicyNames']
                        except:
                            break

                        # List Attached Group Policies
                        for group in user['GroupList']:
                            try:
                                group_attached_policies = profile.list_attached_group_policies(
                                    GroupName=group
                                )

                                while group_attached_policies['IsTruncated']:
                                    group_attached_policies.update(profile.list_attached_group_policies(
                                        GroupName=group,
                                        Marker=group_attached_policies['Marker']
                                    ))


                                if group_attached_policies['ResponseMetadata']:
                                    del group_attached_policies['ResponseMetadata']

                                user['AttachedPolicies'] = group_attached_policies['AttachedPolicies']
                            except:
                                break

                except:
                    break


            for user in json_data:
                try:
                    user_policies = profile.list_user_policies(
                        UserName=user['UserName']
                    )

                    while user_policies['IsTruncated']:
                        user_policies.update(profile.list_user_policies(
                            UserName=user['UserName'],
                            Marker=user_policies['Marker']
                        ))

                    if user_policies['ResponseMetadata']:
                        del user_policies['ResponseMetadata']

                    user['PolicyNames'] = user_policies['PolicyNames']
                except:
                    break
            del user

            for user in json_data:
                try:
                    user_attached_policies = profile.list_attached_user_policies(
                        UserName=user['UserName']
                    )

                    while user_attached_policies['IsTruncated']:
                        user_attached_policies.update(profile.list_attached_user_policies(
                            UserName=user['UserName'],
                            Marker=user_attached_policies['Marker']
                        ))

                    if user_attached_policies['ResponseMetadata']:
                        del user_attached_policies['ResponseMetadata']

                    user['AttachedPolicies'] = user_attached_policies['AttachedPolicies']
                except:
                    break
            all_users_info = json_data

        del user

        for user in all_users_info:
            user_json = {
                "aws_username": user['UserName'],
                "aws_user_arn": user['Arn'],
                "aws_user_id": user['UserId'],
                "aws_user_create_date": user['CreateDate'],
                "aws_account_id": user['Arn'].split(":")[4],
                "aws_user_access_to_login_profile": [],
                "aws_user_managed_attached_policies": [],
                "aws_user_policies": [],
                "aws_user_path": user['Path'],
                "aws_user_groups": [],
                "aws_user_tags": []
            }
            if 'PasswordLastUsed' in user:
                user_json["aws_user_password_last_used"] = user['PasswordLastUsed']
                user_json["aws_user_access_to_login_profile"] = True
            else:
                user_json["aws_user_access_to_login_profile"] = False

            if 'PolicyNames' in user:
                user_json['aws_user_policies'] = user['PolicyNames']

            if 'GroupList' in user:
                user_json['aws_user_groups'] = user['GroupList']

            if 'UserPolicyList' in user:
                (user_json['aws_user_policies']).extend(user['UserPolicyList'])

            if 'AttachedManagedPolicies' in user:
                user_json['aws_user_managed_attached_policies'] = user['AttachedManagedPolicies']

            if 'AttachedPolicies' in user:
                user_json['aws_user_attached_policies'] = user['AttachedPolicies']

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

            except:
                e = sys.exc_info()[1]
                if "AWSUsers matching query does not exist" in e:
                    return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
                else:
                    return {"error": "Error from module: {}".format(str(e))}, 500

        title_name = "UserName"
        return {title_name: all_users_info}, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500

def exploit(profile):
    username = variables['USERNAME']['value']

    if username == "":
        return all_users(profile)
    else:
        return single_user(profile, username)