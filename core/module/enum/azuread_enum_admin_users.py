import json
import sys
import requests
import random
import string
from flask_mongoengine import DoesNotExist
import datetime
import json

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

description = "This module will try to get as many information on the user's account on O365, based on the its privileges."
aws_command = "No cli command"

def exploit(profile, workspace):
    access_token = profile['azure_access_token']

    allInfo = []

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------

    try:
        userInfo = json.loads(requests.get("https://graph.microsoft.com/v1.0/users",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if 'error' in userInfo:
            return {"error": userInfo['error']}
        else:
            for user in userInfo['value']:
                if "adm." in user['userPrincipalName'] or \
                   "admin." in user['userPrincipalName'] or \
                   "adm-" in user['userPrincipalName'] or \
                   ".admin" in user['userPrincipalName'] or \
                   ".adm" in user['userPrincipalName'] or \
                   "-admin" in user['userPrincipalName'] or \
                   "-adm" in user['userPrincipalName']:
                    userID = user['id']

                    #userGroups = json.loads(requests.get(f"https://graph.microsoft.com/beta/{userID}/transitiveMemberOf/microsoft.graph.group",
                    userGroups = json.loads(requests.get(f"https://graph.microsoft.com/beta/users/{userID}/memberOf",
                                                       headers={
                                                           'Content-Type': 'application/json',
                                                           'Authorization': 'Bearer {}'.format(access_token)
                                                       }).text
                                          )
                    if 'error' in userGroups:
                        user['Groups'] = userGroups
                    else:
                        user['Groups'] = userGroups['value']


                    userAttachedRoles = json.loads(
                        requests.get(f"https://graph.microsoft.com/beta/rolemanagement/directory/transitiveRoleAssignments?$filter=principalId eq '{userID}'",
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(access_token),
                                         'ConsistencyLevel': 'eventual'
                                     }).text
                        )
                    if 'error' in userAttachedRoles:
                        user['UserAttachedRoles'] = userAttachedRoles
                    else:
                        user['UserAttachedRoles'] = userAttachedRoles['value']

                    allInfo.append(user)

    except:
        #allInfo['UserInfo'] = str(sys.exc_info())
        return {"error": str(sys.exc_info())}

    #print(json.dumps(allInfo, indent=4, default=str))
    #returnedInfo["InfoType"] = allInfo
    return {"displayName": allInfo}