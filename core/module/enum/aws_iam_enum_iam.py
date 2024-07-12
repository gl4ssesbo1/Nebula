import sys

from mongoengine import DoesNotExist

from core.database.models import AWSUsers
from core.database.models import AWSGroups
from core.database.models import AWSRoles
from core.database.models import AWSPolicies

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
	"RESOURCE-TYPE": {
		"value": "ALL",
		"required": "true",
        "description":"The IAM Resource Type. It can be USERS, GROUPS, ROLES, LOCALPOLICIES, AWSPOLICIES, or ALL"
	}
}
description = "Disables a GD Detector on a specific region. Mind you, many security systems detect this behaviour."

aws_command = "aws iam get-account-authorization-details  --region <region> --profile <profile>"

calls = [
	"iam:GetAccountAuthorizationDetails",
	"or",
	"iam:ListUsers",
	"iam:ListGroups",
	"iam:ListRoles",
	"iam:ListPolicies",
	"iam:ListAttachedUserPolicies",
	"iam:ListAttachedRolePolicies",
	"iam:ListAttachedGroupPolicies",
	"iam:ListUserPolicies",
	"iam:ListGroupPolicies",
	"iam:ListRolePolicies",
	"iam:ListGroupsForUser"
]

def exploit(profile, workspace):
	resourceType = variables['RESOURCE-TYPE']['value']

	try:
		iamDataFilter = ""
		if resourceType == "USERS":
			filter = "User"
			iamDataFilter = "UserDetailList"
		elif resourceType == "GROUPS":
			filter = "Group"
			iamDataFilter = "GroupDetailList"
		elif resourceType == "ROLES":
			filter = "Role"
			iamDataFilter = "RoleDetailList"
		elif resourceType == "ALL":
			filter = None
		elif resourceType == "LOCALPOLICIES":
			filter = "LocalManagedPolicy"
			iamDataFilter = "Policies"
		elif resourceType == "AWSPOLICIES":
			filter = "AWSManagedPolicy"
			iamDataFilter = "Policies"
		else:
			return {
				"error": "RESOURCE-TYPE should be either USERS, GROUPS, ROLES, LOCALPOLICIES, AWSPOLICIES, or ALL"
			}
		iamData = {
			"UserDetailList": [],
			"GroupDetailList": [],
			"RoleDetailList": [],
			"Policies": []
		}
		if filter is None:
			result = profile.get_account_authorization_details()
			iamData['UserDetailList'].extend(result['UserDetailList'])
			iamData['GroupDetailList'].extend(result['GroupDetailList'])
			iamData['RoleDetailList'].extend(result['RoleDetailList'])
			iamData['Policies'].extend(result['Policies'])

			while result['IsTruncated']:
				result = profile.get_account_authorization_details(
					Marker=result['Marker']
				)
				iamData['UserDetailList'].extend(result['UserDetailList'])
				iamData['GroupDetailList'].extend(result['GroupDetailList'])
				iamData['RoleDetailList'].extend(result['RoleDetailList'])
				iamData['Policies'].extend(result['Policies'])

			saveUserData(iamData)
			saveGroupData(iamData)
			saveRoleData(iamData)
			saveLocalPolicyData(iamData)
			saveAWSPolicyData(iamData)

		else:
			args = {
				"Filter": [
					filter
				]
			}

			result = profile.get_account_authorization_details(
				**args
			)
			iamData[iamDataFilter].extend(result[iamDataFilter])
			while result['IsTruncated']:
				args = {
					"Filter": [
						filter
					],
					"Marker": result['Marker']
				}
				result = profile.get_account_authorization_details(
					**args
				)
				iamData['UserDetailList'].extend(result[iamDataFilter])

		if resourceType == "ALL":
			return {"ResourceType": {"ResourceType": resourceType, "IAMData": iamData}}
		else:
			if resourceType == "USERS":
				saveUserData(iamData)

			elif resourceType == "GROUPS":
				saveGroupData(iamData)

			elif resourceType == "ROLES":
				saveRoleData(iamData)

			elif resourceType == "LOCALPOLICIES":
				saveLocalPolicyData(iamData)

			elif resourceType == "AWSPOLICIES":
				saveAWSPolicyData(iamData)

			return {"ResourceType": {"ResourceType": resourceType, iamDataFilter: iamData[iamDataFilter]}}

	except:
		if "AccessDenied" in str(sys.exc_info()):
			otherGetIAM(profile, resourceType)
		else:
			return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

