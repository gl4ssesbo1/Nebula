import json
import requests

def list_domains(apihost, jwt_token):
    try:
        domains = json.loads(requests.get("{}/api/latest/domains".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {"dn_name": domains}

    except Exception as e:
        return {'error': f"Error getting buckets: {str(e)}"}

def get_domains(apihost, domain, jwt_token):
    try:
        domain_dict = json.loads(requests.post("{}/api/latest/domains".format(apihost), json={"dn_name": domain}, headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {'dn_name': domain_dict['dn_name']}

    except Exception as e:
        return {'error': f"Error getting buckets: {str(e)}"}

