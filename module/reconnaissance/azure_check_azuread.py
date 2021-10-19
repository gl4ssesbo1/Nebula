from termcolor import colored
from datetime import datetime
import json
import sys
import requests

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "false",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "DOMAIN": {
        "value": "",
        "required": "true",
        "description":"The domain of the company to test."
    }
}
description = "Check if federation is configured for a domain."

aws_command = "None"

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

def exploit(workspace):
    n_tab = 0
    global output

    domain = variables['DOMAIN']['value']

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_azure_check_azuread_{}".format(dt_string, domain)
    filename = "./workspaces/{}/{}".format(workspace, file)

    if domain == "":
        print(
            colored("[*] Enter a DOMAIN","red")
        )

    else:
        url = 'https://login.microsoftonline.com/getuserrealm.srf?login={}'.format(domain)
        try:
            json_data = json.loads(requests.get(url).text)

            with open(filename, 'w') as outfile:
                json.dump(json_data, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

            if isinstance(json_data, list):
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                for data in json_data:
                    domain = data['DomainName']
                    output += colored("{}: {}\n".format('Domain', domain), "yellow", attrs=['bold'])
                    list_dictionary(data, n_tab)
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            else:
                domain = json_data['DomainName']
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                output += colored("{}: {}\n".format('Domain', domain), "yellow", attrs=['bold'])
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                list_dictionary(json_data, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            print(output)
            del output

        except KeyError:
            print(colored("[*] AzureAD not configured.", "yellow"))

        except:
            e = sys.exc_info()
            print(colored("[*] {}".format(e), "red"))