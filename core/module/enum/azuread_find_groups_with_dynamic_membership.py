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

description = "This module will try to get all groups with dynamic membership"
aws_command = "No cli command"

def exploit(profile, workspace):
    access_token = profile['azure_access_token']

    allInfo = []

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------

    try:
        groupInfoReq = json.loads(requests.get("https://graph.microsoft.com/beta/groups",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )

        if 'error' in groupInfoReq:
            return {"error": groupInfoReq['error']}
        else:
            groupInfo = groupInfoReq

        while "@odata.nextLink" in groupInfo:
            groupUrl = groupInfoReq["@odata.nextLink"]
            groupInfoReq = json.loads(requests.get(groupUrl,
                                                   headers={
                                                       'Content-Type': 'application/json',
                                                       'Authorization': 'Bearer {}'.format(access_token)
                                                   }).text
                                      )
            if 'error' in groupInfoReq:
                return {"error": groupInfoReq['error']}
            else:
                groupInfo['value'].extend(groupInfoReq['value'])

        for group in groupInfo['value']:
            if group['membershipRule'] is not None:
                groupID = group['id']

                #userGroups = json.loads(requests.get(f"https://graph.microsoft.com/beta/{userID}/transitiveMemberOf/microsoft.graph.group",
                groupUsersReq = json.loads(requests.get(f"https://graph.microsoft.com/beta/groups/{groupID}/members",
                                                   headers={
                                                       'Content-Type': 'application/json',
                                                       'Authorization': 'Bearer {}'.format(access_token)
                                                   }).text
                                      )
                if 'error' in groupUsersReq:
                    return {"error": groupInfo['error']}
                else:
                    groupUsers = groupUsersReq

                while "@odata.nextLink" in groupUsers:
                    groupUrl = groupUsersReq["@odata.nextLink"]
                    groupUsersReq = json.loads(requests.get(groupUrl,
                                                           headers={
                                                               'Content-Type': 'application/json',
                                                               'Authorization': 'Bearer {}'.format(access_token)
                                                           }).text
                                              )
                    if 'error' in groupUsersReq:
                        return {"error": groupUsersReq['error']}
                    else:
                        groupUsers['value'].extend(groupUsersReq['value'])

                gUsers = []
                if 'error' in groupUsers:
                    group['users'] = groupUsers
                else:
                    #print(json.dumps(groupUsers['value'][0]['userPrincipalName'], indent=4, default=str))
                    if groupUsers is not []:
                        for gUser in groupUsers['value']:
                            if not 'userPrincipalName' in gUser:
                                if gUser["@odata.type"] == "#microsoft.graph.device":
                                    gUsers.append(f"Device: {gUser['id']}")
                            else:
                                gUsers.append(gUser['userPrincipalName'])
                    group['users'] = gUsers

                groupAttachedRolesReq = json.loads(
                    requests.get(f"https://graph.microsoft.com/beta/rolemanagement/directory/transitiveRoleAssignments?$filter=principalId eq '{groupID}'",
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': 'Bearer {}'.format(access_token),
                                     'ConsistencyLevel': 'eventual'
                                 }).text
                    )


                if 'error' in groupAttachedRolesReq:
                    group['groupAttachedRoles'] = groupAttachedRoles
                else:
                    groupAttachedRoles = groupAttachedRolesReq

                while "@odata.nextLink" in groupAttachedRoles:
                    groupUrl = groupAttachedRoles["@odata.nextLink"]
                    groupAttachedRolesReq = json.loads(requests.get(groupUrl,
                                                                    headers={
                                                                        'Content-Type': 'application/json',
                                                                        'Authorization': 'Bearer {}'.format(
                                                                            access_token),
                                                                        'ConsistencyLevel': 'eventual'
                                                                    }).text
                                              )
                    if 'error' in groupAttachedRolesReq:
                        return {"error": groupAttachedRolesReq['error']}
                    else:
                        groupAttachedRoles['value'].extend(groupAttachedRolesReq['value'])


                group['groupAttachedRoles'] = groupAttachedRoles['value']
                allInfo.append(group)

    except:
        #allInfo['UserInfo'] = str(sys.exc_info())
        return {"error": str(sys.exc_info())}

    print(allInfo)

    #print(json.dumps(allInfo, indent=4, default=str))
    #returnedInfo["InfoType"] = allInfo
    return {"displayName": allInfo}