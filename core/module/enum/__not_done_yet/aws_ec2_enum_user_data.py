from __future__ import print_function
import base64
from termcolor import colored
from datetime import datetime
import os

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
	"INSTANCES":{
		"value":"",
		"required":"false",
        "description":"The instance IDs to query. Either use this option or the WORDLIST option."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
    	"description":"The wordlist of instance IDs. Either use this option or the INSTANCES option."
	}
}

description = "Lists User data of an Instance provided. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws ec2 describe-instance-attribute --instance-id <instance ID> --region <region> --attribute userData --profile <profile>"

def exploit(profile, workspace):
	dt_string = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
	os.mkdir("./workspaces/{}/{}".format(workspace, dt_string))

	if not variables['INSTANCES']['value'] == "" and not variables['WORDLIST']['value'] == "":
		print(colored("[*] either put comma separated instances or instance wordlist.","red"))

	ids = []
	if not variables['INSTANCES']['value'] == "":
		ids = (variables['INSTANCES']['value']).split(",")
	
	elif not variables['WORDLIST']['value'] == "":
		file = open(variables['INSTANCES']['value'], "r")
		for line in file.readlines():
			ids.append(line)
		file.close()
	else:
		inst = profile.describe_instances()
		for x in inst["Reservations"]:
			for y in x["Instances"]:
				ids.append(str(y["InstanceId"]))


	for id in ids:
		response = profile.describe_instance_attribute(
			InstanceId=id,
			Attribute='userData'
		)

		if response['UserData']:
			file = "ec2_enum_user_data_{}".format(id)
			filename = "./workspaces/{}/{}_ec2_data/{}".format(workspace, dt_string, file)
			user_filename = open(filename, 'w')

			data = base64.b64decode(response['UserData']['Value'])
			print("------------------------------")
			print("{} {}".format(colored("InstanceID:","yellow",attrs=['bold']), response['InstanceId']))
			print("------------------------------")
			print("\t{}\t{}\n".format(colored("User data:","red",attrs=['bold']),colored(data,"blue")))
			user_filename.write(str(data))
			user_filename.close()

	print(colored("[*] Current user data is dumped on directiry '{}'. ".format("./workspaces/{}/{}".format(workspace, dt_string)),"yellow"))
