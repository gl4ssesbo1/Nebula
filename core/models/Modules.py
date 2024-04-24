import requests
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required
import sys
import os
from core.run_module import run_azuread_module
from core.run_module import run_azure_module
from core.run_module import run_aws_module
from core.run_module import run_gcp_module
from core.run_module import run_office365_module
from core.run_module import run_digitalocean_module
import json
from core.database.models import AWSCredentials
from core.database.models import AZURECredentials
from core.database.models import DigitalOceanCredentials
from datetime import datetime

from termcolor import colored

module_blueprint = Blueprint('modules', __name__)

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
    'postexploitation'
]

nr_of_modules = {
    'cleanup': "",
    'detection': "",
    'detectionbypass': "",
    'enum': "",
    'exploit': "",
    'lateralmovement': "",
    'listeners': "",
    'persistence': "",
    'privesc': "",
    'reconnaissance': "",
    'stager': "",
    'misc': "",
    'postexploitation': ""
}

nr_of_cloud_modules = {
    "aws": 0,
    "gcp": 0,
    "azure": 0,
    "o365": 0,
    "docker": 0,
    "kube": 0,
    "misc": 0,
    "azuread": 0,
    "digitalocean": 0
}

clouds = [
    "aws",
    "gcp",
    "azure",
    "o365",
    "docker",
    "kube",
    "azuread",
    "misc",
    "digitalocean"
]


@module_blueprint.route('/api/latest/modules', methods=['GET'])
@jwt_required()
def list_modules():
    allmodules = []
    for module in show:
        arr = os.listdir("./core/module/" + module)
        for x in arr:
            if "__" in x:
                continue
            elif ".git" in x:
                continue
            else:
                list1 = {}
                mod = module + "/" + x.split(".py")[0]
                thedir = mod.split("/")[0]
                sys.path.insert(0, "./core/module/" + thedir)

                imported_module = __import__(mod.split("/")[1])
                list1['amodule'] = mod
                list1['description'] = imported_module.description
                allmodules.append(list1)

    return {"modules": allmodules}, 200


@module_blueprint.route('/api/latest/modules/count', methods=['GET'])
@jwt_required()
def module_count():
    all_count = 0
    for module in show:
        module_count = 0
        arr = os.listdir("./core/module/" + module)
        for x in arr:
            if "__" in x:
                continue
            elif ".git" in x:
                continue
            else:
                module_count += 1
                all_count += 1
        if module_count == 0:
            nr_of_modules[module] = "0"
        else:
            nr_of_modules[module] = module_count

    for cloud in clouds:
        module_count = 0
        for module in show:
            arr = os.listdir("./core/module/" + module)
            for x in arr:
                if "__" in x:
                    continue
                elif ".git" in x:
                    continue
                else:
                    if x.split("_")[0] == cloud:
                        module_count += 1
        nr_of_cloud_modules[cloud] = module_count

    return {"all_count": all_count, "nr_of_modules": nr_of_modules, "nr_of_cloud_modules": nr_of_cloud_modules}, 200


# Use Module
@module_blueprint.route('/api/latest/modules/use', methods=['POST'])
def get_module():
    body = request.get_json()
    module = body['module']
    try:
        thedir = module.split("/")[0]
        sys.path.insert(0, "./core/module/" + thedir)
        module_char = (module).split("/")[1]
        imported_module = __import__(module_char)

        variables = imported_module.variables
        description = imported_module.description
        cli_comm = imported_module.aws_command
        needs_creds = imported_module.needs_creds
        author = imported_module.author

        try:
            calls = imported_module.calls
        except:
            calls = ''

        return {
                   "module_name": module,
                   "module_options": variables,
                   "description": description,
                   "cli_comm": cli_comm,
                   "needs_creds": needs_creds,
                   "author": author,
                   "calls": calls
               }, 200

    except(ModuleNotFoundError):
        return {"error": "Module does not exist"}, 404

