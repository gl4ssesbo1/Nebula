from termcolor import colored
import sys
import json
from datetime import datetime
from pydoc import pipepager

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE":{
		"value":"iam",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	}
}

description = "List all Roles on the Infrastrucrure."

aws_command = "aws ec2 describe-instances --region {} --profile {}"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_roles".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    iam_details = profile.list_roles()

    while iam_details['IsTruncated']:
        iam_details = profile.list_groups(Marker=iam_details['Marker'])

    output_file = open(filename, 'w')
    json.dump(iam_details["Roles"],output_file, indent=4, default=str)
    output_file.close()

    print(colored("[*] Role List written to file", "green"), colored("'{}'".format(filename), "blue"),
          colored(".", "green"))

    output = ""
    for iam_d in iam_details["Roles"]:
        output += ("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))
        output += ("{}:\t{}\n".format(colored("IAM", "yellow", attrs=['bold']), iam_d['RoleName']))
        output += ("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))

        for key,value in iam_d.items():
            if key == 'AssumeRolePolicyDocument':
                output += ("\t{}:\n".format(colored(key,"red",attrs=['bold'])))
                for a,b in value.items():
                    if a == 'Statement':
                        output += ("\t\t{}:\n".format(colored(a,"green",attrs=['bold'])))
                        for l in b:
                                output += ("\t\t\t{}:\t{}\n".format(colored("Effect", "yellow", attrs=['bold']), l['Effect']))
                                output += ("\t\t\t{}:\n".format(colored("Principal", "yellow", attrs=['bold'])))
                                for k,v in (l['Principal']).items():
                                    output += ("\t\t\t\t{}:\t{}\n".format(colored(k, "yellow"), v))
                                output += ("\t\t\t{}:\t{}\n".format(colored("Action", "yellow", attrs=['bold']), l['Action']))
            else:
                output += ("\t{}:\t{}\n".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))

    pipepager(output, "less -R")
    output = ""