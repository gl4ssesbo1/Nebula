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

description = "Lists the pool of public IPs configured. Uses describe_public_ipv4_pools API call."

aws_command = "aws ec2 describe-public-ipv4-pools --region <region> --profile <profile>"

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

	dt_string = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_public_ipv4_ip_pools".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)
	output = ""
	response = profile.describe_public_ipv4_pools()['PublicIpv4Pools']
	
	if len(response) == 0:
		print(colored('[*] No Public IPv4 Pools configured!','red'))
	else:
		with open(filename, 'w') as user_filename:
			json.dump(response, user_filename, indent=4, default=str)
		print(colored("[*] IP Pools output is dumped on file '{}'.".format(filename),"yellow"))
		
		if isinstance(response, list):
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			for data in response:
				output += colored("PublicIp: {}\n".format(response['PoolId']), "yellow", attrs=['bold'])
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
				list_dictionary(data, n_tab)
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		else:
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			output += colored("PublicIp: {}\n".format(response['PoolId']), "yellow", attrs=['bold'])
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			list_dictionary(response, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])

		pipepager(output, cmd='less -R')
		output = ""
