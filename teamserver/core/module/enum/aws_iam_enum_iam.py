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
			iamData['UserDetailList'] = result['UserDetailList']
			iamData['GroupDetailList'] = result['GroupDetailList']
			iamData['RoleDetailList'] = result['RoleDetailList']
			iamData['Policies'] = result['Policies']

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
			savePolicyData(iamData)

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
				savePolicyData(iamData)

			elif resourceType == "AWSPOLICIES":
				savePolicyData(iamData)

			return {"ResourceType": {"ResourceType": resourceType, iamDataFilter: iamData[iamDataFilter]}}

	except Exception as e:
		if "AccessDenied" in str(e):
			otherGetIAM(profile, resourceType)
		else:
			return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

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

			except Exception as e:
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveGroupData(iamData):
	if len(iamData['GroupDetailList']) > 0:
		for group in iamData['GroupDetailList']:
			database_data = {
				"aws_groupname": group['GroupName'],
				"aws_group_arn": group['Arn'],
				"aws_group_id": group['GroupId'],
				"aws_group_path": group['Path'],
				"aws_group_create_date": group['CreateDate'],
			}

			if "AttachedManagedPolicies" in group:
				database_data["aws_group_attached_policies"] = group['AttachedManagedPolicies']

			if "GroupPolicyList" in group:
				database_data["aws_group_policies"] = group['GroupPolicyList']

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

			except Exception as e:
				return {"error": "Error from module: {}".format(str(e))}, 500

def saveRoleData(iamData):
	if len(iamData['RoleDetailList']) > 0:
		for role in iamData['RoleDetailList']:
			database_data = {
				"aws_rolename": role['RoleName'],
				"aws_role_arn": role['Arn'],
				"aws_role_id": role['RoleId'],
				"aws_role_path": role['Path'],
				"aws_role_create_date": role['CreateDate'],
				"aws_role_account_id": role['Arn'].split(":")[4]
			}

			if "AttachedManagedPolicies" in role:
				database_data["aws_role_attached_policies"] = role['AttachedManagedPolicies']

			if "RolePolicyList" in role:
				database_data["aws_role_policies"] = role['RolePolicyList']

			if "AssumeRolePolicyDocument" in role:
				database_data['aws_role_assume_role_policy'] = role['AssumeRolePolicyDocument']

			if "Tags" in role:
				database_data["aws_role_tags"] = role['Tags']

			try:
				aws_role = AWSRoles.objects.get(aws_rolename=role['RoleName'])
				aws_role.modify(**database_data)
				aws_role.save()

			except DoesNotExist:
				AWSRoles(**database_data).save()

			except Exception as e:
				return {"error": "Error from module: {}".format(str(e))}, 500


def savePolicyData(iamData):
	if len(iamData['Policies']) > 0:
		for policy in iamData['Policies']:
			database_data = {
				"aws_policy_name": policy['PolicyName'],
				"aws_policy_arn": policy['Arn'],
				"aws_policy_id": policy['PolicyId'],
				"aws_policy_path": policy['Path'],
				"aws_policy_create_date": policy['CreateDate'],
				"aws_policy_update_date": policy['UpdateDate']
			}

			if "DefaultVersionId" in policy:
				database_data["aws_policy_default_version"] = policy['DefaultVersionId']

			if policy['Arn'].split(":")[4] == "aws":
				database_data["aws_policy_scope"] = "AWS"
			else:
				database_data["aws_policy_scope"] = "Local"

			if "PermissionsBoundaryUsageCount" in policy:
				database_data["aws_policy_permission_boundary_usage_count"] = policy['PermissionsBoundaryUsageCount']

			if "AttachmentCount" in policy:
				database_data["aws_policy_attachment_count"] = policy['AttachmentCount']

			if "PolicyVersionList" in policy:
				database_data["aws_policy_documents"] = policy['PolicyVersionList']

			if "IsAttachable" in policy:
				database_data["aws_policy_is_attachable"] = policy['IsAttachable']

			try:
				aws_policy = AWSPolicies.objects.get(aws_policy_name=policy['PolicyName'])
				aws_policy.modify(**database_data)
				aws_policy.save()

			except DoesNotExist:
				AWSPolicies(**database_data).save()

			except Exception as e:
				return {"error": "Error from module: {}".format(str(e))}, 500

