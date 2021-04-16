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
	"SERVICE":{
		"value":"ec2",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "INSTANCE-ID":{
		"value":"",
		"required":"true",
        "description":"The ID of the instance from "
	}
}

description = "Retrieves the configuration data of the specified instance. Uses get_launch_template_data API."

aws_command = "aws ec2 get-launch-template-data --instance-id <instance-id> --query 'LaunchTemplateData' --region <region> --profile <profile>"

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]
output = ""

def list_dictionary(d, n_tab):
	global output
	if isinstance(d, list):
		n_tab += 1
		for i in d:
			if not isinstance(i, list) and not isinstance(i, dict):
				output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
			else:
				list_dictionary(i, n_tab)
	elif isinstance(d, dict):
		n_tab+=1
		for key, value in d.items():
			if not isinstance(value, dict) and not isinstance(value, list):
				output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
			else:
				output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
				list_dictionary(value, n_tab)

def exploit(profile, workspace):
	global output
	n_tab = 0
	
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_get_launch_templates".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	instance_id = variables['INSTANCE-ID']['value']
	response = profile.get_launch_template_data(
		InstanceId=instance_id
	)

	json_data = response['LaunchTemplateData']
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	if isinstance(json_data, list):
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		for data in json_data:
			output += ("{}: {}\n".format(colored("LaunchTemplateName", "yellow", attrs=['bold']), instance_id))
			list_dictionary(data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	else:
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		output += ("{}: {}\n".format(colored("LaunchTemplateName", "yellow", attrs=['bold']), instance_id))
		list_dictionary(json_data, n_tab)
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	print(output)
	output = ""