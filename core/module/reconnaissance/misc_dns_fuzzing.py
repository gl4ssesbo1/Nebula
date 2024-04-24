import sys

import dns.resolver
import flask_mongoengine

from core.database import models

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
        "description": "The domain to check"
    },
    "WORDLIST": {
        "value": "",
        "required": "true",
        "description": "The wordlist of hosts."
    }
}

description = "Get a list of hosts and checks if they exist."

aws_command = "No awscli command"


def exploit(workspace):
    objects = []
    domain = variables['DOMAIN']['value']

    try:
        try:
            file = open(variables['WORDLIST']['value'], 'r')
        except FileNotFoundError as e:
            return {"error": "File {} not found. Try adding the full path.".format(
                variables['WORDLIST']['value'])}, 500

        except:
            e = str(sys.exc_info()[1])
            return {"error": e}, 500

        for host in file.readlines():
            try:
                host = host.replace("\n", "").strip()
                dns.resolver.resolve("{0}.{1}".format(host, domain))
                objects.append("{0}.{1}".format(host, domain))
            except:
                pass

        return {"wordlist": {
            "wordlist": variables['WORDLIST']['value'],
            "output": objects
        }}, 200

    except:
        return {"error": str(sys.exc_info()[1])}, 500
