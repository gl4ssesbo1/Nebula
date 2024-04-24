from termcolor import colored
import sys
import json
from datetime import datetime

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "USERNAME": {
        "value": "",
        "required": "true",
        "description":"The user to check the policies."
    }
}

description = "List all users policies for a user. Needs ListAttachedUserPolicies API right."

aws_command = "aws iam list-attached-user-policies --user-name <user> --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_user_policies".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    workspaces = {}

    try:
        response = profile.list_attached_user_policies(
            UserName=variables['USERNAME']['value']
        )
        while response['IsTruncated']:
            response = profile.list_attached_user_policies(
                Marker=response['Marker']
            )

        workspaces['AttachedPolicies'] = response['AttachedPolicies']

        print(colored("------------------------", "yellow", attrs=['bold']))
        print("{}: {}".format(colored("UserName", "yellow", attrs=['bold']), variables['USERNAME']['value']))
        print(colored("------------------------", "yellow", attrs=['bold']))
        print("\t{}:".format(colored("Attached policies", "magenta", attrs=['bold'])))
        for policy in response['AttachedPolicies']:
            for key, value in policy.items():
                print("\t\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
            print()

        response = profile.list_user_policies(
            UserName=variables['USERNAME']['value']
        )
        while response['IsTruncated']:
            response = profile.list_user_policies(
                Marker=response['Marker']
            )
        workspaces['PolicyNames'] = response['PolicyNames']

        print("\t{}:".format(colored("Inline policies", "magenta", attrs=['bold'])))
        if not len(response['PolicyNames']) == 0:
            for policy in response['PolicyNames']:
                print("\t\t{}: {}".format(colored("Policy Name","red"),colored(policy, "blue", attrs=['bold'])))
            print()

        with open(filename, 'w') as outfile:
            json.dump(workspaces, outfile, indent=4, default=str)
            print(colored("[*] Credentials dumped on file '{}'.".format(filename), "green"))

    except profile.exceptions.NoSuchEntityException:
        print(colored("[*] This User does not Exist","red"))

    except profile.exceptions.InvalidInputException:
        print(colored("[*] The only non alphanumeric characters allowed to be inputed are: \_\+\=\,\.\@-", "red"))
