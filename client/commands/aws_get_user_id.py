import sys

import requests
import json
import flask_mongoengine

def get_user_id(apihost, jwt_token, profile_dict, user_agent):
    try:
        jsontosend = {
            "profile_dict": profile_dict,
            "user_agent": user_agent
        }
        users = json.loads(requests.get("{}/api/latest/clientcommands".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}, json=jsontosend).text)
        return users

    except Exception as e:
        return {'error': str(e)}

