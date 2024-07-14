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
		"value": "iam",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"USER-NAME": {
		"value": "ALL",
		"required": "true",
        "description":"The IAM User to check."
	}
}
description = "Disables a GD Detector on a specific region. Mind you, many security systems detect this behaviour."

aws_command = "aws iam get-user --user-name <user>  --region <region> --profile <profile>"

calls = [
	"iam:GetUser"
]

def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
	try:
		userName = variables['USER-NAME']['value']

		iamProfile = giveMeClient(
			all_sessions,
			cred_prof,
			useragent,
			web_proxies,
			"iam"
		)
		user = iamProfile.get_user(UserName=userName)["User"]

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

		return {"UserName": {"UserName": user['UserName'], "UserInfo": user}}

	except Exception as e:
		return {"error": str(e)}






