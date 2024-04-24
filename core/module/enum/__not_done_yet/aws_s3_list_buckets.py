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
	"SERVICE":{
		"value":"s3",
		"required":"true",
    	"description":"The service that will be used to run the module. It cannot be changed."
	}
}

description = "List s3 buckets that are accessible from the IAM provided or public to all. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws s3api list-buckets --query \"Buckets[].Name\" --region <region> --profile <profile>"

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_s3_list_buckets".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)
	json_data = {}

	response = profile.list_buckets()
	json_data['Owner'] = response['Owner']
	json_data['Buckets'] = response['Buckets']

	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	print (colored("Owner:","yellow",attrs=['bold']))
	print (colored("-----------", "yellow", attrs=["bold"]))
	for x,y in (response['Owner']).items():
		print("\t{}:\t{}".format(colored(x,"red"),colored(y,"blue")))
	print()
	print (colored("Buckets:","yellow",attrs=['bold']))
	print (colored("-----------", "yellow", attrs=["bold"]))
	for buckets in response['Buckets']:
		for x,y in buckets.items():
			print("\t{}:\t{}".format(colored(x,"red"),colored(y,"blue")))
		print(colored("\t--------------------------------------------", "yellow", attrs=["bold"]))
