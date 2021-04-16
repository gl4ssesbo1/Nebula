import json
import sys
from termcolor import colored
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
	}
}

description = "Enumerates the permissions of all users, groups, policies, roles or just any of them if required. The IAM whose credentials are provided needs to have IAMReadOnlyAccess, IAMFullAccess, or have permissions: "

aws_command = "aws iam get-account-summary --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_account_summary".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    try:
        response = profile.get_account_summary()
        
        print(colored("------------------------", "yellow", attrs=['bold']))
        print("{}".format(colored("Account Summary", "yellow", attrs=['bold'])))
        print(colored("------------------------", "yellow", attrs=['bold']))
        for key,value in (response['SummaryMap']).items():
            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

        policy = response['SummaryMap']
        with open(filename,'w') as outputfile:
            json.dump(policy, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))