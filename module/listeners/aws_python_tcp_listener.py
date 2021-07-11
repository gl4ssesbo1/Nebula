from termcolor import colored
from __listeners import aws_python_tcp_server
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
		"value": "none",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"HOST": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"PORT": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	}
}
description = "Description of your Module"

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

def exploit(workspace):
	host = variables['HOST']['value']
	port = int(variables['PORT']['value'])
	if os.geteuid() == 0:
		aws_python_tcp_server.main(host, port, workspace)
	else:
		print(colored("[*] You need to be root to be able to open ports. Dump credentials to save them and rerun the tool as privileged user.","red"))