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
		"value": "ec2",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	}
}

description = "List all ec2 images. Needs credentials of an IAM with DescribeImages right. Output is dumpled on a file. It takes a sh*tload of time, unfortunately. And boy, is it a huge output."

aws_command = "aws ec2 describe-images --image-ids <image id> --region <region> --profile <profile>"

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_images".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)
	workspaces = {}
	try:
		inst = profile.describe_images()
		workspaces["Images"] = inst["Images"]

		with open(filename, 'w') as outfile:
			json.dump(workspaces, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	except:
		print(colored("[*] You have no rights to Describe Images. ", "red"))

