import json
import flask_mongoengine
import requests

def list_aws_iam_users(apihost, jwt_token):
    try:
        domains = json.loads(requests.get("{}/api/latest/domains".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {"dn_name": domains}

    except flask_mongoengine.DoesNotExist:
        return {'error': "DoesNotExist"}

def get_aws_iam_user(apihost, domain, jwt_token):
    try:
        domain_dict = json.loads(requests.post("{}/api/latest/domains".format(apihost), json={"domains": domain}, headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {'dn_name': domain_dict}

    except flask_mongoengine.DoesNotExist:
        return {'error': "DoesNotExist"}