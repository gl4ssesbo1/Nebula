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
    },
    "AADOBJECT": {
        "value": "all",
        "required": "true",
        "description": "The objects to test. By default is all, but can also be me, users or groups"
    }
}

description = "This module will try to get as many information on the user's account on O365, based on the its privileges."
aws_command = "No cli command"

def exploit(profile, workspace):
    access_token = profile['azure_access_token']
    aadObjectType = variables['AADOBJECT']['value']

    if aadObjectType != "all" and aadObjectType != "me" and aadObjectType != "groups" and aadObjectType != "users":
        return {"error": "Please provide AADOBJECT as \"me\", \"users\" or \"groups\"."}

    returnedInfo = {
        "AADObject": {}
    }

    allInfo = []

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------
    if aadObjectType == "me" or aadObjectType == "all":
        try:
            print("look me")
            meInfo = json.loads(requests.get("https://graph.microsoft.com/beta/me",
                               headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(access_token)
                               }).text
                            )
            print("looked me")
            #meGroups = json.loads(requests.get("https://graph.microsoft.com/beta/me/transitiveMemberOf/microsoft.graph.group",
            meGroups = json.loads(requests.get("https://graph.microsoft.com/beta/me/transitiveMemberOf/microsoft.graph.group",
                                             headers={
                                                 'Content-Type': 'application/json',
                                                 'Authorization': 'Bearer {}'.format(access_token)
                                             }).text
                                )
            print("look me groups")
            print(meGroups)
            meInfo['MyGroups'] = meGroups['value']
            meID = meInfo['id']

            print("look me privileges")
            meAttachedRoles = json.loads(
                requests.get(
                    f"https://graph.microsoft.com/beta/rolemanagement/directory/transitiveRoleAssignments?$filter=principalId eq '{meID}'",
                    #f"https://graph.microsoft.com/beta/rolemanagement/directory/transitiveRoleAssignments?$filter=principalId eq '48d31887-5fad-4d73-a9f5-3c356e68a038'",
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer {}'.format(access_token),
                        'ConsistencyLevel': 'eventual'
                    }).text
            )
            print("looked me privs")
            meInfo['meAttachedRoles'] = meAttachedRoles['value']


            allInfo.append(meInfo)
            allInfo[0]['AADObject'] = "MeInfo"

        except:
            #allInfo['MeInfo'] = str(sys.exc_info())
            return {"error": str(sys.exc_info())}

    if aadObjectType == "users" or aadObjectType == "all":
        try:
            userInfo = json.loads(requests.get("https://graph.microsoft.com/v1.0/users",
                               headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {}'.format(access_token)
                               }).text
                            )
            if 'error' in userInfo:
                allInfo["UserInfo"] = userInfo
            else:
                for user in userInfo['value']:
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

            allInfo.append(userInfo)
            if aadObjectType == "users":
                allInfo[1]['AADObject'] = "UserInfo"
            else:
                allInfo[0]['AADObject'] = "UserInfo"

        except:
            #allInfo['UserInfo'] = str(sys.exc_info())
            return {"error": str(sys.exc_info())}

    #print(json.dumps(allInfo, indent=4, default=str))
    #returnedInfo["AADObject"] = allInfo
    return {"AADObject": allInfo}