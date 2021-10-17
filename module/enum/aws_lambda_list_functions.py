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
	"MASTERREGION": {
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
		file = "{}_lambda_list_functions".format(dt_string)
		filename = "./workspaces/{}/{}".format(workspace, file)
		workspaces = {}
		masterregion = variables['MASTERREGION']['value']

		if not masterregion == "":
			response = profile.list_functions(MasterRegion=masterregion)['Functions']
		else:
			response = profile.list_functions()['Functions']
			
		
		with open(filename, 'w') as outfile:
			json.dump(response, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
	
		output = ""

		for function in response:
			output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
			output += ("{}: {}\n".format(colored("FunctionName", "yellow", attrs=['bold']), function['FunctionName']))
			output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
			for key,value in function.items():
				if key == 'TracingConfig':
					output += ("\t{}: \n".format(colored("TracingConfig", "red", attrs=['bold'])))
					for k,v in value.items():
						output += ("\t\t{}: {}\n".format(colored(k, "blue", attrs=['bold']), colored(v, "yellow")))
				else:
					output += ("\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
		output += "\n"
		pipepager(output, cmd='less -R')
		del output
	
	except profile.exceptions.TooManyRequestsException:
		print(colored("[*] Too many requests sent. Only one does the job.", "red"))

	except profile.exceptions.InvalidParameterValueException:
		print(colored("[*] No other caracters other than _+=,.@- is allowed on the GroupName", "red"))

	except:
		e = sys.exc_info()
		print(colored("[*] {}".format(e), "red"))