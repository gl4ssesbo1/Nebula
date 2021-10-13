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
    "POLICYARN":{
        "value":"",
        "required":"true",
        "description":"The arn of the policy to check."
    }
}

description = "Get info on the policy provided. Uses GetPolicy or get_account_authorization_details API call."

aws_command = "aws iam get-policy --policy-arn <policy arn> --region <region> --profile <profile>"

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""

def list_dictionary(d, n_tab):
    global output
    if isinstance(d, list):
        n_tab += 1
        for i in d:
            if not isinstance(i, list) and not isinstance(i, dict):
                output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
            else:
                list_dictionary(i, n_tab)

    elif isinstance(d, dict):
        n_tab+=1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
            else:
                output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)

def exploit(profile, workspace):
    n_tab = 0
    global output

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_policy".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    pol = {}
    try:
        iam_details = profile.get_account_authorization_details()
        while iam_details['IsTruncated']:
            iam_details = profile.get_account_authorization_details(
                Marker=iam_details['Marker']
            )

        pol_dict = []

        for x in iam_details['Policies']:
            arn = x['Arn']
            if arn == variables['POLICYARN']['value']:
                print(colored("------------------------", "yellow", attrs=['bold']))
                print("{}: {}".format(colored("PolicyName", "yellow", attrs=['bold']), x['PolicyName']))
                print(colored("------------------------", "yellow", attrs=['bold']))
                for a,b in x.items():
                    if not a == "PolicyVersionList":
                        print("\t{}: {}".format(colored(a, "red", attrs=['bold']), colored(b, "blue")))
                        pol[a] = b
                    else:
                        default_version = x['DefaultVersionId']
                        for k in x['PolicyVersionList']:
                            if k['VersionId'] == default_version:
                                pol_dict.append(k)

        if isinstance(pol_dict, list):
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            output += colored("{}:\n".format("PolicyVersionList"), "yellow", attrs=['bold'])
            for data in pol_dict:
                list_dictionary(data, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        print(output)
        output = ""
        pol['PolicyVersionList'] = pol_dict
    except botocore.exceptions.ClientError:
        print("Trying GetPolicy")
        policy = profile.get_policy(
            PolicyArn = variables['POLICYARN']['value']
        )

        pol['Policy'] = policy['Policy']

        print(colored("------------------------", "yellow", attrs=['bold']))
        print("{}: {}".format(colored("PolicyName", "yellow", attrs=['bold']), pol['PolicyName']))
        print(colored("------------------------", "yellow", attrs=['bold']))

        for key,value in pol.items():
            print("\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

    except:
        print(colored("[*] Does your IAM have the right permissions to use 'GetAccountAuthorizationDetails' or 'GetPolicy' API calls? ","red"))

    output_file = open(filename, 'w')
    json.dump(pol,output_file, indent=4, default=str)
    output_file.close()
    print(colored("[*] Policy Permissions written to file", "green"), colored("'{}'".format(filename), "blue"),
          colored(".", "green"))