import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

'''
    If you want to be recognized about your contribution, you can add your name/nickname and contacts here. It will be outputed when user types "options".
'''
author = {
    "name":"",
    "twitter":"",
    "github":"",
    "email":""
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"INCLUDE-RESOLVED-CASES": {
		"value": "True",
		"required": "true",
        "description":"Specifies whether to include resolved support cases in the DescribeCases response. If set to False, resolved cases won't be included."
	},
	"INCLUDE-COMMUNICATIONS": {
		"value": "True",
		"required": "true",
        "description":"Specifies whether to include communications in the DescribeCases response. By default, communications are included."
	},
	"CASE-IDS": {
		"value": "",
		"required": "false",
        "description":"A list of ID numbers of the support cases you want returned, split by comma (,). The maximum number of cases is 100. Either put this or CASE-WORDLIST. Not both."
	},
	"CASE-WORDLIST": {
		"value": "",
		"required": "false",
        "description":"The path to a wordlist of ID numbers of the support cases you want returned. The maximum number of cases is 100. Either put this or CASE-IDS. Not both."
	},
	"BEFORE-DATE": {
		"value": "",
		"required": "false",
        "description":"The end date for a filtered date search on support case communications. Case communications are available for 12 months after creation."
	},
	"AFTER-DATE": {
		"value": "",
		"required": "false",
        "description":"The start date for a filtered date search on support case communications. Case communications are available for 12 months after creation.."
	}
}
description = "Returns a list of cases that you specify by passing one or more case IDs. Case data is available for 12 months after creation. If a case was created more than 12 months ago, a request might return an error."

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"


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
	file = "{}_ec2_enum_describe_support_cases".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	arguments = {}

	include_resolved_cases = variables['INCLUDE-RESOLVED-CASES']['value']
	include_communications = variables['INCLUDE-COMMUNICATIONS']['value']

	case_id = variables['CASE-IDS']['value']
	case_wordlist = variables['CASE-WORDLIST']['value']

	before = variables['BEFORE-DATE']['value']
	after = variables['AFTER-DATE']['value']

	if not case_id == "" and not case_wordlist == "":
		print(colored("[*] Either put CASE-IDS or CASE-WORDLIST. Not both.", "red"))

	else:
		if not case_id == "":
			case_ids = case_id.split(",")
			arguments['caseIdList'] = case_ids

		elif not case_wordlist == "":
			case_ids = []
			casefile = open(case_wordlist, 'r')
			for line in casefile.readlines():
				case_ids.append(line.strip().replace("\n", ""))
			arguments['caseIdList'] = case_ids

		arguments['includeResolvedCases'] = include_resolved_cases
		arguments['includeCommunications'] = include_communications

		if not after == "":
			arguments['afterTime'] = after

		if not before == "":
			arguments['beforeTime'] = before

		response = profile.describe_cases(
			**arguments
		)

		json_data = response['cases']

		while "nextToken" in response:
			arguments['nextToken'] = response['nextToken']
			response = profile.describe_cases(
				**arguments
			)
			json_data.extend(response['cases'])

		with open(filename, 'w') as outfile:
			json.dump(json_data, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		title_name = "caseId"
		if isinstance(json_data, list):
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			for data in json_data:
				output += colored("{}: {}\n".format(title_name, data[title_name]), "yellow", attrs=['bold'])
				list_dictionary(data, n_tab)
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		else:
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
			list_dictionary(json_data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		pipepager(output, "less -R")