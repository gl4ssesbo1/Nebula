from termcolor import colored
from datetime import datetime
import json
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
		"value": "s3",
		"required": "true",
    	"description":"The service that will be used to run the module. It cannot be changed."
	},
    "BUCKETS":{
		"value":"",
		"required":"true",
    	"description":"The service that will be used to run the module. It cannot be changed."
	},
    "MAXKEYS":{
		"value":"1500",
		"required":"false",
    	"description":"The service that will be used to run the module. It cannot be changed."
	}
}

description = "Gets the name of a bucket or a list of buckets separated by comma (',') and gives information regarding objects in it, size and date modified. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws s3api list-objects-v2 --bucket <my-bucket> --region <region> --profile <profile>"

def exploit(profile, workspace):
	buckets = variables['BUCKETS']['value'].split(",")
	contents = {}
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_s3_list_objects".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	json_data = {}
	for buck in buckets:
		maxkeys = int(variables['MAXKEYS']['value'])
		response = profile.list_objects_v2(Bucket=buck, MaxKeys=maxkeys)

		contents[buck] = response['Contents']
		while response['IsTruncated']:
			response = profile.list_objects_v2(
					Bucket=buck,
					MaxKeys=maxkeys,
					ContinuationToken=response['NextContinuationToken']
			)
			contents[buck].extend(response['Contents'])
		json_data[buck] = response['Contents']

	with open(filename, 'w') as outputfile:
		json.dump(json_data, outputfile, indent=4, default=str)

	outputfile.close()
	print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

	output = ""
	for key,value in json_data.items():
		output += (colored("-----------------------------\n", "yellow", attrs=["bold"]))
		output += ("{}: {}".format(colored("Name:", "yellow", attrs=["bold"]), colored("\t{}\n".format(key),"white")))
		output += (colored("-----------------------------\n", "yellow", attrs=["bold"]))

		output += (colored("\t\t-----------------------------\n", "yellow", attrs=["bold"]))
		for x in value:
			for k, v in x.items():
				output += ("\t\t{}:\t{}\n".format(colored(k, "red"), colored(v, "blue")))
			output += (colored("\t\t-----------------------------\n", "yellow", attrs=["bold"]))
	pipepager(output, "less -R")