def saveUserData(iamData):
	if len(iamData['UserDetailList']) > 0:
		for user in iamData['UserDetailList']:
			database_data = {
				"aws_username": user['UserName'],
				"aws_user_arn": user['Arn'],
				"aws_user_id": user['UserId'],
				"aws_user_path": user['Path'],
				"aws_user_create_date": user['CreateDate'],
				"aws_account_id": user['Arn'].split(":")[4]
			}

			if "AttachedManagedPolicies" in user:
				database_data["aws_user_attached_policies"] = user['AttachedManagedPolicies']

			if "UserPolicyList" in user:
				database_data["aws_user_policies"] = user['UserPolicyList']

			if "GroupList" in user:
				database_data["aws_user_groups"] = user['GroupList']

			if "Tags" in user:
				database_data["aws_user_tags"] = user['Tags']

			try:
				aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
				aws_user.modify(**database_data)
				aws_user.save()

			except DoesNotExist:
				AWSUsers(**database_data).save()

			except:
				e = sys.exc_info()
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveGroupData(iamData):
	if len(iamData['GroupDetailList']) > 0:
		for group in iamData['GroupDetailList']:
			database_data = {
				"aws_groupname": group['GroupName'],
				"aws_group_arn": group['Arn'],
				"aws_group_id": group['UserId'],
				"aws_group_path": group['Path'],
				"aws_group_create_date": group['CreateDate'],
			}

			if "AttachedManagedPolicies" in group:
				database_data["aws_group_attached_policies"] = group['AttachedManagedPolicies']

			if "GroupPolicyList" in group:
				database_data["aws_group_policies"] = group['UserPolicyList']

			if "Users" in group:
				database_data["aws_group_users"] = group['Users']

			if "Tags" in group:
				database_data["aws_group_tags"] = group['Tags']

			try:
				aws_user = AWSGroups.objects.get(aws_groupname=group['GroupName'])
				aws_user.modify(**database_data)
				aws_user.save()

			except DoesNotExist:
				AWSGroups(**database_data).save()

			except:
				e = sys.exc_info()
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveRoleData(iamData):
	if len(iamData['UserDetailList']) > 0:
		for user in iamData['UserDetailList']:
			database_data = {
				"aws_rolename": user['UserName'],
				"aws_user_arn": user['Arn'],
				"aws_user_id": user['UserId'],
				"aws_user_path": user['Path'],
				"aws_user_create_date": user['CreateDate'],
				"aws_account_id": user['Arn'].split(":")[4]
			}

			if "AttachedManagedPolicies" in user:
				database_data["aws_user_attached_policies"] = user['AttachedManagedPolicies']

			if "UserPolicyList" in user:
				database_data["aws_user_policies"] = user['UserPolicyList']

			if "GroupList" in user:
				database_data["aws_user_groups"] = user['GroupList']

			if "Tags" in user:
				database_data["aws_user_tags"] = user['Tags']

			try:
				aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
				aws_user.modify(**database_data)
				aws_user.save()

			except DoesNotExist:
				AWSUsers(**database_data).save()

			except:
				e = sys.exc_info()
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveAWSPolicyData(iamData):
	if len(iamData['UserDetailList']) > 0:
		for user in iamData['UserDetailList']:
			database_data = {
				"aws_username": user['UserName'],
				"aws_user_arn": user['Arn'],
				"aws_user_id": user['UserId'],
				"aws_user_path": user['Path'],
				"aws_user_create_date": user['CreateDate'],
				"aws_account_id": user['Arn'].split(":")[4]
			}

			if "AttachedManagedPolicies" in user:
				database_data["aws_user_attached_policies"] = user['AttachedManagedPolicies']

			if "UserPolicyList" in user:
				database_data["aws_user_policies"] = user['UserPolicyList']

			if "GroupList" in user:
				database_data["aws_user_groups"] = user['GroupList']

			if "Tags" in user:
				database_data["aws_user_tags"] = user['Tags']

			try:
				aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
				aws_user.modify(**database_data)
				aws_user.save()

			except DoesNotExist:
				AWSUsers(**database_data).save()

			except:
				e = sys.exc_info()
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveLocalPolicyData(iamData):
	if len(iamData['UserDetailList']) > 0:
		for user in iamData['UserDetailList']:
			database_data = {
				"aws_username": user['UserName'],
				"aws_user_arn": user['Arn'],
				"aws_user_id": user['UserId'],
				"aws_user_path": user['Path'],
				"aws_user_create_date": user['CreateDate'],
				"aws_account_id": user['Arn'].split(":")[4]
			}

			if "AttachedManagedPolicies" in user:
				database_data["aws_user_attached_policies"] = user['AttachedManagedPolicies']

			if "UserPolicyList" in user:
				database_data["aws_user_policies"] = user['UserPolicyList']

			if "GroupList" in user:
				database_data["aws_user_groups"] = user['GroupList']

			if "Tags" in user:
				database_data["aws_user_tags"] = user['Tags']

			try:
				aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
				aws_user.modify(**database_data)
				aws_user.save()

			except DoesNotExist:
				AWSUsers(**database_data).save()

			except:
				e = sys.exc_info()
				return {"error": "Error from module: {}".format(str(e))}, 500

