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
    "GROUP": {
        "value": "",
        "required": "true",
        "description":"The group you will list the policies."
    }
}

description = "Get info on the policy provided"

aws_command = "aws iam list-group-policies -groupname <groupname> --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_group_policies".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    try:
        response = profile.list_attached_group_policies(
            GroupName=variables['GROUP']['value']
        )

        while response['IsTruncated']:
            response.extend(profile.list_attached_group_policies(
                Marker=response['Marker']
            ))

        with open(filename,'w') as outputfile:
            json.dump(response, outputfile, indent=4, default=str)

        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
              colored(".", "green"))
        outputfile.close()

        print(colored("------------------------", "yellow", attrs=['bold']))
        print("{}: {}".format(colored("GroupName", "yellow", attrs=['bold']), variables['GROUP']['value']))
        print(colored("------------------------", "yellow", attrs=['bold']))

        for policy in response['AttachedPolicies']:
            for key, value in policy.items():
                print("\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
            print()

    except profile.exceptions.NoSuchEntityException:
        print(colored("[*] This User does not Exist","red"))

    except profile.exceptions.InvalidInputException:
        print(colored("[*] The only non alphanumeric characters allowed to be inputed are: \_\+\=\,\.\@-", "red"))