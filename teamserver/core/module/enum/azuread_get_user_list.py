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
        userListInfo = json.loads(requests.get("https://graph.microsoft.com/v1.0/users",
                           headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)
                           }).text
                        )
        if 'error' in userListInfo:
            return {"error": userListInfo['error']}
        else:
            userInfo = userListInfo['value']

        while "@odata.nextLink" in userListInfo:
            usersURL = userListInfo["@odata.nextLink"]
            userListInfo = json.loads(requests.get(usersURL,
                                               headers={
                                                   'Content-Type': 'application/json',
                                                   'Authorization': 'Bearer {}'.format(access_token)
                                               }).text
                                  )
            if 'error' in userInfo:
                return {"error": userListInfo['error']}
            else:
                userInfo.extend(userListInfo['value'])

        for user in userInfo:
            allInfo.append(user['userPrincipalName'])

    except Exception as e:
        #allInfo['UserInfo'] = str(e)
        return {"error": str(e)}

    #print(json.dumps(allInfo, indent=4, default=str))
    #returnedInfo["InfoType"] = allInfo
    return {"DataType": {"DataType": "Users",
							 "UserList": allInfo}}