from termcolor import colored
import sys
import json
from datetime import datetime

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
	"ROLENAME":{
        "value":"",
        "required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
    }
}

description = "List all Roles on the Infrastrucrure."

aws_command = "aws iam get-role --role-name <rolename> --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_policy".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    try:
        roles = profile.get_role(
		    RoleName=variables["ROLENAME"]["value"]
	    )

        with open(filename,'w') as outputfile:
            outputfile.write(roles)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

        print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
        print("{}: {}".format(colored("Role", "yellow", attrs=['bold']), roles['Role']['RoleName']))
        print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))

        for key, value in (roles['Role']).items():
            if key == 'AssumeRolePolicyDocument':
                print("\t{}:".format(colored(key, "red", attrs=['bold'])))
                for a, b in value.items():
                    if a == 'Statement':
                        print("\t\t{}:".format(colored(a, "green", attrs=['bold'])))
                        for l in b:
                            print("\t\t\t{}:\t{}".format(colored("Effect", "yellow", attrs=['bold']), l['Effect']))
                            print("\t\t\t{}:".format(colored("Principal", "yellow", attrs=['bold'])))
                            for k, v in (l['Principal']).items():
                                print("\t\t\t\t{}:\t{}".format(colored(k, "magenta", attrs=['bold']), v))
                            print("\t\t\t{}:\t{}".format(colored("Action", "yellow", attrs=['bold']), l['Action']))
            else:
                print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
        
    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))
