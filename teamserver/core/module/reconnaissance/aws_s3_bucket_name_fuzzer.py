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
        "value": "s3",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "BUCKET": {
        "value": "",
        "required": "false",
        "description": "A single bucket or several buckets spearated by comma."
    },
    "WORDLIST": {
        "value": "",
        "required": "false",
        "description": "The wordlist of buckets.",
        "iswordlist": True,
        "wordlistvalue": []
    }
}

description = "Gets the name of a bucket or a list of buckets separated by comma (',') or a wordlist of the bucket name and bruteforces the name of the bucket by sending a request to https://<bucketname>.s3.<region>.amazonaws.com or if it's a website by querying http://<bucketname>.s3-<region>.amazonaws.com."

aws_command = "No awscli command"


def exploit(workspace):
    buckets = []

    if variables['BUCKET']['value'] == "" and variables['WORDLIST']['value'] != "":
        bucklist = variables['WORDLIST']['wordlistvalue']
    elif variables['BUCKET']['value'] != "" and variables['WORDLIST']['value'] == "":
        bucklist = (variables['BUCKET']['value']).split(",")
    else:
        return {
            "error": "Please put either BUCKET or WORDLIST. Not both, not none"
        }

    try:
        for buck in bucklist:
            buck = buck.replace("\n", "").strip()
            objects = getBucket(buck)
            if objects is not None:
                buckets.append(objects)
        for s3object in buckets:
            try:
                # models.AzureADUsage.objects().get(domain_name=saved_json['domain_name']).update(**saved_json)
                models.AWSS3Bucket.objects().get(aws_s3_bucket_name=s3object['aws_s3_bucket_name']).update(
                    **s3object)

            except flask_mongoengine.DoesNotExist:
                # models.AzureADUsage(**saved_json).save()
                models.AWSS3Bucket(**s3object).save()
            except Exception as e:
                pass

            return {"aws_s3_bucket_name": buckets}, 200
        else:
            return {"error": "[*] Add either a bucket or a wordlist of buckets."}, 404

    except Exception as e:
        return {"error": str(e)}, 500


def getBucket(buck):
    objects = {}
    try:
        s3_url = "http://{0}.s3.amazonaws.com".format(buck)
        response = requests.get(s3_url)

        if response.status_code == 200:
            tree = ET.ElementTree(
                ET.fromstring((response.text).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', "")))

            # tree = ET.parse(filename)
            root = tree.getroot()
            tag_keys = []
            tag_date = []
            for t in root.findall(".//Key"):
                tag_keys.append(t.text)

            for t in root.findall(".//LastModified"):
                tag_date.append(t.text)

            res = {tag_keys[i]: tag_date[i] for i, _ in enumerate(tag_date)}

            try:
                s3_website_url = "http://{0}.s3-website.amazonaws.com".format(buck)
                website_code = requests.get(s3_website_url).status_code
                if website_code == 200:
                    objects["aws_s3_is_website"] = True

            except ConnectionError:
                objects["aws_s3_is_website"] = False

            objects["aws_s3_bucket_name"] = buck
            objects["aws_s3_bucket_policy_status"] = "Public"
            objects["aws_s3_bucket_objects"] = {}
            objects["aws_s3_bucket_objects"] = res

            return objects

        elif response.status_code == 403:
            objects["aws_s3_bucket_name"] = buck
            objects["aws_s3_bucket_policy_status"] = "Private"
            try:
                s3_website_url = "http://{0}.s3-website.amazonaws.com".format(buck)
                website_code = requests.get(s3_website_url).status_code
                if website_code == 200:
                    objects["aws_s3_is_website"] = True

            except ConnectionError:
                objects["aws_s3_is_website"] = False

            return objects

        else:
            return None
    except ConnectionError:
        return None
