from mongoengine import DoesNotExist
from termcolor import colored
import dns.resolver
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from pydoc import pipepager
import sys
import urllib.request
from requests.exceptions import ConnectionError
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
    "BASENAME": {
        "value": "",
        "required": "false",
        "description": "A single basename or several basenames spearated by comma."
    },
    "WORDLIST": {
        "value": "",
        "required": "false",
        "description": "The wordlist of basenames."
    },
    "AZREGION": {
        "value": "",
        "required": "false",
        "description": "The region to test it against. If it's empty, it will fuzz it against all of them."
    }
}

char_array = [
    'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't',
    'u', 'v', 'x', 'y', 'z',
    '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9'
    ]

regions = [
    'eastus', 'eastus2', 'southcentralus', 'westus2', 'westus3', 'australiaeast',
    'southeastasia', 'northeurope', 'swedencentral', 'uksouth', 'westeurope',
    'centralus', 'southafricanorth', 'centralindia', 'eastasia', 'japaneast',
    'koreacentral', 'canadacentral', 'francecentral', 'germanywestcentral',
    'norwayeast', 'brazilsouth', 'eastus2euap', 'centralusstage', 'eastusstage',
    'eastus2stage', 'northcentralusstage', 'southcentralusstage', 'westusstage',
    'westus2stage', 'asia', 'asiapacific', 'australia', 'brazil', 'canada',
    'europe', 'france', 'germany', 'global', 'india', 'japan', 'korea', 'norway',
    'southafrica', 'switzerland', 'uae', 'uk', 'unitedstates', 'unitedstateseuap',
    'eastasiastage', 'southeastasiastage', 'northcentralus', 'westus', 'jioindiawest',
    'switzerlandnorth', 'uaenorth', 'centraluseuap', 'westcentralus', 'southafricawest',
    'australiacentral', 'australiacentral2', 'australiasoutheast', 'japanwest',
    'jioindiacentral', 'koreasouth', 'southindia', 'westindia', 'canadaeast', 'francesouth',
    'germanynorth', 'norwaywest', 'switzerlandwest', 'ukwest', 'uaecentral', 'brazilsoutheast'
]

description = "Gets the name of a basename or a list of basenames separated by comma (',') or a wordlist of the basename and bruteforces the name of the services by sending DNS Requests to them."

aws_command = "No awscli command"

def exploit(workspace):
    objects = []
    basenames = {}
    array = [0, 0, 0, 0, 0, 0, 0, 0]

    region = variables['AZREGION']['value']

    try:
        if variables['BASENAME']['value'] == "" and variables['WORDLIST']['value'] != "":
            try:
                file = open(variables['WORDLIST']['value'], 'r')
            except FileNotFoundError as e:
                return {"error": "File {} not found. Try adding the full path.".format(variables['WORDLIST']['value'])}, 500

            except:
                e = str(sys.exc_info()[1])
                return {"error": e}, 500

            for basename in file.readlines():
                basename = basename.replace("\n", "").strip()
                for index in range(0, 8):
                    for a in range(0, 35):
                        random_part = generate_random_part(array, index)
                        if region == "":
                            for r in regions:
                                try:
                                    url = "{0}-dns-{1}.hcp.{2}.azmk8s.io".format(basename, random_part, r)
                                    dns.resolver.resolve(url)
                                    basenames[url] = "AKS Endpoint"
                                except dns.resolver.NXDOMAIN:
                                    pass
                        else:
                            try:
                                url = "{0}-dns-{1}.hcp.{2}.azmk8s.io".format(basename, random_part, region)
                                print(url)
                                dns.resolver.resolve(url)
                                basenames[url] = "AKS Endpoint"
                            except dns.resolver.NXDOMAIN:
                                pass

                all_services = {
                    "azure_services_base_name": basename,
                    "azure_services_dns_list": basenames
                }
                objects.append(all_services)
                basenames = []

                try:
                    models.AzureServices.objects().get(azure_services_base_name=basename).update(
                        **all_services)

                except flask_mongoengine.DoesNotExist:
                    models.AzureServices(**all_services).save()

                except:
                    pass

            return {"azure_services_base_name": objects}, 200

        elif variables['BASENAME']['value'] != "" and variables['WORDLIST']['value'] == "":
            all_basenameets = variables['BASENAME']['value'].split(",")

            for basename in all_basenameets:
                basename = basename.replace("\n", "").strip()
                for index in range(0, 8):
                    for a in range(0, 35):
                        random_part = generate_random_part(array, index)
                        if region == "":
                            for r in regions:
                                try:
                                    url = "{0}-dns-{1}.hcp.{2}.azmk8s.io".format(basename, random_part, r)
                                    dns.resolver.resolve(url)
                                    basenames[url] = "AKS Endpoint"
                                except dns.resolver.NXDOMAIN:
                                    pass
                        else:
                            try:
                                url = "{0}-dns-{1}.hcp.{2}.azmk8s.io".format(basename, random_part, region)
                                dns.resolver.resolve(url)
                                basenames[url] = "AKS Endpoint"
                            except dns.resolver.NXDOMAIN:
                                pass

                all_services = {
                    "azure_services_base_name": basename,
                    "azure_services_dns_list": basenames
                }
                objects.append(all_services)
                basenames = []

                try:
                    models.AzureServices.objects().get(azure_services_base_name=basename).update(
                        **all_services)

                except flask_mongoengine.DoesNotExist:
                    models.AzureServices(**all_services).save()
                except:
                    pass

            print(objects)
            return {"azure_services_base_name": objects}, 200
        else:
            return {"error": "[*] Add either a basenameet or a wordlist of basenameets."}, 404

    except:
        return {"error": str(sys.exc_info()[1])}, 500

def generate_random_part(array, index):
    if array[index] == 34:
        pass
    else:
        array[index] = array[index] + 1

    string = ""
    for i in array:
        string += char_array[i]

    return string