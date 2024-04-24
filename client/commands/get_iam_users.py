import json
import flask_mongoengine
import requests

def list_aws_iam_users(apihost, jwt_token):
    try:
        users = json.loads(requests.get("{}/api/latest/awsusers".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {"aws_username": users}

    except flask_mongoengine.DoesNotExist:
        return {'error': "DoesNotExist"}

def get_aws_iam_user(apihost, user, jwt_token):
    try:
        user_dict = json.loads(requests.post("{}/api/latest/awsusers".format(apihost), json={"aws_username": user}, headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {'aws_username': user_dict['aws_username']}

    except flask_mongoengine.DoesNotExist:
        return {'error': "DoesNotExist"}

