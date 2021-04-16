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
    }
}

description = "Get info on the policy provided"

aws_command = "aws iam get-account-password-policy --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_account_password_policy".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    try:
        policy = profile.get_account_password_policy()
        print("---------------------------".format(colored("Password Policy:","yellow", attrs=['bold'])))
        print("{}".format(colored("Password Policy:","yellow", attrs=['bold'])))
        print("---------------------------".format(colored("Password Policy:","yellow", attrs=['bold'])))
        for key,value in (policy['PasswordPolicy']).items():
            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

        with open(filename,'w') as outputfile:
            json.dump(policy, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

    except:
        print(colored("[*] No password policy applied to this account","green"))
