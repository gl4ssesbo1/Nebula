import json
import requests

def getuid(profile_dict):
    headers = {
        'Authorization': 'Bearer ' + profile_dict['azure_access_token']
    }

    user = requests.get("https://graph.microsoft.com/beta/me", headers=headers)
    if user.status_code == 200:
        return user.json()

    else:
        return {"error": user.text}
