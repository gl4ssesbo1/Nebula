from termcolor import colored
import json
from datetime import datetime
import botocore
from pydoc import pipepager
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
	"SERVICE":{
		"value":"ec2",
		"required":"true",
    	"description":"The service that will be used to run the module. It cannot be changed."
	},
	"GROUPID":{
		"value":"",
		"required":"false",
        "description":"The security group to enumerate. Can supply one or several, split by comma. If not provided, all security groups will be enumerated."
	}
}

description = "Enumerate all security groups on the region or specific if provided. Uses describe-security-groups API call to retrieve."

aws_command = "aws ec2 describe-security-groups --group-ids <group IDs> --region <region> --profile <profile>"

def print_output(response):
	output = ""
	try:
		for secgroup in response['SecurityGroups']:
			output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
			output += "{}: {}\n".format(colored("GroupId","red",attrs=['bold']), colored(secgroup['GroupId'],"yellow"))
			output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
			for key,value in secgroup.items():
				if key == 'IpPermissions' or key == 'IpPermissionsEgress':
					output += "\t{}:\n".format(colored(key, "blue", attrs=['bold']))
					for ip_perm in value:
						for k,v in ip_perm.items():
							if k == 'IpRanges':
								output += "\t\t{}:\n".format(colored(k, "yellow", attrs=['bold']))
								if v:
									for ip_ran in v:
										for ip,ran in ip_ran.items():
											output += "\t\t\t{}: {}\n".format(colored(ip, "green", attrs=['bold']), colored(ran, "magenta"))

							if k == 'Ipv6Ranges':
								output += "\t\t{}:\n".format(colored(k, "yellow", attrs=['bold']))
								if v:
									for ip_ran in v:
										for ip, ran in ip_ran.items():
											output += "\t\t\t{}: {}\n".format(colored(ip, "green", attrs=['bold']), colored(ran, "magenta"))

							if k == 'PrefixListIds':
								output += "\t\t{}:\n".format(colored(k, "yellow", attrs=['bold']))
								if v:
									for ip_ran in v:
										for ip, ran in ip_ran.items():
											output += "\t\t\t{}: {}\n".format(colored(ip, "green", attrs=['bold']), colored(ran, "magenta"))

							if k == 'UserIdGroupPairs':
								output += "\t\t{}:\n".format(colored(k, "yellow", attrs=['bold']))
								if v:
									for ip_ran in v:
										for ip, ran in ip_ran.items():
											output += "\t\t\t{}: {}\n".format(colored(ip, "green", attrs=['bold']), colored(ran, "magenta"))

							if not k == 'IpRanges' and not k == 'UserIdGroupPairs' and not k == 'PrefixListIds' and not k == 'Ipv6Ranges':
								output += "\t\t{}: {}\n".format(colored(k, "yellow", attrs=['bold']), colored(v, "green", attrs=['bold']))

						output += "\t\t{}:\n".format(colored("---------------------------", "yellow", attrs=['bold']))

				else:
					output += "\t{}: {}\n".format(colored(key,"red",attrs=['bold']), colored(value,"blue"))

			output += "\n"
	except Exception as e:
		print(e)
	return output

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_security_groups".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	
	if (variables['GROUPID']['value']) == "":
		try:
			response = profile.describe_security_groups()
			#while response.get('NextToken'):
			#	response = profile.describe_snapshots(
			#		NextToken=response['NextToken']
			#	)
			with open(filename,'w') as snap_file:
				json.dump(response['SecurityGroups'], snap_file, indent=4, default=str)

			output = print_output(response)
			pipepager(output, cmd='more')
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		except botocore.exceptions.ClientError:
			print(colored("[*] Check internet connection.".format(filename), "red"))

	else:
		try:
			secgroups = (variables['GROUPID']['value']).split(",")
			response = profile.describe_security_groups(
				GroupIds=secgroups
			)
			with open(filename,'w') as snap_file:
				json.dump(response['SecurityGroups'], snap_file, indent=4, default=str)

			output = print_output(response)
			pipepager(output, cmd='more')
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		except botocore.exceptions.ClientError:
			print(colored("[*] Check all the Snapshot IDs provided. Some might be incorrect. Else, check internet connection.".format(filename), "red"))