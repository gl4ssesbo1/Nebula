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
    "ACCESSKEY":{
        "value":"",
        "required":"true",
        "description":"The access key to test. It's a required Option."
    }
}

description = "Get info about the current user or specific Users like the Username, ID, ARN, Creation Date, Attached Policies, GroupList and Tags. The IAM whose credentials are provided should have IAMReadOnlyAccess or IAMFullAccess. If the user field is empty, all users' details will be shown. Or you can provide a single user or a group of user separated by comma (',')"

aws_command = "aws iam get-access-key-last-used --access-key-id <Access Key> --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_access_key_last_used".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    
    try:
        response = profile.get_access_key_last_used(
            AccessKeyId=variables['ACCESSKEY']['value']
        )

        print(colored("------------------------", "yellow", attrs=['bold']))
        print("{}: {}".format(colored("Username", "yellow", attrs=['bold']), response['UserName']))
        print(colored("------------------------", "yellow", attrs=['bold']))
        for key,value in (response['AccessKeyLastUsed']).items():
            print("\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

        with open(filename,'w') as outputfile:
            json.dump(response, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))
        
    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))

