import sys

import requests
import json
import flask_mongoengine

def get_user_id(apihost, jwt_token, profile_dict):
    try:
        users = json.loads(requests.get("{}/api/latest/clientcommands".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}, json=profile_dict).text)
        return users

    except flask_mongoengine.DoesNotExist:
        return {'error': str(sys.exc_info()[1])}

