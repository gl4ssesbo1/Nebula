import sys

import dns.resolver
import flask_mongoengine
import requests

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
    "API_TOKEN": {
        "value": "",
        "required": "true",
        "description": "The token generated for you by GrayHatWarFare."
    },
    "CLOUD_VENDOR": {
        "value": "",
        "required": "false",
        "description": "The vendor to check for. Can be empty or aws, azure or dos, depending on the cloud vendor."
    },
    "FILE_KEYWORDS": {
        "value": "",
        "required": "false",
        "description": "The keyword to search on the bucket's objects."
    },
    "BUCKET_KEYWORDS": {
        "value": "",
        "required": "true",
        "description": "The bucket keywords to search separated by comma and no spaces. Eg: test,testbucket,bucket"
    },
    "NUMBER_OF_RESULTS_TO_BE_RETURNED": {
        "value": "10000",
        "required": "true",
        "description": "Number of results returned. Free users can only get 10000 results, and based on the subscription you have, you can set the value."
    },
    "LIST_OBJECTS": {
        "value": "false",
        "required": "true",
        "description": "If set to true, it will list the objects of each bucket. Else, it will only list the buckets."
    }
}

description = "Find open buckets on GrayHatWarFare. The buckets can be Azure, AWS or DigitalOcean buckets. You'll need an access token, so you'll need an account on GrayHatWarFare."

aws_command = "No awscli command"

def exploit(workspace):
    api_token = variables['API_TOKEN']['value']
    cloud_vendor = variables['CLOUD_VENDOR']['value']

    list_objects_bool = variables['LIST_OBJECTS']['value']

    if not variables['FILE_KEYWORDS']['value'] == "":
        file_keywords = (variables['FILE_KEYWORDS']['value']).replace(" ", "").replace("\n", "").strip().split(",")
    else:
        file_keywords = []
    bucket_keywords = (variables['BUCKET_KEYWORDS']['value']).replace(" ", "").replace("\n", "").strip().split(",")

    returned_clouds = []

    try:
        nr_of_results_to_be_returned = int(variables['NUMBER_OF_RESULTS_TO_BE_RETURNED']['value'])
    except ValueError:
        return {"error": "NUMBER_OF_RESULTS_TO_BE_RETURNED can only be an Integer."}, 500

    for bucket_keyword in bucket_keywords:
        returned_output = bucket_keyword_func(
            bucket_keyword,
            nr_of_results_to_be_returned,
            api_token,
            cloud_vendor
        )

        if "error" in returned_output:
            return returned_output

        if len(returned_output) == 0:
            print("0 returned\n")
            return {"error": "No buckets found for those keywords. Try another one."}

        for bucket in returned_output:
            returned_clouds.append(bucket)

            if list_objects_bool.replace("\n", "").replace(" ", "").strip() == "true":
                if len(file_keywords) == 0:
                    bucket_files = object_keyword_func(
                        [],
                        nr_of_results_to_be_returned,
                        api_token,
                        bucket['id']
                    )
                    bucket['files'] = bucket_files

                else:
                    for file_keyword in file_keywords:
                        bucket_files = object_keyword_func(
                            file_keyword,
                            nr_of_results_to_be_returned,
                            api_token,
                            bucket['id']
                        )

                        bucket['files'] = bucket_files

    return {'bucket': returned_clouds}

def bucket_keyword_func(keyword, nr_of_results_to_be_returned, api_token, cloud_vendor):
    '''bucket_url = "https://buckets.grayhatwarfare.com/api/v1/buckets/0/{}?access_token={}".format(
        str(nr_of_results_to_be_returned),
        api_token.replace("\n", "").strip()
    )'''

    bucket_url = f"https://buckets.grayhatwarfare.com/api/v1/buckets/0/{nr_of_results_to_be_returned}"

    params = {
        "access_token": api_token,
        "keywords": keyword,
        "type": cloud_vendor
    }

    # bucket_url += "&keyword={}".format(keyword)

    try:
        buckets_found = requests.get(
            bucket_url,
            params=params
        ).json()

        if "buckets" in buckets_found:
            return buckets_found["buckets"]

    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Check internet access."}

    except Exception as e:
        pass

def object_keyword_func(keyword, nr_of_results_to_be_returned, api_token, bucket_id):
    bucket_url = "https://buckets.grayhatwarfare.com/api/v1/bucket/{}/files/0/{}".format(
        str(bucket_id),
        nr_of_results_to_be_returned
    )

    params = {
        "access_token": api_token,
    }

    if not keyword == "":
        params["keywords"] = keyword

    # bucket_url += "&keyword={}".format(keyword)

    try:
        files_found = requests.get(
            bucket_url,
            params=params
        ).json()
        return files_found["files"]

    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Check internet access."}

    except Exception as e:
        pass