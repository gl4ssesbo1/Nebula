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
    "SPACE": {
        "value": "",
        "required": "false",
        "description": "A single SPACE or several SPACES separated by comma."
    },
    "WORDLIST": {
        "value": "",
        "required": "false",
        "description": "The wordlist of SPACES."
    },
    "REGION": {
        "value": "",
        "required": "true",
        "description": "The region to test the SPACES."
    }
}

description = "Gets the name of a SPACE or a list of SPACES separated by comma (',') or a wordlist of the SPACE name and bruteforces the name of the SPACE by sending a request to https://<SPACEname>.s3.<region>.amazonaws.com or if it's a website by querying http://<SPACEname>.s3-<region>.amazonaws.com."

aws_command = "No awscli command"


def exploit():
    objects = {}
    SPACES = []

    try:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        filen = "{}_spaces".format(dt_string)
        if not os.path.exists(filen):
            os.makedirs("./workspaces/{}".format(filen))

        if variables['SPACE']['value'] == "" and variables['WORDLIST']['value'] != "":
            try:
                filename = variables['WORDLIST']['value']
                #if "~/" in filename:
                #    filename = str(Path.home()) + "" + filename.replace("/~", "/")
                file = open(filename, 'r')

            except FileNotFoundError as e:
                return {"error": "File {} not found. Try adding the full path.".format(variables['WORDLIST']['value'])}, 500

            except:
                e = str(sys.exc_info()[1])
                return {"error": e}, 500

            region = variables["REGION"]["value"]

            for buck in file.readlines():
                buck = buck.replace("\n", "")
                try:
                    do_url = "https://{0}.{1}.digitaloceanspaces.com".format(buck, region)
                    response = requests.get(do_url)

                    if response.status_code == 200:
                        filename = "./workspaces/{}/{}.xml".format(filen, buck.strip("\n"))
                        file = open(filename, "w")
                        file.write((response.text).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', ""))
                        file.close()

                        tree = ET.parse(filename)
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

        elif variables['SPACE']['value'] != "" and variables['WORDLIST']['value'] == "":
            all_SPACES = variables['SPACE']['value'].split(",")
            region = variables["REGION"]["value"]
            for buck in all_SPACES:
                try:
                    #s3_url = "https://{0}.{1}.cdn.digitaloceanspaces.com".format(buck.replace("\n", ""), region)
                    s3_url = "https://{0}.{1}.digitaloceanspaces.com".format(buck, region)
                    print(s3_url)
                    response = requests.get(s3_url)

                    if response.status_code == 200:
                        filename = "./workspaces/{}/{}.xml".format(filen, buck.strip("\n"))
                        file = open(filename, "w")
                        file.write((response.text).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', ""))
                        file.close()

                        tree = ET.parse(filename)
                        root = tree.getroot()
                        tag_keys = []
                        tag_date = []
                        for t in root.findall(".//Key"):
                            tag_keys.append(t.text)

                        for t in root.findall(".//LastModified"):
                            tag_date.append(t.text)

                        res = {tag_keys[i]: tag_date[i] for i, _ in enumerate(tag_date)}

                        try:
                            do_website_url = "https://{0}.{1}.cdn.digitaloceanspaces.com/".format(buck.replace("\n", ""), region)
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
                            do_website_url = "https://{0}.{1}.cdn.digitaloceanspaces.com/".format(
                                buck.replace("\n", ""), region)
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
                    # models.AzureADUsage.objects().get(domain_name=saved_json['domain_name']).update(**saved_json)
                    models.DigitalOceanSpace.objects().get(digitalocean_s3_space_name=s3object['digitalocean_s3_space_name']).update(
                        **s3object)

                except flask_mongoengine.DoesNotExist:
                    # models.AzureADUsage(**saved_json).save()
                    models.DigitalOceanSpace(**s3object).save()
                except:
                    pass

            return {"digitalocean_s3_space_name": SPACES}, 200
        else:
            return {"error": "[*] Add either a SPACE or a wordlist of SPACES."}, 404

    except:
        return {"error": str(sys.exc_info()[1])}, 500
