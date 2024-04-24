import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import sys
from colorama import init

init()

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "lambda",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "FUNCTIONNAME": {
        "value": "",
        "required": "true",
        "description": "Another variable to set"
    }
}

description = "Description of your Module"

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"

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
    try:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        file = "{}_lambda_get_policy".format(dt_string)
        filename = "./workspaces/{}/{}".format(workspace, file)

        functionname = variables['FUNCTIONNAME']['value']

        response = profile.get_policy(FunctionName=functionname)
        lambda_data = {}
        lambda_data['Policy'] = json.loads(response['Policy'])
        lambda_data['Policy']['RevisionId'] = response['RevisionId']

        output = ""
        output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
        output += ("{}: {}\n".format(colored("FunctionName", "yellow", attrs=['bold']), functionname))
        output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))

        for key, value in lambda_data.items():
            if isinstance(value, list):
                for data in value:
                    list_dictionary(data, n_tab)
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            else:
                output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                list_dictionary(value, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])

        print(output)
        with open(filename, 'w') as outfile:
            json.dump(lambda_data, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    except profile.exceptions.TooManyRequestsException:
        print(colored("[*] Too many requests sent. Only one does the job.", "red"))

    except profile.exceptions.InvalidParameterValueException:
        print(colored("[*] No other caracters other than _+=,.@- is allowed on the GroupName", "red"))

    except:
        e = sys.exc_info()
        print(colored("[*] {}".format(e), "red"))
