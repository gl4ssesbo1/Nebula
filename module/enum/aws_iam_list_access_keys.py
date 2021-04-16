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
    "USERS":{
        "value":"",
        "required":"false",
        "description":"The ."
    }
}

aws_command = """
aws iam list-access-keys --region <region> --profile <profile>
aws iam list-access-keys --user-name <user> --region <region> --profile <profile>
"""

description = "Get info about the current user or specific Users like the Username, ID, ARN, Creation Date, Attached Policies, GroupList and Tags. The IAM whose credentials are provided should have IAMReadOnlyAccess or IAMFullAccess. If the user field is empty, all users' details will be shown. Or you can provide a single user or a group of user separated by comma (',')"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_user_details".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    all_users = variables['USERS']['value']
    users = []
    access_keys = {}

    if not all_users == "":
        users = (variables['USERS']['value']).split(",")

    else:
        try:
            iam_details = profile.list_users()
            while iam_details['IsTruncated']:
                iam_details = profile.list_users(Marker=iam_details['Marker'])

            for user in iam_details['Users']:
                users.append(user['UserName'])
        except:
            print(colored("[*] You have no permission to list users. Try providing a user or some separated by comma.", "red"))

    for user in users:
        try:
            response = profile.list_access_keys(
                UserName=user,
                MaxItems=123
            )
            access_keys[user] = response['AccessKeyMetadata']

        except profile.exceptions.NoSuchEntityException:
            print("{}{}{}".format(colored("[*] User '","red"), colored(user,"blue"), colored("' does not exist.","red")))

        except:
            e = sys.exc_info()[0]
            print(colored("[*] {}".format(e), "red"))

    if not all_users == "":
        print(list_access_keys_func(access_keys))
    else:
        pipepager(list_access_keys_func(access_keys), "less -R")

    with open(filename,'w') as outputfile:
        json.dump(access_keys, outputfile, indent=4, default=str)

    outputfile.close()
    print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

def list_access_keys_func(access_keys):
    output = ""
    for u,a in access_keys.items():
        output += (colored("------------------------\n", "yellow", attrs=['bold']))
        output += ("{}: {}\n".format(colored("Username", "yellow", attrs=['bold']), u))
        output += (colored("------------------------\n", "yellow", attrs=['bold']))
        for res in a:
            for key, value in res.items():
                output += ("\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
            output += ("\n")
    return output