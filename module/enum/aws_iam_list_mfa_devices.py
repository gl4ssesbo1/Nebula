from termcolor import colored
import sys
from datetime import datetime
from pydoc import pipepager
import json

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
        "USERNAME":{
            "value":"",
            "required":"false",
            "description":"The service that will be used to run the module. It cannot be changed."
        },
}

description = "List all MFA Devices on the account, or if USERNAME option is used, list all MFA Devices of that user on the account."

aws_command = """aws iam list-mfa-devices --user-name Bob --region <region> --profile <profile>
aws iam list-mfa-devices --region <region> --profile <profile>"""

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_mfa_devices".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    try:
        if variables['USERNAME']['value'] == "" or variables['USERNAME']['value'] == None:
            iam_details = profile.list_mfa_devices()
        
        else:
            iam_details = profile.list_mfa_devices(
                UserName=variables['USERNAME']['value']
            )
        
        with open(filename, 'w') as outputfile:
            json.dump(iam_details['MFADevices'], outputfile, indent=4, default=str)

        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
              colored(".", "green"))
        outputfile.close()

        while iam_details['IsTruncated']:
            iam_details = profile.list_mfa_devices(Marker=iam_details['Marker'])
        
        if iam_details['MFADevices']:
            print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
            print("{}:".format(colored("MFA Devices", "yellow", attrs=['bold'])))
            print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
            for mfa in iam_details['MFADevices']:
                print("\t{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
                print("\t{}:\t{}".format(colored("UserName", "yellow", attrs=['bold']), mfa['UserName']))
                print("\t{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
                for key,value in mfa.items():
                    print("\t\t{}:\t{}".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))
                print()
        else:
            print(colored("[*] The user supplied has no MFA Support Enabled.","green"))
            
    except:
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))
