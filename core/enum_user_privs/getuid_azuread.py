import msal
import requests
from datetime import datetime
import json
from termcolor import colored
import sys

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


def getuid(profile_dict, workspace):
    global output
    n_tab = 0

    json_data = {}

    ENDPOINT = 'https://graph.microsoft.com/v1.0'

    #tenant = profile_dict['tenantId']

    #ENDPOINT = 'https://graph.windows.net/{}/me'.format(tenant)

    headers = {
        'Authorization': 'Bearer ' + profile_dict['access_token']
    }

    print(headers)

    user = requests.get("{}/me".format(ENDPOINT), headers=headers)
    if user.status_code == 200:
        userPrincipalName = user.json()['userPrincipalName']
        json_data[userPrincipalName] = user.json()
    else:
        print(user.status_code)

    users = requests.get("{}/users".format(ENDPOINT), headers=headers)
    if users.status_code == 200:
        json_data["Users"] = users.json()
    else:
        print(users.status_code)

    groups = requests.get("{}/groups".format(ENDPOINT), headers=headers)
    if groups.status_code == 200:
        json_data["Groups"] = groups.json()
    else:
        print(groups.status_code)
        print(groups.text)


    print(json.dumps(json_data, indent=4, default=str))
    #print(json.dumps(user.json(), indent=4, default=str))

    '''
            if len(policies) > 0:
                pol_output = []
                for pol in policies:
                    response = client.get_policy(
                        PolicyArn=pol
                    )
                    if response['ResponseMetadata']:
                        del response['ResponseMetadata']
                    pol_output.append(response)

                if len(pol_output) > 0:
                    for json_data in pol_output:
                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                        output += colored("{}: {}\n".format("Policy", json_data["Policy"]['PolicyName']), "yellow", attrs=['bold'])
                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                        list_dictionary(json_data, n_tab)
                        output += "\n"
                        print(output)
                        output = ""

            all_info['Policies'] = pol_output

        except:
            e = sys.exc_info()
            print(colored("[*] {}".format(e), "red"))

        if not username == "":
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            file = "{}_getuid_{}".format(dt_string, username)
            filename = "./workspaces/{}/{}".format(workspace, file)

            with open(filename, 'w') as dump_file:
                json.dump(all_info, dump_file, indent=4, default=str)
                dump_file.close()

            print(colored("[*] Output is saved to '{}'".format(filename), "green"))
    '''