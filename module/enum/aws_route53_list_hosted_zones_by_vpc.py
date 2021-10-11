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
	"VPC-ID": {
		"value": "",
		"required": "true",
        "description":"The ID of the VPC to test it against."
	},
	"VPC-REGION": {
		"value": "",
		"required": "false",
        "description":"The region of the VPC to test it against."
	}
}
description = "Get Hosted Zone info by providing a DNS Host-Name."

aws_command = "aws route53 list-hosted-zones-by-name --dns-name <host dns> --region <region> --profile <profile>"

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

	id = variables['VPC-ID']['value']
	region = variables['VPC-REGION']['value']

	response = profile.list_hosted_zones_by_vpc(
		VPCId=id,
		VPCRegion=region
	)

	while response['NextToken']:
		response.extend(profile.list_hosted_zones_by_vpc(
			VPCId=id,
			VPCRegion=region,
			NextToken=response['NextToken']
			)
		)

	json_data = response
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	if isinstance(json_data, list):
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		for data in json_data:
			output += colored("VPCId: {}\n".format(id), "yellow", attrs=['bold'])
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			list_dictionary(data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	else:
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		output += colored("VPCId: {}\n".format(id), "yellow", attrs=['bold'])
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		list_dictionary(json_data, n_tab)
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	print(output)
	output = ""

