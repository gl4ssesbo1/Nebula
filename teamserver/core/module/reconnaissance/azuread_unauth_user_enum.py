import json
import os.path

import flask_mongoengine
import requests
from termcolor import colored
from core.database import models

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
	"SERVICE": {
		"value": "none",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"EMAIL":{
		"value":"",
		"required":"false",
        "description":"The email of the user to test."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
        "description":"A wordlist of emails",
		"iswordlist": True,
		"wordlistvalue": []
	}
}

description = ""

aws_command = "No awscli command"

def exploit(workspace):
	userfile = variables['WORDLIST']['value']
	theuserfile = variables['WORDLIST']['wordlistvalue']
	email = variables['EMAIL']['value']
	all_output = []
	single_user_info = {}
	print(os.path.exists(userfile))

	if not email == "" and not userfile == "":
		return {"error": colored("[*] Only add a username or a user file. Not both.", "red")}, 500

	if email == "" and userfile == "":
		return {"error": colored("[*] Add at least a username or a user file. Not both though.", "red")}, 500

	elif not email == "":
		url = "https://login.microsoftonline.com/common/GetCredentialType"
		data = '{"Username": "' + email + '"}'
		response = requests.post(url, data=data)
		json_output = json.loads(response.text)

		if json_output["IfExistsResult"] == 0:
			if json_output['Credentials']['HasPassword']:
				single_user_info = {
						"azure_user_email": email,
						"azure_user_has_password": True,
						"azure_user_domain": email.split("@")[1]
					}

			else:
				single_user_info = {
					"azure_user_email": email,
					"azure_user_has_password": False,
					"azure_user_domain": email.split("@")[1]
				}

			try:
				models.AzureUsers.objects().get(azure_user_email=email).update(
					**single_user_info)

			except flask_mongoengine.DoesNotExist:
				models.AzureUsers(**single_user_info).save()

			except Exception as e:
				pass

			return {"azure_user_email": single_user_info}, 200

		return {"azure_user_email": {"azure_user_email": "User '{0}' does not exist".format(email)}}, 200

	elif not userfile == "":
		#theuserfile = open(userfile.replace("\n", ""), 'r')
		for useremail in theuserfile:
			useremail = useremail.replace("\n","").strip()
			url = "https://login.microsoftonline.com/common/GetCredentialType"
			data = '{"Username": "' + useremail + '"}'
			response = requests.post(url, data=data)
			json_output = json.loads(response.text)

			if json_output["IfExistsResult"] == 0:
				if json_output['Credentials']['HasPassword']:
					single_user_info = {
						"azure_user_email": useremail,
						"azure_user_has_password": True,
						"azure_user_domain": useremail.split("@")[1]
					}
					all_output.append(single_user_info)
				else:
					single_user_info = {
						"azure_user_email": useremail,
						"azure_user_has_password": False,
						"azure_user_domain": useremail.split("@")[1]
					}
					all_output.append(single_user_info)

				try:
					models.AzureUsers.objects().get(azure_user_email=useremail).update(
						**single_user_info)

				except flask_mongoengine.DoesNotExist:
					models.AzureUsers(**single_user_info).save()

				except Exception as e:
					pass

		return {"azure_user_email": all_output}, 200

