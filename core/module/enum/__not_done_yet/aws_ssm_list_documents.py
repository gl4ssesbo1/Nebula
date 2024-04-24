import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
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
        "value": "ssm",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "DOCUMENT-NAME": {
        "value": "",
        "required": "false",
        "description":"List documents based on the name or the beginning of the name. So searching for AWS-Run would show AWS-RunShellScript"
    },
    "DOCUMENT-OWNER": {
        "value": "",
        "required": "false",
        "description":"List documents based on the owner of the document."
    },
    "PLATFORM": {
        "value": "",
        "required": "false",
        "description":"List documents based on the platform it runs on (Windows, Linux)"
    },
    "DOCUMENT-TYPE": {
        "value": "",
        "required": "false",
        "description":"Lists documents based on the type of the document (Command, Policy, Automation, Session)."
    }
}
description = "Get a list of the documents that were or are currently executed. Can be filtered using CommandID, InstanceID, Time invoked (either before or after a specific time), Status and Execution Stage. Requires ssm:ListCommands permission."

aws_command = "aws ssm list-documents --filters Key=Name,Values=AWS-RunShellScript --region <region> --profile <profile>"

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
    try:
        n_tab = 0
        global output

        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        file = "{}_ssm_list_documents".format(dt_string)
        filename = "./workspaces/{}/{}".format(workspace, file)

        documenttype = variables['DOCUMENT-TYPE']['value']
        documentname = variables['DOCUMENT-NAME']['value']
        owner = variables['DOCUMENT-OWNER']['value']
        platform = variables['PLATFORM']['value']

        args = {
            "MaxResults":50
        }
        filters = []

        if not owner == "":
            a = {}
            a['key'] = 'Owner'
            a['value'] = owner
            filters.append(a)

        if not documenttype == "":
            a = {}
            a['key'] = 'DocumentType'
            a['value'] = documenttype
            filters.append(a)

        if not documentname == "":
            a = {}
            a['key'] = 'Name'
            a['value'] = documentname
            filters.append(a)

        if not platform == "":
            a = {}
            a['key'] = 'PlatformTypes'
            a['value'] = platform
            filters.append(a)

        if filters:
            args['DocumentFilterList'] = filters

        response = profile.list_documents(
            **args
        )

        json_data = response['DocumentIdentifiers']

        while 'NextToken' in response:
            nexttoken = response['NextToken']
            response = profile.list_documents(
                **args,
                NextToken=nexttoken
            )
            json_data.extend(response['DocumentIdentifiers'])

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        title_name = "Name"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        for data in json_data:
            output += colored("{}: {}\n".format(title_name, data[title_name]), "yellow", attrs=['bold'])
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            list_dictionary(data, n_tab)
            output += "\n"
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        pipepager(output, "less -R")
        output = ""

    except:
        e = sys.exc_info()
        print(colored("[*] {}".format(e), "red"))