def otherGetUsers(profile, resourceType):
	try:
		iamData = profile.list_users()['Users']

	except:
		return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

	for user in iamData:
		try:
			userGroups = profile.list_groups_for_user(
				User=user['UserName']
			)['Groups']
			user['Groups'] = userGroups

		except:
			pass

		try:
			userInlinePolicies = profile.list_user_policies(
				User=user['UserName']
			)['PolicyNames']
			user['InlinePolicies'] = userInlinePolicies

		except:
			pass

		try:
			userAttachedPolicies = profile.list_attached_user_policies(
				User=user['UserName']
			)['AttachedPolicies']
			user['AttachedPolicies'] = userAttachedPolicies

		except:
			pass

	return {"ResourceType": {"ResourceType": resourceType, "UserDetailList": iamData}}

def otherGetGroups(profile, resourceType):
	try:
		iamData = profile.list_roles()['Groups']

	except:
		return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

	for group in iamData:
		try:
			groupInfo = profile.get_group(
				GroupName=group['GroupName']
			)
			group['Users'] = groupInfo['Users']

		except:
			pass

		try:
			groupPolicies = profile.list_group_policies(
				GroupName=group['GroupName']
			)['PolicyNames']
			group['AttachedPolicies'] = groupPolicies

		except:
			pass

		try:
			groupAttachedPolicies = profile.list_attached_group_policies(
				GroupName=group['GroupName']
			)['AttachedPolicies']
			group['AttachedPolicies'] = groupAttachedPolicies

		except:
			pass

	return {"ResourceType": {"ResourceType": resourceType, "GroupDetailList": iamData}}

def otherGetRoles(profile, resourceType):
	try:
		iamData = profile.list_roles()['Roles']

	except:
		return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

	for role in iamData:
		try:
			roleInlinePolicies = profile.list_user_policies(
				User=role['RoleName']
			)['PolicyNames']
			role['InlinePolicies'] = roleInlinePolicies

		except:
			pass

		try:
			roleAttachedPolicies = profile.list_attached_user_policies(
				User=role['RoleName']
			)['AttachedPolicies']
			role['AttachedPolicies'] = roleAttachedPolicies

		except:
			pass

	return {"ResourceType": {"ResourceType": resourceType, "RoleDetailList": iamData}}

def otherGetLocalPolicies(profile, resourceType):
	try:
		iamData = profile.list_policies(Scope="Local")['Policies']
		return {"ResourceType": {"ResourceType": resourceType, "LocalPolicies": iamData}}

	except:
		return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

def otherGetAWSPolicies(profile, resourceType):
	try:
		iamData = profile.list_policies(Scope="AWS")['Policies']
		return {"ResourceType": {"ResourceType": resourceType, "AWSPolicies": iamData}}

	except:
		return {"error": f"Error listing IAM Resources with error code: {str(sys.exc_info())}."}

def otherGetIAM(profile, resourceType):
	if resourceType == "USERS":
		return otherGetUsers(profile=profile, resourceType=resourceType)

	elif resourceType == "GROUPS":
		return otherGetGroups(profile=profile, resourceType=resourceType)

	elif resourceType == "ROLES":
		return otherGetRoles(profile=profile, resourceType=resourceType)

	elif resourceType == "ALL":
		iamData = {
			'UserDataList': otherGetUsers(profile=profile, resourceType="USERS")['ResourceType']['UserDetailList'],
			'GroupDataList': otherGetUsers(profile=profile, resourceType="GROUPS")['ResourceType']['GroupDetailList'],
			'RoleDataList': otherGetUsers(profile=profile, resourceType="ROLES")['ResourceType']['RoleDetailList'],
			'LocalPolicies': otherGetUsers(profile=profile, resourceType="LOCALPOLICIES")['ResourceType']['LocalPolicies'],
			'AWSPolicies': otherGetUsers(profile=profile, resourceType="AWSPOLICIES")['ResourceType']['AWSPolicies']
		}

		return {"ResourceType": {"ResourceType": resourceType, "IAMData": iamData}}

	elif resourceType == "LOCALPOLICIES":
		return otherGetLocalPolicies(profile=profile, resourceType=resourceType)

	elif resourceType == "AWSPOLICIES":
		return otherGetAWSPolicies(profile=profile, resourceType=resourceType)
	else:
		return {
			"error": "RESOURCE-TYPE should be either USERS, GROUPS, ROLES, LOCALPOLICIES, AWSPOLICIES, or ALL"
		}

