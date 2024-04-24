import sys
from crtsh import crtshAPI
from core.database import models
import flask_mongoengine

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "DOMAIN": {
        "value": "",
        "required": "true",
        "description": "The domain to search for"
    }
}
description = "Checks for subdomains of the domain by enumerating certificates from crt.sh"

aws_command = "None"


def exploit(workspace):
    try:
        domain = variables['DOMAIN']['value']
        json_data = crtshAPI().search(domain)
        for certs in json_data:
            nv = (certs['name_value']).split("\n")
            certs['name_value'] = nv

        dns_names = []
        for cert in json_data:
            for dns in cert['name_value']:
                dns_names.append(dns)
        uniquedns = set(dns_names)
        dns_list = list(uniquedns)

        return_data = {"Domain":{
                            "Domain": domain,
                            "Domain List": dns_list
                            }
                        }

        database_data = {
            "dn_name": domain,
            "service": "None",
            "subdomains": dns_list
        }

        try:
            models.Domains.objects().get(dn_name=database_data['dn_name']).update(**database_data)

        except flask_mongoengine.DoesNotExist:
            models.Domains(**database_data).save()

        return return_data, 200

    except:
        e = sys.exc_info()[1]
        return {"error": e}, 500