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
		"value": "ecr",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"REPO-NAME": {
		"value": "",
		"required": "true",
        "description":"Another variable to set"
	},
	"REGISTRY-ID": {
		"value": "",
		"required": "false",
        "description":"Another variable to set"
	},
	"TAG-STATUS": {
		"value": "ANY",
		"required": "false",
        "description":"Can be TAGGED, UNTAGGED, ANY"
	}
}
description = "Description of your Module"

aws_command = "aws ecr list-images --repository-name <repo name> --profile <profile>"


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
	tag_status = variables['TAG-STATUS']['value']
	if tag_status == 'TAGGED' or tag_status == 'UNTAGGED' or tag_status == 'ANY':
		n_tab = 0
		global output

		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		file = "{}_ecr_list_images".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)

		repo_name = variables['REPO-NAME']['value']
		reg_id = variables['REGISTRY-ID']['value']

		kwargs = {
			"repositoryName": repo_name,
			"filter": {
			'tagStatus': tag_status
			},
			"maxResults": 1000
		}

		if not reg_id == '':
			kwargs['registryId'] = reg_id

		response = profile.list_images(
			**kwargs
		)
		json_data = response['imageIds']

		while 'nextToken' in response:
			kwargs['nextToken'] = response['nextToken']
			response = profile.list_images(
				**kwargs
				)
			json_data.extend(response['imageIds'])


		with open(filename, 'w') as outfile:
			json.dump(json_data, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		if isinstance(json_data, list):
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			for data in json_data:
				list_dictionary(data, n_tab)
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		else:
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			list_dictionary(json_data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		pipepager(output, "less -R")
		output = ""