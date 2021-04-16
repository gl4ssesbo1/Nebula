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
	},
    "USER":{
        "value":"",
        "required":"false",
        "description":"If you want to get the groups where a certain user is part of, use this option."
    }
}

description = "List all the groups in the infrastructure, or just the groups that belong to a specific user."

aws_command = """aws iam list-groups --region <region> --profile <profile>
aws iam list-groups-for-user --user-name <username> --region <region> --profile <profile>"""

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_groups".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    try:
        iam_details = profile.list_groups()
        while iam_details['IsTruncated']:
            iam_details = profile.list_groups(Marker=iam_details['Marker'])

        groups = iam_details['Groups']
        with open(filename, 'w') as outputfile:
            json.dump(groups, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
              colored(".", "green"))

        output = ""
        for iam in iam_details['Groups']:
            output +=("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))
            output +=("{}:\t{}\n".format(colored("IAM", "yellow", attrs=['bold']), iam['GroupName']))
            output +=("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))
            for key,value in iam.items():
                output +=("\t{}:\t{}\n".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))
            output += "\n"
        pipepager(output, cmd='less -R')

    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))