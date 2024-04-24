from termcolor import colored
import requests
from datetime import datetime
import os
import sys

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
	"ACCOUNT-IDS":{
		"value":"",
		"required":"false",
        "description":"A single account or several accounts spearated by comma."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
        "description":"The wordlist of accounts."
	},
	"VERBOSITY":{
		"value":"false",
		"required":"false",
        "description":"If set to true, it will show you all the accounts, wether they exist or not. If set to false, will only list existing accounts."
	}
}

description = "Check if one or a list of account IDs are valid. They are tested against https://<account-id>.signin.aws.amazon.com"

aws_command = "No awscli command"

def exploit(workspace):
	try:
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		filen = "{}_account_id_fuzzer".format(dt_string)
		if not os.path.exists(filen):
			outputfile = open("./workspaces/{}/{}".format(workspace,filen), 'w')

	except:
		e = sys.exc_info()[1]
		print(colored(e, "red"))

	print()

	if variables['ACCOUNT-IDS']['value'] == "" and variables['WORDLIST']['value'] != "":
		file = open(variables['WORDLIST']['value'], 'r')

		for account in file.readlines():
			try:
				url = 'https://{}.signin.aws.amazon.com/'.format(account.strip())
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
				}
				response = requests.get(
					url,
					headers=headers
				)

				if response.status_code == 200:
					print("{}{}{}".format(
						colored(
							"Account '", "green"
							),
						colored(
							account.strip(), "blue"
						),colored(
							"' is valid", "green"
							)
						)
					)
					outputfile.write(account)
				else:
					if (variables['VERBOSITY']['value']).lower() == 'true':
						print("{}{}{}".format(
							colored(
								"Account '", "red"
							),
							colored(
								account.strip(), "blue"
							), colored(
								"' is not valid", "red"
							)
						)
					)

			except:
				e = sys.exc_info()[1]
				print(colored(e, "red"))

		print()
		print("{}{}{}".format(
			colored(
				"Output saved on '", "green"
			),
			colored(
				"./workspaces/{}/{}".format(workspace,filen), "blue"
			), colored(
				"'.", "green"
			)))

	elif variables['ACCOUNT-IDS']['value'] != "" and variables['WORDLIST']['value'] == "":
		accounts = (variables['ACCOUNT-IDS']['value']).split(",")
		for acc in accounts:
			try:
				url = 'https://{}.signin.aws.amazon.com/'.format(acc)
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
				}
				response = requests.get(
					url,
					headers=headers
				)

				if response.status_code == 200:
					print("{}{}{}".format(
						colored(
							"Account '", "green"
						),
						colored(
							acc, "blue"
						), colored(
							"' is valid", "green"
						)
					)
					)
					outputfile.write(acc)
				else:
					if (variables['VERBOSITY']['value']).lower() == 'true':
						print("{}{}{}".format(
							colored(
								"Account '", "red"
							),
							colored(
								acc, "blue"
							), colored(
								"' is not valid", "red"
							)
						)
					)

			except:
				e = sys.exc_info()[1]
				print(colored(e, "red"))

		print()
		print("{}{}{}".format(
			colored(
				"Output saved on '", "green"
			),
			colored(
				"./workspaces/{}/{}".format(workspace,filen), "blue"
			), colored(
				"'.", "green"
			)))

	else:
		print(colored("[*] Add either an account, or a wordlist of accounts.","red"))