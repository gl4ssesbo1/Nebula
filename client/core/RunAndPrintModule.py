import json
import os, sys

import requests
from termcolor import colored
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pydoc import pipepager
def RunModule(module_char, module_options, cred_prof, useragent, workspace, web_proxies, jwt_token, apihost, username, region):
    run_module_options = {
        'module': module_char,
        'module_options': module_options['module_options'],
        'cred-prof': cred_prof,
        'user-agent': useragent,
        'workspace': workspace,
        'web-proxies': web_proxies,
        "username": username,
        "awsregion": region
    }

    return json.loads(requests.post("{}/api/latest/modules/run".format(apihost),
                                            json=run_module_options,
                                            headers={"Authorization": "Bearer {}".format(
                                               jwt_token)}).text)

    #run_module_json = json.loads(run_module_output)

AWS_REGIONS = [
        "af-south-1",
        "ap-east-1",
        "ap-northeast-1",
        "ap-northeast-2",
        "ap-northeast-3",
        "ap-south-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "ca-central-1",
        "eu-central-1",
        "eu-north-1",
        "eu-south-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "me-south-1",
        "sa-east-1",
        "us-east-1",
        "us-east-2",
        "us-gov-east-1",
        "us-gov-west-1",
        "us-west-1",
        "us-west-2"
    ]

def PrintAWSModule(run_module_json):
    output = ""
    for title, json_data in run_module_json.items():
        if title == "error":
            print(colored("[*] {}".format(json_data), "red"))
        elif "error" in json_data:
            print(colored("[*] {}".format(json_data['error']), "red"))
        elif 'clientError' in json_data:
            continue
        else:
            output += colored(
                "------------------------------------------------------------------\n",
                "yellow", attrs=['bold'])

            if isinstance(json_data, list):
                for data in json_data:
                    if not title in AWS_REGIONS:
                        output += colored(
                            f"{title}: {data[title]}\n",
                            "yellow", attrs=['bold'])
                    else:
                        output += colored(
                            f"Region: {title}\n",
                            "yellow", attrs=['bold'])
                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow", attrs=['bold'])
                    raw_json = json.dumps(data, indent=4)
                    output += highlight(
                        raw_json,
                        JsonLexer(),
                        TerminalFormatter()
                    )

                    # Print to console

                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow",
                        attrs=['bold'])
            else:
                if not title in AWS_REGIONS:
                    output += colored(
                        f"{title}: {json_data[title]}\n",
                        "yellow", attrs=['bold'])
                else:
                    output += colored(
                        f"Region: {title}\n",
                        "yellow", attrs=['bold'])
                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow", attrs=['bold'])
                raw_json = json.dumps(json_data, indent=4)
                output += highlight(
                    raw_json,
                    JsonLexer(),
                    TerminalFormatter()
                )

                # Print to console

                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow",
                    attrs=['bold'])
            if len(output.split("\n")) > (os.get_terminal_size().lines * 2):
                pipepager(output, cmd='less -FR')
            else:
                print(output)
            output = ""

"""for title_name, json_data in run_module_json.items():
    if isinstance(json_data, list):
        output += colored("------------------------------------------------------------------\n",
                          "yellow", attrs=['bold'])
        for data in json_data:
            output += colored(
                "{}: {}\n".format(title_name, data[title_name]),
                "yellow", attrs=['bold'])
            output += colored(
                "------------------------------------------------------------------\n",
                "yellow", attrs=['bold'])
            list_dictionary(data, n_tab)
            output += colored(
                "------------------------------------------------------------------\n",
                "yellow",
                attrs=['bold'])
    else:
        output += colored("------------------------------------------------------------------\n",
                          "yellow", attrs=['bold'])
        output += colored(
            "{}: {}\n".format(title_name, json_data[title_name]),
            "yellow", attrs=['bold'])
        output += colored("------------------------------------------------------------------\n",
                          "yellow", attrs=['bold'])
        list_dictionary(json_data, n_tab)
        output += colored("------------------------------------------------------------------\n",
                          "yellow", attrs=['bold'])
    pipepager(output, cmd='less -FR')
    output = """""

def PrintModule(run_module_json):
    output = ""
    if "error" in run_module_json:
        print(colored("[*] {}".format(run_module_json['error']), "red"))

    else:
        for title_name, json_data in run_module_json.items():
            if isinstance(json_data, list):
                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow", attrs=['bold'])
                for data in json_data:
                    output += colored(
                        "{}: {}\n".format(title_name, data[title_name]),
                        "yellow", attrs=['bold'])
                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow", attrs=['bold'])
                    raw_json = json.dumps(data, indent=4)
                    output += highlight(
                        raw_json,
                        JsonLexer(),
                        TerminalFormatter()
                    )

                    # Print to console

                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow",
                        attrs=['bold'])
            else:

                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow", attrs=['bold'])
                output += colored(
                    "{}: {}\n".format(title_name, json_data[title_name]),
                    "yellow", attrs=['bold'])
                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow", attrs=['bold'])
                raw_json = json.dumps(json_data, indent=4)
                output += highlight(
                    raw_json,
                    JsonLexer(),
                    TerminalFormatter()
                )
                # TerminalFormatter()
                output += colored(
                    "------------------------------------------------------------------\n",
                    "yellow", attrs=['bold'])

            if len(output.split("\n")) > (os.get_terminal_size().lines*2):
                pipepager(output, cmd='less -FR')
            else:
                print(output)
            output = ""

        """for title_name, json_data in run_module_json.items():
            if isinstance(json_data, list):
                output += colored("------------------------------------------------------------------\n",
                                  "yellow", attrs=['bold'])
                for data in json_data:
                    output += colored(
                        "{}: {}\n".format(title_name, data[title_name]),
                        "yellow", attrs=['bold'])
                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow", attrs=['bold'])
                    list_dictionary(data, n_tab)
                    output += colored(
                        "------------------------------------------------------------------\n",
                        "yellow",
                        attrs=['bold'])
            else:
                output += colored("------------------------------------------------------------------\n",
                                  "yellow", attrs=['bold'])
                output += colored(
                    "{}: {}\n".format(title_name, json_data[title_name]),
                    "yellow", attrs=['bold'])
                output += colored("------------------------------------------------------------------\n",
                                  "yellow", attrs=['bold'])
                list_dictionary(json_data, n_tab)
                output += colored("------------------------------------------------------------------\n",
                                  "yellow", attrs=['bold'])
            pipepager(output, cmd='less -FR')
            output = """""