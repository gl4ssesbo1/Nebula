import json
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


def PrintAWSModule(run_module_json):
    output = ""

    for region, json_data in run_module_json.items():
        if "error" in json_data:
            print(colored("[*] {}".format(json_data['error']), "red"))
        elif 'clientError' in json_data:
            continue
        else:
            output += colored(
                "------------------------------------------------------------------\n",
                "yellow", attrs=['bold'])

            output += colored(
                "Region: {}\n".format(region),
                "yellow", attrs=['bold'])

            if isinstance(json_data, list):
                for data in json_data:
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
            pipepager(output, cmd='less -FR')
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
            pipepager(output, cmd='less -FR')
            yn = input("Do you want to print the output? [y/N] ")
            if yn != "Y" and yn != "y":
                continue
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