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
        "description":"The user that will enumerate. If not added, all users will be attempted to be listed (provided we have ListUsers API Access) and we will get permissions of all users."
	}
}

description = "Enumerates the permissions of all users, groups, policies, roles or just any of them if required. The IAM whose credentials are provided needs to have IAMReadOnlyAccess, IAMFullAccess, or have permissions: "

aws_command = "aws iam get-user --user-name <user> --region <region> --profile <profile>"

def exploit(profile, workspace):
    try:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        file = "{}_iam_enum_user_permissions".format(dt_string)
        filename = "./workspaces/{}/{}".format(workspace, file)
        outputfile = open(filename,'w')
        if not variables['USER']['value'] == "":
            # Chars allowed _+=,.@-
            username = profile.get_user(
                UserName=variables['USER']['value']
            )['User']

            json.dump(username, outputfile, indent=4, default=str)

            print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
            print("{}: {}".format(colored("User", "yellow", attrs=['bold']), username['UserName']))
            print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))

            for key, value in username.items():
                if key == 'PermissionsBoundary':
                    print("\t{}:".format(colored(key, "red", attrs=['bold'])))
                    for a, b in value.items():
                        print("\t\t{}:\t{}".format(colored(a, "blue", attrs=['bold']), colored(b, "green")))
                else:
                    print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

        else:
            all_users = []
            user_info = []
            output = ""
            users = profile.list_users()['Users']
            for user in users:
                all_users.append(user['UserName'])

            for user in all_users:
                username = profile.get_user(
                    UserName=user
                )['User']

                user_info.append(username)

                output += ("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))
                output += ("{}: {}\n".format(colored("User", "yellow", attrs=['bold']), username['UserName']))
                output += ("{}\n".format(colored("-----------------------------", "yellow", attrs=['bold'])))

                for key, value in username.items():
                    if key == 'PermissionsBoundary':
                        output += ("\t{}:\n".format(colored(key, "red", attrs=['bold'])))
                        for a, b in value.items():
                            output += ("\t\t{}:\t{}\n".format(colored(a, "blue", attrs=['bold']), colored(b, "green")))
                    else:
                        output += ("\t{}:\t{}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
                output += "\n"

            pipepager(output, cmd='less -R')

            json.dump(user_info, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))
