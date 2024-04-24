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
        "description": "The wordlist of buckets."
    },
    "REGION": {
        "value": "",
        "required": "true",
        "description": "The region to test the buckets."
    }
}

description = "Gets the name of a bucket or a list of buckets separated by comma (',') or a wordlist of the bucket name and bruteforces the name of the bucket by sending a request to https://<bucketname>.s3.<region>.amazonaws.com or if it's a website by querying http://<bucketname>.s3-<region>.amazonaws.com."

aws_command = "No awscli command"


def exploit():
    objects = {}
    buckets = []

    try:
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        filen = "{}_buckets".format(dt_string)
        if not os.path.exists(filen):
            os.makedirs("./workspaces/{}".format(filen))

        if variables['BUCKET']['value'] == "" and variables['WORDLIST']['value'] != "":
            try:
                file = open(variables['WORDLIST']['value'], 'r')
            except FileNotFoundError as e:
                return {"error": "File {} not found. Try adding the full path.".format(variables['WORDLIST']['value'])}, 500

            except:
                e = str(sys.exc_info()[1])
                return {"error": e}, 500

            region = variables["REGION"]["value"]

            for buck in file.readlines():
                buck = buck.replace("\n", "")
                try:
                    s3_url = "http://{0}.s3.{1}.amazonaws.com".format(buck, region)
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
                            s3_website_url = "http://{0}.s3-website.{1}.amazonaws.com".format(buck, region)
                            website_code = requests.get(s3_website_url).status_code
                            if website_code == 200:
                                objects["aws_s3_is_website"] = True

                        except ConnectionError:
                            objects["aws_s3_is_website"] = False

                        objects["aws_s3_bucket_name"] = buck
                        objects["aws_s3_bucket_policy_status"] = "Public"
                        objects["aws_s3_bucket_objects"] = {}
                        objects["aws_s3_bucket_objects"] = res

                        buckets.append(objects)
                        objects = {}

                    elif response.status_code == 403:
                        objects["aws_s3_bucket_name"] = buck
                        objects["aws_s3_bucket_policy_status"] = "Private"
                        try:
                            s3_website_url = "http://{0}.s3-website.{1}.amazonaws.com".format(buck, region)
                            website_code = requests.get(s3_website_url).status_code
                            if website_code == 200:
                                objects["aws_s3_is_website"] = True

                        except ConnectionError:
                            objects["aws_s3_is_website"] = False

                        buckets.append(objects)
                        objects = {}

                    else:
                        pass
                except ConnectionError:
                    pass



            for s3object in buckets:
                try:
                    # models.AzureADUsage.objects().get(domain_name=saved_json['domain_name']).update(**saved_json)
                    models.AWSS3Bucket.objects().get(aws_s3_bucket_name=s3object['aws_s3_bucket_name']).update(
                        **s3object)

                except flask_mongoengine.DoesNotExist:
                    # models.AzureADUsage(**saved_json).save()
                    models.AWSS3Bucket(**s3object).save()
                except:
                    pass

            return {"aws_s3_bucket_name": buckets}, 200

        elif variables['BUCKET']['value'] != "" and variables['WORDLIST']['value'] == "":
            all_buckets = variables['BUCKET']['value'].split(",")
            region = variables["REGION"]["value"]
            for buck in all_buckets:
                try:
                    s3_url = "http://{0}.s3.{1}.amazonaws.com".format(buck.replace("\n", ""), region)
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
                            s3_website_url = "http://{0}.s3-website.{1}.amazonaws.com".format(buck.replace("\n", ""),
                                                                                              region)
                            website_code = requests.get(s3_website_url).status_code
                            if website_code == 200:
                                objects["aws_s3_is_website"] = True

                        except ConnectionError:
                            objects["aws_s3_is_website"] = False

                        objects["aws_s3_bucket_name"] = buck
                        objects["aws_s3_bucket_policy_status"] = "Public"
                        objects["aws_s3_bucket_objects"] = {}
                        objects["aws_s3_bucket_objects"] = res

                        buckets.append(objects)
                        objects = {}

                    elif response.status_code == 403:
                        objects["aws_s3_bucket_name"] = buck
                        objects["aws_s3_bucket_policy_status"] = "Private"
                        try:
                            s3_website_url = "http://{0}.s3-website.{1}.amazonaws.com".format(buck.replace("\n", ""),
                                                                                              region)
                            website_code = requests.get(s3_website_url).status_code
                            if website_code == 200:
                                objects["aws_s3_is_website"] = True

                        except ConnectionError:
                            objects["aws_s3_is_website"] = False

                        buckets.append(objects)
                        objects = {}

                    else:
                        pass
                except ConnectionError:
                    pass

            for s3object in buckets:
                try:
                    # models.AzureADUsage.objects().get(domain_name=saved_json['domain_name']).update(**saved_json)
                    models.AWSS3Bucket.objects().get(aws_s3_bucket_name=s3object['aws_s3_bucket_name']).update(
                        **s3object)

                except flask_mongoengine.DoesNotExist:
                    # models.AzureADUsage(**saved_json).save()
                    models.AWSS3Bucket(**s3object).save()
                except:
                    pass

            return {"aws_s3_bucket_name": buckets}, 200
        else:
            return {"error": "[*] Add either a bucket or a wordlist of buckets."}, 404

    except:
        return {"error": str(sys.exc_info()[1])}, 500
