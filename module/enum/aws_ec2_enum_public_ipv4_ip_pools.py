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

def exploit(profile, workspace):
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
		
		for pool in response:
			output += ("------------------------------\n")
			output += ("{} {}\n".format(colored("PoolId:","yellow",attrs=['bold']), pool['PoolId']))
			output += ("------------------------------\n")
			output += ("\t{}:\n".format(colored("PoolAddressRanges:","red",attrs=['bold'])))
			for address in pool['PoolAddressRanges']:
				for key,value in address.items():
					output += ("\t{}\t{}\n".format(colored(key,"blue",attrs=['bold']),colored(value,"white")))
				
			output += ("\t{}\t{}\n".format(colored("TotalAddressCount:","red",attrs=['bold']),colored(pool['TotalAddressCount'],"blue")))
			output += ("\t{}\t{}\n".format(colored("TotalAvailableAddressCount:","red",attrs=['bold']),colored(pool['TotalAvailableAddressCount'],"blue")))
			output += "\n"

		pipepager(output, cmd='less -R')
