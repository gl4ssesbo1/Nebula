import sys

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
		"value": "route53",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"HOSTED-ZONE-ID": {
		"value": "",
		"required": "true",
        "description":"The ID of the hosted zone to enumerate."
	}
}
description = "Get info on DNSSec configured on a Hosted Zone."

aws_command = "aws route53 get-dnssec --hosted-zone-id <id> --region <region> --profile <profile>"

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
	n_tab = 0
	global output

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_route53_list_hosted_zones".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	id = variables["HOSTED-ZONE-ID"]['value']

	response = profile.get_dnssec(
		HostedZoneId=id
	)
	del response['ResponseMetadata']
	json_data = response

	if response["Status"]['ServeSignature'] == 'NOT_SIGNING':
		print(colored("DNSSec is not configured for hosted zone: {}".format(id), "yellow"))

	if response["Status"]['ServeSignature'] == 'DELETING':
		print(colored("DNSSec is in the process of deleting for hosted zone: {}".format(id), "yellow"))

	if response["Status"]['ServeSignature'] == 'ACTION_NEEDED':
		print(colored("DNSS has an issue for hosted zone: {}".format(id), "yellow"))

	if response["Status"]['ServeSignature'] == 'INTERNAL_FAILURE':
		print(colored("DNSS has an internal issue with the request for hosted zone: {}".format(id), "yellow"))

	elif response["Status"]['ServeSignature'] == 'SIGNING':
		print(colored("DNSSec is configured for hosted zone: {}".format(id), "yellow"))
		if isinstance(json_data, list):
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			for data in json_data:
				output += colored("ID: {}\n".format(id), "yellow", attrs=['bold'])
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
				list_dictionary(data, n_tab)
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		else:
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			output += colored("ID: {}\n".format(id), "yellow", attrs=['bold'])
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			list_dictionary(json_data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		print(output)
		output = ""

	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))