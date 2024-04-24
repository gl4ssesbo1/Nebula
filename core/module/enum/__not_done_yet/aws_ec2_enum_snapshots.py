from termcolor import colored
import json
from datetime import datetime
import sys
import botocore

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
	"SNAPSHOTS":{
		"value":"",
		"required":"false",
        "description":"The snapshot to enumerate. Can supply one or several, split by comma. If not provided, all snapshots will be enumerated."
	}
}

description = "Enumerate all snapshots on the region or specific if provided. Uses describe-security-groups API call to retrieve."

aws_command = "aws ec2 describe-snapshots --snapshot-ids <snapshot ID> --region <region> --profile <profile>"

def exploit(profile, workspace):
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_snapshots".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)
	
	if (variables['SNAPSHOTS']['value']) == "":
		try:
			response = profile.describe_snapshots()
			while response.get('NextToken'):
				response = profile.describe_snapshots(
					NextToken=response['NextToken']
				)
				with open(filename,'w') as snap_file:
					json.dump(response['Snapshots'], snap_file, indent=4, default=str)
				
						
				for snapshot in response['Snapshots']:
					print(colored("----------------------------------------------","yellow",attrs=['bold']))
					print("{}: {}".format(colored("SnapshotId","red",attrs=['bold']), colored(snapshot['SnapshotId'],"yellow")))
					print(colored("----------------------------------------------","yellow",attrs=['bold']))
					for key,value in snapshot.items():
						print("\t{}: {}".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))
					print()
					
				print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
		except botocore.exceptions.ClientError:
			print(colored("[*] Check internet connection.".format(filename), "red"))

	else:
		try:
			snapshots = (variables['SNAPSHOTS']['value']).split(",")
			response = profile.describe_snapshots(
				SnapshotIds=snapshots
			)
			with open(filename,'w') as snap_file:
				json.dump(response['Snapshots'], snap_file, indent=4, default=str)
			
					
			for snapshot in response['Snapshots']:
				print(colored("----------------------------------------------","yellow",attrs=['bold']))
				print("{}: {}".format(colored("SnapshotId","red",attrs=['bold']), colored(snapshot['SnapshotId'],"yellow")))
				print(colored("----------------------------------------------","yellow",attrs=['bold']))
				for key,value in snapshot.items():
					print("\t{}: {}".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))
				print()
				
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
		except botocore.exceptions.ClientError:
			print(colored("[*] Check all the Snapshot IDs provided. Some might be incorrect. Else, check internet connection.".format(filename), "red"))
