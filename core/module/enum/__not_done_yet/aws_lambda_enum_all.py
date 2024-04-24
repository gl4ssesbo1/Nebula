import boto3
from termcolor import colored
from datetime import datetime
import json
import sys
from pydoc import pipepager

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "lambda",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
	"MASTERREGION": {
		"value": "",
		"required": "false",
        "description":"Another variable to set"
	}
}

description = "Description of your Module"

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
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_lambda_enum_all".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    lambda_data = {}
    masterregion = variables['MASTERREGION']['value']
    functions = []
    layers = []

    try:
        response = profile.get_account_settings()
        lambda_data['AccountLimit'] = response['AccountLimit']
        lambda_data['AccountUsage'] = response['AccountUsage']
        del response
    except:
        e = sys.exc_info()[1]
        print(colored("[*] {}".format(e), "red"))

    try:
        if not masterregion == "":
            theresponse = profile.list_functions(
                MasterRegion=masterregion
            )
            response = theresponse['Functions']
            while 'NextMarker' in theresponse:
                theresponse = profile.list_functions(
                    MasterRegion=masterregion,
                    Marker=theresponse['NextMarker']
                )
                response.extend(theresponse['Functions'])
        else:
            theresponse = profile.list_functions()
            response = theresponse['Functions']
            while 'NextMarker' in theresponse:
                theresponse = profile.list_functions(
                    Marker=theresponse['NextMarker']
                )
                response.extend(theresponse['Functions'])

        for function in response:
            name = function['FunctionName']
            lambda_data[name] = function

            functions.append(name)

        del response
        del theresponse
    except:
        e = sys.exc_info()[1]
        print(colored("[*] {}".format(e), "red"))

    try:
        for function in functions:
            response = profile.list_aliases(
                FunctionName=function
            )
            lambda_data[function]['Aliases'] = response['Aliases']
            del response


    except:
        e = sys.exc_info()[1]
        print(colored("[*] {}".format(e), "red"))

    try:
        for function in functions:
            response = profile.get_policy(FunctionName=function)
            lambda_data[function]['Policy'] = json.loads(response['Policy'])
            lambda_data[function]['RevisionId'] = response['RevisionId']
            del response

    except:
        e = sys.exc_info()[1]
        print(colored("[*] {}".format(e), "red"))

    with open(filename, 'w') as outfile:
        json.dump(lambda_data, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    output += colored("==========================================================================\n",
                      "yellow", attrs=['bold'])
    output += colored("                            Lambda Functions\n", "yellow", attrs=['bold'])
    output += colored("==========================================================================\n",
                      "yellow", attrs=['bold'])
    for key, value in lambda_data.items():
        if isinstance(value, list):
            for data in value:
                list_dictionary(data, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        else:
            output += colored("{}\n".format(key), "yellow", attrs=['bold'])
            list_dictionary(value, n_tab)
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
    pipepager(output, 'less -R')
    output = ""