# Run Module
@module_blueprint.route('/api/latest/modules/run', methods=['POST'])
def set_module():
    body = request.get_json()

    module = body['module']
    module_options = body['module_options']
    cred_prof = body['cred-prof']
    useragent = body['user-agent']
    workspace = body['workspace']
    web_proxies = body['web-proxies']
    username = body["username"]
    awsregion = body['awsregion']

    # aws_sessions = json.loads(requests.get("{}/api/latest/awscredentials".format(apihost),headers={"Authorization": "Bearer {}".format(jwt_token)}).text)

    aws_sessions = json.loads(AWSCredentials.objects().to_json())
    azure_sessions = json.loads(AZURECredentials.objects().to_json())
    do_sessions = json.loads(DigitalOceanCredentials.objects().to_json())
    all_sessions = []

    for aws_sess in aws_sessions:
        #region = ""
        #if 'aws_region' in aws_sess:
        #    region = aws_sess['aws_region']
        if "aws_session_token" in aws_sess:
            all_sessions.append(
                {
                    'provider': 'AWS',
                    'profile': aws_sess['aws_profile_name'],
                    'access_key_id': aws_sess['aws_access_key'],
                    'secret_key': aws_sess['aws_secret_key'],
                    'session_token': aws_sess['aws_session_token'],
                    'region': awsregion
                }
            )
        else:
            all_sessions.append(
                {
                    'provider': 'AWS',
                    'profile': aws_sess['aws_profile_name'],
                    'access_key_id': aws_sess['aws_access_key'],
                    'secret_key': aws_sess['aws_secret_key'],
                    'region': awsregion
                }
            )

    for az_sess in azure_sessions:
        az_sess['profile'] = az_sess['azure_creds_id']
        del (az_sess['azure_creds_id'])
        az_sess['provider'] = 'AZURE'

        all_sessions.append(az_sess)

    for do_sess in do_sessions:
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

    try:
        thedir = module.split("/")[0]
        sys.path.insert(0, "./core/module/" + thedir)
        imported_module = __import__(module.split("/")[1])
        imported_module.variables = module_options
        m_name = (module.split("/")[1]).split("_")[0]

        if m_name == 'aws':
            try:
                print(colored(f"[*] User {username} ran module {module} at {str(datetime.now())} on region {awsregion}", "yellow"))
                return run_aws_module.run_aws_module(imported_module, all_sessions, cred_prof, useragent, web_proxies)

            except:
                return {"error": str(sys.exc_info()[1])}, 500

        elif m_name == 'digitalocean':
            try:
                print("Running DigitalOcean Module")
                return run_digitalocean_module.run_digitalocean_module(imported_module, all_sessions, cred_prof,
                                                                       useragent)

            except:
                return {"error": str(sys.exc_info()[1])}, 500

        elif m_name == 'azure':
            try:
                return run_azure_module.run_azure_module(
                    imported_module, all_sessions, cred_prof, workspace, useragent)

            except:
                return {"error": str(sys.exc_info()[1])}, 500

        elif m_name == 'azuread':
            try:
                return run_azuread_module.run_azuread_module(imported_module, all_sessions,
                                                             cred_prof, useragent,
                                                             )
            except:
                return {"error": str(sys.exc_info()[1])}, 500

        elif m_name == 'office365':
            try:
                return run_office365_module.run_o365_module(
                                                            imported_module, all_sessions,
                                                             cred_prof, useragent
                                                             )
            except:
                return {"error": str(sys.exc_info()[1])}, 500

        elif m_name == 'gcp':
            try:
                return run_gcp_module.run_gcp_module(imported_module, all_sessions, cred_prof, useragent)

            except:
                return {"error": str(sys.exc_info()[1])}, 500
        else:
            try:
                return imported_module.exploit(workspace)
            except:
                return {"error": str(sys.exc_info()[1])}, 500
    except(ModuleNotFoundError):
        return {"error": "Module does not exist"}, 404
