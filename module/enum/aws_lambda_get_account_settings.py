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
	}
}

description = "Description of your Module"

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	try:
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		file = "{}_lambda_get_account_settings".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)
		workspaces = {}
		
		response = profile.get_account_settings()
		full_response = []
		full_response.append(response['AccountLimit'])
		full_response.append(response['AccountUsage'])

		with open(filename, 'w') as outfile:
			json.dump(full_response, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
		
		output = ""
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
		output += ("{}: \n".format(colored("Account Settings", "yellow", attrs=['bold'])))
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
			
		output += ("\t{}: \n".format(colored("AccountLimit", "yellow", attrs=['bold'])))
		for key,value in (response['AccountLimit']).items():
			output += ("\t\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"
		
		output += ("\t{}: \n".format(colored("AccountUsage", "yellow", attrs=['bold'])))
		for key,value in (response['AccountUsage']).items():
			output += ("\t\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"

		pipepager(output, cmd='less -R')

	except profile.exceptions.TooManyRequestsException:
		print(colored("[*] Too many requests sent. Only one does the job.", "red"))

	except profile.exceptions.InvalidParameterValueException:
		print(colored("[*] No other caracters other than _+=,.@- is allowed on the GroupName", "red"))

	except:
		e = sys.exc_info()
		print(colored("[*] {}".format(e), "red"))