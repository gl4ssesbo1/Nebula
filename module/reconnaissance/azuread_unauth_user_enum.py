import json

import requests
from termcolor import colored
from datetime import datetime
import os

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
	"SERVICE": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
        "description":"The wordlist of buckets."
	},
	"USERNAME":{
		"value":"",
		"required":"false",
        "description":"The wordlist of buckets."
	},
	"DOMAIN":{
		"value":"",
		"required":"true",
        "description":"The wordlist of buckets."
	},
	"VERBOSITY":{
		"value":"false",
		"required":"false",
        "description":"If set to true, it will show you all the buckets if they are PUBLIC, PRIVATE or NOT-EXISTANT. If set to false, will only list PUBLIC and PRIVATE buckets."
	}
}

description = "Gets the name of a bucket or a list of buckets separated by comma (',') or a wordlist of the bucket name and bruteforces the name of the bucket by sending a request to https://<bucketname>.s3.<region>.amazonaws.co. The xml files will be saved on ./workspaces/<workspace>/<datetime>_buckets>/<bucketname>.xml"

aws_command = "No awscli command"

def exploit(workspace):
	userfile = variables['WORDLIST']['value']
	user = variables['USERNAME']['value']
	domain = variables['DOMAIN']['value']
	verbosity = variables['VERBOSITY']['value']

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	filen = "{}_azuread_unauth_enum_users_{}".format(dt_string, domain)
	filename = "./workspaces/{}/{}".format(workspace, filen)
	while os.path.exists(filen):
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		filen = "{}_azuread_unauth_enum_users_{}".format(dt_string, domain)

	outputfile = open(filename, 'w')

	if not user == "" and not userfile == "":
		print(colored("[*] Only add a username or a user file. Not both.", "red"))

	if user == "" and userfile == "":
		print(colored("[*] Add at least a username or a user file. Not both though.", "red"))

	elif not user == "":
		user = "{}@{}".format(user, domain)
		url = "https://login.microsoftonline.com/common/GetCredentialType"
		response = requests.post(url, data={"Username": user})
		print(response.status_code)
		print(response.text)
		json_output = json.loads(response.text)

		if json_output["IfExistsResult"] == 0:
			print("[*] {}{}{}".format(
				colored("User '", "green"),
				colored("{}@{}".format(user, domain), "blue"),
				colored("' exists", "green")
			))
			outputfile.write("{}@{}".format(user, domain))
		else:
			if verbosity.lower() == 'true':
				print("[*] {}{}{}".format(
					colored("User '", "red"),
					colored("{}@{}".format(user, domain), "blue"),
					colored("' doen not exist", "red")
				))

	elif not userfile == "":
		theuserfile = open(userfile, 'r')
		for us in theuserfile.readlines():
			url = "https://login.microsoftonline.com/common/GetCredentialType"
			data = {
				"Username": "{}@{}".format(us.strip(), domain)
			}

			response = requests.post(url, data=data)
			json_output = json.loads(response.content)

			if json_output["IfExistsResult"] == 0:
				print("[*] {}{}{}".format(
					colored("User '", "green"),
					colored("{}@{}".format(us.strip(), domain), "blue"),
					colored("' exists", "green")
				))
				outputfile.write("{}@{}".format(us.strip(), domain))
			else:
				if verbosity.lower() == 'true':
					print("[*] {}{}{}".format(
						colored("User '", "red"),
						colored("{}@{}".format(us.strip(), domain), "blue"),
						colored("' does not exist", "red")
					))

	"https://login.microsoft.com/common/oauth2/token"