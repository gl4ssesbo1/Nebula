import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import requests, zipfile, io
import urllib
import os
from colorama import init
init()

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
	}
}

description = "Description of your Module"

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	try:
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		file = "{}_lambda_get_policy".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)
		
		functionname = variables['FUNCTIONNAME']['value']
		
		response = profile.get_policy(FunctionName=functionname)
		full_response = []
		full_response.append(response['RevisionId'])
		full_response.append(response['Policy'])

		with open(filename, 'w') as outfile:
			json.dump(full_response, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		output = ""
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
		output += ("{}: {}\n".format(colored("FunctionName", "yellow", attrs=['bold']), functionname))
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))

		output += ("\t\t{}: {}\n".format(colored("Policy", "red", attrs=['bold']), colored(response['Policy'], "blue")))
		output += ("\t\t{}: {}\n".format(colored("RevisionId", "red", attrs=['bold']), colored(response['RevisionId'], "blue")))

		output += "\n"

		print(output)
		
	except profile.exceptions.TooManyRequestsException:
		print(colored("[*] Too many requests sent. Only one does the job.", "red"))

	except profile.exceptions.InvalidParameterValueException:
		print(colored("[*] No other caracters other than _+=,.@- is allowed on the GroupName", "red"))
		
	except:
		e = sys.exc_info()
		print(colored("[*] {}".format(e), "red"))