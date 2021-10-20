import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import requests, zipfile, io
import urllib
import os
import sys
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
	},
	"DOWNLOADPATH": {
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
		file = "{}_lambda_get_function".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)
		workspaces = {}
		
		functionname = variables['FUNCTIONNAME']['value']
		response = profile.get_function(FunctionName=functionname)

		full_response = []
		full_response.append(response['Configuration'])
		full_response.append(response['Code'])
		full_response.append(response['Tags'])

		with open(filename, 'w') as outfile:
			json.dump(full_response, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
		
		output = ""
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
		output += ("{}: {}\n".format(colored("FunctionName", "yellow", attrs=['bold']), response['Configuration']['FunctionName']))
		output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
			
		output += ("\t{}: \n".format(colored("Configuration", "yellow", attrs=['bold'])))
		for key,value in (response['Configuration']).items():
			if key == 'TracingConfig':
				output += ("\t\t{}: \n".format(colored("TracingConfig", "red", attrs=['bold'])))
				for k,v in value.items():
					output += ("\t\t\t{}: {}\n".format(colored(k, "blue", attrs=['bold']), colored(v, "yellow")))
			else:
				output += ("\t\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"
		
		output += ("\t{}: \n".format(colored("Code", "yellow", attrs=['bold'])))
		for key,value in (response['Code']).items():
			output += ("\t\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"

		output += ("\t{}: \n".format(colored("Tags", "yellow", attrs=['bold'])))
		for key,value in (response['Tags']).items():
			output += ("\t\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"

		pipepager(output, cmd='less -R')

		downloadpath = "./lambda_code/{}".format(variables['DOWNLOADPATH']['value'])
		url = response['Code']['Location']
		download_code = input(colored(
			"------------------------------------------------\nDo you want to download the code at '{}'? [Y/n] ".format(
				downloadpath), "yellow"))

		if download_code == "Y" or download_code == "y":
			try:
				if not os.path.isdir(downloadpath):
					os.mkdir(downloadpath)

				r = requests.get(url)
				z = zipfile.ZipFile(io.BytesIO(r.content))
				z.extractall(downloadpath)
				print(colored("[*] Code dumped on file '{}'.".format(downloadpath), "green"))

			except:
				e = sys.exc_info()
				print(colored("[*] {}".format(e), "red"))

	except profile.exceptions.TooManyRequestsException:
		print(colored("[*] Too many requests sent. Only one does the job.", "red"))

	except profile.exceptions.InvalidParameterValueException:
		print(colored("[*] No other caracters other than _+=,.@- is allowed on the GroupName", "red"))

	except:
		e = sys.exc_info()[1]
		print(colored("[*] {}".format(e), "red"))