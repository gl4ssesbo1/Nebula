import boto3
from termcolor import colored
from datetime import datetime
import json
import sys
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
		"value": "lambda",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"FUNCTIONNAME": {
		"value": "",
		"required": "true",
        "description":"Another variable to set"
	},
	"FUNCTIONVERSION": {
		"value": "",
		"required": "false",
        "description":"Another variable to set"
	}
}

description = "Description of your Module"

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	try:
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		file = "{}_lambda_list_alias".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)
		workspaces = {}
		functionname = variables['FUNCTIONNAME']['value']
		functionversion = variables['FUNCTIONVERSION']['value']

		if not functionversion == "":
			response = profile.list_aliases(
				FunctionName=functionname,
				FunctionVersion=functionversion,
				MaxItems=10000
			)['Aliases']
		else:
			response = profile.list_aliases(
				FunctionName=functionname,
				MaxItems=10000
			)['Aliases']

		if not response:
			print(colored("[*] There are no aliases for this function.", "green"))
		else:
			with open(filename, 'w') as outfile:
				json.dump(response, outfile, indent=4, default=str)
				print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

			output = ""
			for alias in response:
				output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
				output += ("{}: {}\n".format(colored("Name", "yellow", attrs=['bold']), alias['Name']))
				output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
				for key,value in alias.items():
					if key == 'RoutingConfig':
						output += ("\t{}: \n".format(colored("RoutingConfig", "red", attrs=['bold'])))
						for k,v in value.items():
							output += ("\t\t{}: {}\n".format(colored(k, "blue", attrs=['bold']), colored(v, "yellow")))
					else:
						output += ("\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
			output += "\n"
			pipepager(output, cmd='less -R')
	
	except profile.exceptions.ResourceNotFoundException:
		print(colored("[*] The function does not exist. Check the name.", "red"))
	
	except:
		e = sys.exc_info()
		print(colored("[*] {}".format(e), "red"))