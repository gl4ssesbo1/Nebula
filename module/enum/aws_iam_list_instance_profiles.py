from termcolor import colored
import sys
import json
from datetime import datetime
from pydoc import pipepager

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

description = "List all the instance profiles."

aws_command = "aws iam list-instance-profiles --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_instance_profiles".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    try:
        response = profile.list_instance_profiles()
        output = ""
        with open(filename, 'w') as outputfile:
            json.dump(response['InstanceProfiles'], outputfile, indent=4, default=str)

        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
              colored(".", "green"))
        outputfile.close()

        for prof in response['InstanceProfiles']:
            output +=("{}".format(colored("--------------------------------------------\n", "yellow", attrs=['bold'])))
            output +=("{}:\t{}\n".format(colored("InstanceProfileName", "yellow", attrs=['bold']), prof['InstanceProfileName']))
            output +=("{}".format(colored("--------------------------------------------\n", "yellow", attrs=['bold'])))
            
            for key,value in prof.items():
                if key == "Roles":
                    output +=("\t{}:".format(colored(key, "red", attrs=['bold'])))
                    for k in value:
                        for a,b in k.items():
                            if a == 'AssumeRolePolicyDocument':
                                output +=("\t\t{}\n".format(colored("AssumeRolePolicyDocument", "green", attrs=['bold'])))
                                output +=("\t\t\t{}:\t{}\n".format(colored('Version', "yellow", attrs=['bold']), colored(b['Version'], "white")))
                                output +=("\t\t\t{}:\n".format(colored('Statement', "yellow", attrs=['bold'])))
                                for statement in b['Statement']:
                                    output +=("\t\t\t\t{}:\t{}\n".format(colored('Effect', "magenta", attrs=['bold']), colored(statement['Effect'], "white")))
                                    output +=("\t\t\t\t{}:\n".format(colored('Principal', "magenta", attrs=['bold'])))
                                    for pkey,pval in (statement['Principal']).items():
                                        output +=("\t\t\t\t\t{}:\t{}\n".format(colored(pkey, "white", attrs=['bold']), colored(pval, "white")))
                                    output +=("\t\t\t\t{}:\t{}\n".format(colored('Action', "magenta", attrs=['bold']), colored(statement['Action'], "white")))
                            else:
                                output +=("\t\t{}:\t{}\n".format(colored(a, "green", attrs=['bold']), colored(b, "white")))
                else:
                    output +=("\t{}:\t{}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
            output += "\n"
        pipepager(output, cmd='less -R')

    except:
        print(colored("[*] Does your IAM have the right permissions to use 'GetUserPolicy' API call? ","red"))
        e = sys.exc_info()[0]
        print(colored("[*] {}".format(e), "red"))
