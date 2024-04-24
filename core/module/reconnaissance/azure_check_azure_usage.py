import flask_mongoengine
import json
import sys
import requests
from core.database import models

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

calls = [
    'None'
]

variables = {
    "SERVICE": {
        "value": "none",
        "required": "false",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "DOMAIN": {
        "value": "",
        "required": "true",
        "description":"The domain of the company to test."
    }
}
description = "Check if federation is configured for a domain."

aws_command = "None"

def exploit(workspace):
    domain = variables['DOMAIN']['value']

    url = 'https://login.microsoftonline.com/getuserrealm.srf?login={}'.format(domain)
    try:
        json_data = json.loads(requests.get(url).text)
        azure_json = {}

        if json_data['NameSpaceType'] == 'Unknown':
            return {"DomainName": {
                "DomainName": domain,
                "Usage": "No Azure Usage"
            }}, 404
        elif json_data['NameSpaceType'] == 'Managed':
            url_tenantId = "https://login.microsoftonline.com/{}/v2.0/.well-known/openid-configuration".format(domain)
            tenantId = (json.loads(requests.get(url_tenantId).text)['token_endpoint']).split("/")[3]

            azure_json = {
                "Usage": "Azure",
                "DomainName": json_data['DomainName'],
                "FederationBrandName": json_data['FederationBrandName'],
                "CloudInstanceName": json_data['CloudInstanceName'],
                "CloudInstanceIssuerUri": json_data['CloudInstanceIssuerUri'],
                "TenantID": tenantId
                }

        elif json_data['NameSpaceType'] == 'Federated':
            url_tenantId = "https://login.microsoftonline.com/{}/v2.0/.well-known/openid-configuration".format(domain)
            tenantId = (json.loads(requests.get(url_tenantId).text)['token_endpoint']).split("/")[3]

            #azure_json['DomainName'] = {
            azure_json = {
                "Usage": "Federation",
                "DomainName": json_data['DomainName'],
                "AuthURL": json_data['AuthURL'],
                "FederationBrandName": json_data['FederationBrandName'],
                "CloudInstanceName": json_data['CloudInstanceName'],
                "CloudInstanceIssuerUri": json_data['CloudInstanceIssuerUri'],
                "TenantID": tenantId
            }

        saved_json = {
            "usage": str(azure_json['Usage']),
            "federation_brandname": azure_json['FederationBrandName'],
            "cloud_instance_name": azure_json['CloudInstanceName'],
            "cloud_instance_issuer_uri": azure_json['CloudInstanceIssuerUri'],
            "tenant_id": azure_json['TenantID']
        }

        if 'AuthURL' in azure_json:
            saved_json['auth_url'] = azure_json['AuthURL']

        try:
            database_data = {"azureUsage": saved_json}
            #models.AzureADUsage.objects().get(domain_name=saved_json['domain_name']).update(**saved_json)
            models.Domains.objects().get(dn_name=azure_json['DomainName']).update(**database_data)

        except flask_mongoengine.DoesNotExist:
            database_data = {
                "dn_name": azure_json['DomainName'],
                "azureUsage": saved_json
            }

            #models.AzureADUsage(**saved_json).save()
            models.Domains(**database_data).save()

        response_data = {"DomainName": azure_json}
        return response_data, 200

    except KeyError:
        return {"error": "AzureAD not configured."}, 404

    except:
        return {"error": str(sys.exc_info()[1])}, 501