from pathlib import Path
from mongoengine import DoesNotExist
from termcolor import colored
import requests
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
        "value": "SPACE",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "WORDLIST": {
        "value": "",
        "required": "false",
        "description": "The wordlist of SPACES.",
        "iswordlist": True,
        "wordlistvalue": []
    }
}

description = "Gets the name of a SPACE or a list of SPACES separated by comma (',') or a wordlist of the SPACE name and bruteforces the name of the SPACE by sending a request to https://<SPACEname>.s3.<region>.amazonaws.com or if it's a website by querying http://<SPACEname>.s3-<region>.amazonaws.com."

aws_command = "No awscli command"

DO_REGIONS = [
    "nyc3",
    "fra1",
    "sfo2",
    "sfo3",
    "ams3",
    "sgp1",
    "blr1",
    "syd1"
]

def exploit():
    objects = {}
    SPACES = []

    try:
        for buck in variables['WORDLIST']['wordlistvalue']:
            for region in DO_REGIONS:
                buck = buck.replace("\n", "")
                try:
                    do_url = "https://{0}.{1}.digitaloceanspaces.com".format(buck, region)
                    response = requests.get(do_url)

                    if response.status_code == 200:
                        tree = ET.ElementTree(
                            ET.fromstring(
                                (response.text).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', "")))
                        root = tree.getroot()
                        tag_keys = []
                        tag_date = []
                        for t in root.findall(".//Key"):
                            tag_keys.append(t.text)

                        for t in root.findall(".//LastModified"):
                            tag_date.append(t.text)

                        res = {tag_keys[i]: tag_date[i] for i, _ in enumerate(tag_date)}

                        try:
                            do_website_url = "https://{0}.{1}.cdn.digitaloceanspaces.com/".format(buck, region)
                            website_code = requests.get(do_website_url).status_code
                            if website_code == 200:
                                objects["digitalocean_s3_is_website"] = True

                        except ConnectionError:
                            objects["digitalocean_s3_is_website"] = False

                        objects["digitalocean_s3_space_name"] = buck
                        objects["digitalocean_s3_space_policy_status"] = "Public"
                        objects["digitalocean_s3_space_objects"] = {}
                        objects["digitalocean_s3_space_objects"] = res

                        SPACES.append(objects)
                        objects = {}

                    elif response.status_code == 403:
                        objects["digitalocean_s3_space_name"] = buck
                        objects["digitalocean_s3_space_policy_status"] = "Private"
                        try:
                            do_website_url = "https://{0}.{1}.cdn.digitaloceanspaces.com".format(buck, region)
                            website_code = requests.get(do_website_url).status_code
                            if website_code == 200:
                                objects["digitalocean_s3_is_website"] = True

                        except ConnectionError:
                            objects["digitalocean_s3_is_website"] = False

                        SPACES.append(objects)
                        objects = {}

                    else:
                        pass
                except ConnectionError:
                    pass



        for s3object in SPACES:
            try:
                models.DigitalOceanSpace.objects().get(digitalocean_s3_space_name=s3object['digitalocean_s3_space_name']).update(
                    **s3object)

            except flask_mongoengine.DoesNotExist:
                models.DigitalOceanSpace(**s3object).save()
            except:
                pass

        return {"digitalocean_s3_space_name": SPACES}, 200


    except:
        return {"error": str(sys.exc_info()[1])}, 500
