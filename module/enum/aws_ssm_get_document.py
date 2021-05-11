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
        "required": "true",
        "description":"Get document info based on the name."
    },
    "DOCUMENT-VERSION": {
        "value": "",
        "required": "false",
        "description":"Get document info based on the owner of the document."
    },
    "VERSION-NAME": {
        "value": "",
        "required": "false",
        "description":"Get document info based on the owner of the document."
    }
}
description = "Gets the contents of the specified Systems Manager document. Document Name is mandatory, but can also be filtered using DocumentVersion and Version Name. Requires ssm:GetCommand permission."

aws_command = "aws ssm get-document --name <Document Name> --version-name <version-name> --document-version <document-version> --region <region> --profile <profile>"

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
    file = "{}_ssm_get_document".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    documentversion = variables['DOCUMENT-VERSION']['value']
    documentname = variables['DOCUMENT-NAME']['value']
    versionname = variables['VERSION-NAME']['value']

    args = {
        "DocumentFormat": "JSON"
    }

    if not documentname == "":
        args['Name'] = documentname

    if not documentversion == "":
        args['DocumentVersion'] = documentversion

    if not versionname == "":
        args['VersionName'] = versionname

    content = {}

    try:
        response = profile.describe_document(
            **args
        )

        json_data = response['Document']
        content['Describe-Document'] = json_data

        title_name = "Name"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])

        output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        list_dictionary(json_data, n_tab)
        output += "\n"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        print(output)
        output = ""

        response = profile.get_document(
            **args
        )
        del response['ResponseMetadata']
        c = (response['Content']).replace("\\n", "")
        content2 = c.replace("\\", "")
        response['Content'] = json.loads(content2)
        json_data = response
        content['Get-Document'] = json_data

        with open(filename, 'w') as outfile:
            json.dump(content, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        title_name = "Name"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])

        output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        list_dictionary(json_data, n_tab)
        output += "\n"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        print(output)
        output = ""

    except:
        response = profile.get_document(
            **args
        )
        del response['ResponseMetadata']
        content = (response['Content']).replace("\\n", "")
        content2 = content.replace("\\", "")
        response['Content'] = json.loads(content2)
        json_data = response

        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        title_name = "Name"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])

        output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        list_dictionary(json_data, n_tab)
        output += "\n"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        print(output)
        output = ""

    else:
        e = sys.exc_info()
        print(colored("[*] {}".format(e), "red"))