def otherGetUsers(profile, resourceType):
	iamData = []
	userinfo = {}
	try:
		userlist = profile.list_users()['Users']

	except Exception as e:
		return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

	for user in userlist:
		try:
			userinfo = profile.get_user(
				User=user['UserName']
			)['User']

		except Exception as e:
			pass
		try:
			userGroups = profile.list_groups_for_user(
				User=user['UserName']
			)['Groups']
			userinfo['Groups'] = userGroups

		except Exception as e:
			pass

		try:
			userInlinePolicies = profile.list_user_policies(
				User=user['UserName']
			)['PolicyNames']
			userinfo['UserPolicyList'] = userInlinePolicies

		except Exception as e:
			pass

		try:
			userAttachedPolicies = profile.list_attached_user_policies(
				User=user['UserName']
			)['AttachedPolicies']
			userinfo['AttachedPolicies'] = userAttachedPolicies

		except Exception as e:
			pass

		iamData.append(userinfo)

	return {"ResourceType": {"ResourceType": resourceType, "UserDetailList": iamData}}

def otherGetGroups(profile, resourceType):
	groupInfo = {}
	iamData = []

	try:
		groupList = profile.list_groups()['Groups']

	except Exception as e:
		return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

	for group in groupList:
		try:
			groupInfo = profile.get_group(
				GroupName=group['GroupName']
			)

		except Exception as e:
			pass

		try:
			groupUsers = profile.list_group_users(
				GroupName=group['GroupName']
			)
			groupInfo['Users'] = groupUsers

		except Exception as e:
			pass

		try:
			groupPolicies = profile.list_group_policies(
				GroupName=group['GroupName']
			)['PolicyNames']
			groupInfo['AttachedPolicies'] = groupPolicies

		except Exception as e:
			pass

		try:
			groupAttachedPolicies = profile.list_attached_group_policies(
				GroupName=group['GroupName']
			)['AttachedPolicies']
			groupInfo['AttachedPolicies'] = groupAttachedPolicies

		except Exception as e:
			pass

		iamData.append(groupInfo)

	return {"ResourceType": {"ResourceType": resourceType, "GroupDetailList": iamData}}

def otherGetRoles(profile, resourceType):
	try:
		iamData = profile.list_roles()['Roles']

	except Exception as e:
		return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

	for role in iamData:
		try:
			roleInlinePolicies = profile.list_user_policies(
				User=role['RoleName']
			)['PolicyNames']
			role['InlinePolicies'] = roleInlinePolicies

		except Exception as e:
			pass

		try:
			roleAttachedPolicies = profile.list_attached_user_policies(
				User=role['RoleName']
			)['AttachedPolicies']
			role['AttachedPolicies'] = roleAttachedPolicies

		except Exception as e:
			pass

	return {"ResourceType": {"ResourceType": resourceType, "RoleDetailList": iamData}}

def otherGetLocalPolicies(profile, resourceType):
	iamData = []
	policyInfo = {}
	try:
		policyList = profile.list_policies(Scope="Local")['Policies']
		for policy in policyList:
			try:
				policyInfo = profile.get_policy(PolicyArn=policy['Arn'])["Policy"]
			except Exception as e:
				pass

			try:
				policyInfo = profile.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId'])["Policy"]
			except Exception as e:
				pass

			iamData.append(policyInfo)

		return {"ResourceType": {"ResourceType": resourceType, "LocalPolicies": iamData}}

	except Exception as e:
		return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

def otherGetAWSPolicies(profile, resourceType):
	iamData = []
	policyInfo = {}
	try:
		policyList = profile.list_policies(Scope="AWS")['Policies']
		for policy in policyList:
			try:
				policyInfo = profile.get_policy(PolicyArn=policy['Arn'])["Policy"]
			except Exception as e:
				pass

			try:
				policyInfo = profile.get_policy_version(PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId'])[
					"Policy"]
			except Exception as e:
				pass

			iamData.append(policyInfo)

		return {"ResourceType": {"ResourceType": resourceType, "LocalPolicies": iamData}}

	except Exception as e:
		return {"error": f"Error listing IAM Resources with error code: {str(e)}."}

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

