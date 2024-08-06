import string
import sys
import random

import flask_mongoengine

from core.database.models import AWSCredentials

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
        "description":"The user to add to the group"
	},
	"GROUP": {
		"value": "",
		"required": "true",
        "description":"The group to add the username to."
	}
}
description = "Create a 2nd access key to a user. To do this, the user needs to have only one access key. If the user has 2 access keys and OVERRIDE-OLDEST-ACCESS-KEY is set to true, the oldest created access key will be deleted and a new one will be created."

aws_command = "aws ec2 add-user-to-group --user-name {} --group {} --region {} --profile {}"

def exploit(profile, workspace):
	user = variables['USER']['value']
	group = variables['GROUP']['value']

	try:

		profile.add_user_to_group(
			GroupName=user,
			UserName=group
		)
		return {
			"AdditionStatus": f"User {user} added to group {group}"
		}
	except Exception as e:
		return {
			"error": str(e)
		}, 500


