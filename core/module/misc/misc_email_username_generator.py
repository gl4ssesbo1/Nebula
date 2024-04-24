import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

'''
    If you want to be recognized about your contribution, you can add your name/nickname and contacts here. It will be outputed when user types "options".
'''
author = {
    "name":"",
    "twitter":"",
    "github":"",
    "email":""
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"SOURCE-ADDRESS": {
		"value": "",
		"required": "true",
        "description":"The email address that is sending the email. This email address must be either individually verified with Amazon SES, or from a domain that has been verified with Amazon SES."
	},
	"SUBJECT": {
		"value": "",
		"required": "true",
        "description":"The subject of the message."
	},
	"LIST-OF-DESTINATION-EMAILS": {
		"value": "",
		"required": "true",
        "description":"The path of a file containing target emails to send the malicious message to."
	},
	"LIST-OF-CC-EMAILS": {
		"value": "",
		"required": "false",
        "description":"The path of a file containing CC emails to send the malicious message to."
	},
	"LIST-OF-BCC-EMAILS": {
		"value": "",
		"required": "false",
        "description":"The path of a file containing BCC emails to send the malicious message to."
	},
	"MESSAGE-TYPE": {
		"value": "Text",
		"required": "true",
        "description":"Message type. Either TEXT or HTML(in case of links)"
	},
	"MESSAGE-BODY-FILE": {
		"value": "",
		"required": "true",
        "description":"Either Text or HTML(in case of links)"
	}
}
description = "Description of your Module"

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(profile, workspace):
	charset = 'UTF-8'

	source = variables['SOURCE-ADDRESS']['value']

	destinationdir = {
		'ToAddresses': []
	}
	dest = variables['LIST-OF-DESTINATION-EMAILS']['value']
	cc = variables['LIST-OF-CC-EMAILS']['value']
	bcc = variables['LIST-OF-BCC-EMAILS']['value']

	destinationfile = open(dest, 'r')
	for email in destinationfile.readlines():
		(destinationdir['ToAddresses']).append(email.strip().replace("\n",""))
	del email

	if not cc == "":
		ccfile = open(cc, 'r')
		for email in ccfile.readlines():
			(destinationdir['CcAddresses']).append(email.strip().replace("\n", ""))
	del email

	if not bcc == "":
		bccfile = open(bcc, 'r')
		for email in bccfile.readlines():
			(destinationdir['BccAddresses']).append(email.strip().replace("\n", ""))
	del email

	subject = variables["SUBJECT"]['value']

	message = {
		'Subject': {
			'Data': subject,
			'Charset': charset
		},
		'Body': {

		}
	}

	messagefile = open(variables["MESSAGE-BODY-FILE"]['value'], 'r')
	if (variables["MESSAGE-TYPE"]['value']).lower() == 'text':
		message['Body']['Text']['Data'] = messagefile.read()
		message['Body']['Text']['Charset'] = charset

	messagefile = open(variables["MESSAGE-BODY-FILE"]['value'], 'r')
	if (variables["MESSAGE-TYPE"]['value']).lower() == 'html':
		message['Body']['Html']['Data'] = messagefile.read()
		message['Body']['Html']['Charset'] = charset

	response = profile.send_email(
		Source=source,
		Destination=destinationdir,
		Message=message
	)

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ses_send_message_{}".format(dt_string, source)
	filename = "./workspaces/{}/{}".format(workspace, file)

	del response['ResponseMetadata']
	with open(filename, 'w') as outfile:
		json.dump(response, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	output = ""
	output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	output += colored("MessageID: {}\n".format(response['MessageId']), "yellow", attrs=['bold'])
	output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	print(output)