import sys

from core.database.models import AWSGroups
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
    "GROUPNAME":{
		"value":"",
		"required":"false",
        "description":"A specific group to check."
	}
}

description = "List all users on the infrastructure and tries to get groups and policies."

calls = [
    'iam:GetAccountAuthorizationDetails',
    'iam:ListGroups',
    'iam:GetGroup',
    'iam:ListAttachedGroupPolicies',
    'iam:ListGroupPolicies',
]

aws_command = "aws iam list-users --region <region> --profile <profile>"


def all_users(profile):
    all_groups_info = []
    try:
        # Get all groups
        try:
            get_acc = profile.get_account_authorization_details()
            user_details = get_acc['UserDetailList']
            group_details = get_acc['GroupDetailList']

            for group in group_details:
                group['Users'] = []
                for user in user_details:
                    if group['GroupName'] in user_details['GroupList']:
                        (group['Users']).append(user['UserName'])

            all_groups_info = group_details
            del user_details
            del group_details
        except:
            # List Groups
            iam_details = profile.list_groups()
            while iam_details['IsTruncated']:
                iam_details = profile.list_groups(Marker=iam_details['Marker'])

            json_data = iam_details['Groups']

            # Get Groups of user
            for group in json_data:
                try:
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

                                print(group_attached_policies)
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

        del group

        for group in all_groups_info:
            group_json = {
                "aws_groupname": group['UserName'],
                "aws_group_arn": group['Arn'],
                "aws_group_id": group['UserId'],
                "aws_group_create_date": group['CreateDate'],
                "aws_account_id": group['Arn'].split(":")[4],
                "aws_group_attached_policies": [],
                "aws_group_policies": [],
                "aws_group_path": group['Path'],
                "aws_group_users": [],
                "aws_group_tags": []
            }

            if 'GroupPolicyList' in group:
                group_json['aws_group_policies'] = group['GroupPolicyList']

            if 'Users' in group:
                group_json['aws_group_users'] = group['GroupList']

            if 'GroupPolicyList' in group:
                group_json['aws_group_policies'] = group['GroupPolicyList']

            if 'AttachedManagedPolicies' in group:
                group_json['aws_group_attached_policies'] = group['AttachedManagedPolicies']

            try:
                aws_user = AWSGroups.objects.get(aws_groupname=group['GroupName'])
                aws_user.modify(**group_json)
                aws_user.save()

            except DoesNotExist:
                AWSGroups(**group_json).save()

            except:
                e = sys.exc_info()[1]
                if "AWSUsers matching query does not exist" in e:
                    return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
                else:
                    return {"error": "Error from module: {}".format(str(e))}, 500

        title_name = "UserName"
        return {title_name: all_groups_info}, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500

def exploit(profile):
    username = variables['USERNAME']['value']

    if username == "":
        return all_users(profile)
    else:
        pass
        #return single_user(username, profile)