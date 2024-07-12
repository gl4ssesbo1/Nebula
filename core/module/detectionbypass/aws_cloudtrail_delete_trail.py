import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "cloudtrail",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"TRAIL-NAME": {
		"value": "",
		"required": "true",
        "description":"Specifies the name or the CloudTrail ARN of the trail for which CloudTrail will stop logging Amazon Web Services API calls."
	}
}
description = "Delete a CloudTrail Trail on a specific Region."

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	trailName = variables['TRAIL-NAME']['value']

	try:
		profile.delete_trail(
			Name=trailName
		)

		status = f"Successfully deleted CloudTrail Trail {trailName}"

	except:
		status = f"CloudTrail Trail {trailName} was not deleted with error code: {str(sys.exc_info()[1])}."

	return {
		"TrailName": {
			"TrailName": trailName,
			"Status": status
		}
	}

