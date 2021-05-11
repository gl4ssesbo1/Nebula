import json
from termcolor import colored
from datetime import datetime
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
	}
}

description = "Lists User data of an Instance provided. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws ec2 describe-public-ipv4-pools --region {} --profile {}"

def exploit(profile, workspace):
	dt_string = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_elastic_ips".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)
	output = ""
	response = profile.describe_addresses()['Addresses']

	if len(response) == 0:
		print(colored('[*] No Public IPv4 Pools configured!','red'))
	else:
		with open(filename, 'w') as user_filename:
			json.dump(response, user_filename, indent=4, default=str)
		print(colored("[*] IP Pools output is dumped on file '{}'.".format(filename),"yellow"))
		
		for elastic in response:
			output += ("------------------------------\n")
			output += ("{} {}\n".format(colored("AllocationId:", "yellow", attrs=['bold']), elastic['AllocationId']))
			output += ("------------------------------\n")
			for key,value in elastic.items():
				if not key == 'Tags':
					output += ("\t{}\t{}\n".format(colored(key,"blue",attrs=['bold']),colored(value,"white")))
				else:
					if not elastic['Tags']:
						pass
					else:
						for t, v in (elastic['Tags']).items():
							output += ("\t{}\t{}\n".format(colored(t, "blue", attrs=['bold']), colored(v, "white")))

		pipepager(output, cmd='less -R')
