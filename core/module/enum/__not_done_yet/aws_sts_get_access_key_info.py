from termcolor import colored
import sys
author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value":"sts",
        "required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "ACCESSKEYID": {
        "value":"",
        "required":"true",
        "description":"The access key to query."
    }
}

description = "Get the ID of the account that the current User is in. Just provide IAM Credentials and run. No extra permissions are needed."

aws_command = "aws get-access-key-info --access-key-id <value> --region <region> --profile <profile>"

def exploit(profile, workspace):
    try:
        accesskeyid = variables['ACCESSKEYID']['value']

        response = profile.get_access_key_info(
            AccessKeyId=accesskeyid
        )

        output = ""
        output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
        output += ("{}: {}\n".format(colored("AccessKeyID", "yellow", attrs=['bold']), accesskeyid))
        output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))

        output += ("\t{}: {}\n".format(colored("Account", "red", attrs=['bold']), colored(response['Account'], "blue")))

        output += "\n"

        print(output)
        
    except:
        e = sys.exc_info()
        print(colored("[*] This AccessKeyID does not exist.", "red"))