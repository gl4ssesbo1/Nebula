import sys

import boto3
import json

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "cur",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"OTHERVARIABLE": {
		"value": "",
		"required": "true/false",
        "description":"Another variable to set"
	}
}
description = "Description of your Module"

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

# The exploit function is like the main() of the module. This is called 
# from the module

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

def exploit(profile):
    try:
        response = profile.describe_report_definitions()

        if response['NextToken']:
            response.extend(profile.describe_report_definitions(NextToken=response['NextToken']))

        return {"ReportName": response['ReportDefinitions']}

    except:
        return {"error": str(sys.exc_info())}

    