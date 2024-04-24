import json
from termcolor import colored
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
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

description = "Enumerates the permissions of all users, groups, policies, roles or just any of them if required. The IAM whose credentials are provided needs to have IAMReadOnlyAccess, IAMFullAccess, or have permissions: "

aws_command = "aws iam get-account-authorization-details --region <region> --profile <profile>"

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white",
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
        n_tab += 1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold']),
                                               colored(value, colors[n_tab + 1])))
            else:
                output += ("{}{}:\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)


def exploit(profile, workspace):
    global output
    n_tab = 0
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_enum_all".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    iam = {}

    try:
        iam_details = {}
        response = profile.get_account_authorization_details()
        iam_details = response

        while response['IsTruncated']:
            response = profile.get_account_authorization_details(
                Marker=response['Marker']
            )
            if response.get('UserDetailList'):
                (iam_details['UserDetailList']).extend(response['UserDetailList'])
            if response.get('GroupDetailList'):
                (iam_details['GroupDetailList']).extend(response['GroupDetailList'])
            if response.get('RoleDetailList'):
                (iam_details['RoleDetailList']).extend(response['RoleDetailList'])
            if response.get('Policies'):
                (iam_details['Policies']).extend(response['Policies'])

        iam['UserDetailList'] = iam_details['UserDetailList']
        iam['GroupDetailList'] = iam_details['GroupDetailList']
        iam['RoleDetailList'] = iam_details['RoleDetailList']

        pol_dict = []
        for x in iam_details['Policies']:
            correct_version = {}
            for key, value in x.items():
                if key == "PolicyVersionList":
                    for version in value:
                        if 'IsDefaultVersion':
                            correct_version['PolicyVersion'] = version
                            pol_dict.append(correct_version)
                            break
                else:
                    correct_version[key] = value

        iam['Policies'] = pol_dict
        with open(filename, 'w') as outputfile:
            json.dump(iam, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
              colored(".", "green"))

        for key, value in iam.items():
            if key == "Policies":
                continue
            else:
                output += colored("==========================================================================\n",
                                  "yellow", attrs=['bold'])
                output += colored("                                  " + key + " \n", "yellow", attrs=['bold'])
                output += colored("==========================================================================\n",
                                  "yellow", attrs=['bold'])
                if isinstance(value, list):
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                    for data in value:
                        list_dictionary(data, n_tab)
                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                else:
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                    output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                    list_dictionary(value, n_tab)
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        pipepager(output, 'less -R')
    except profile.exceptions.ServiceFailureException:
        print(colored("[*] Are you sure you have the rights to execute 'GetAccountAuthorizationDetails' API Call?",
                      "red"))
