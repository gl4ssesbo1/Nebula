import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import json
from datetime import datetime
from termcolor import colored
import sys

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "s3",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "BUCKETNAME": {
        "value": "",
        "required": "true",
        "description":"The name of the bucket to test."
    }
}
description = "Shows if a module is public or not"

aws_command = "aws s3api get-bucket-policy-status --bucket my-bucket --region <region> --profile <profile>"

def exploit(profile, workspace):
    json_data = {}
    bucket = variables['BUCKETNAME']['value']
    now = datetime.now()
    title_name = 'BucketName'
    dt_string = now.strftime('%d_%m_%Y_%H_%M_%S')
    file = "{}_s3_get_bucket_policy_status".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    try:
        json_data = profile.get_bucket_policy_status(
            Bucket=bucket
        )['PolicyStatus']
        json_data['BucketName'] = bucket
    except:
        e = sys.exc_info()[1]
        print(type(e))
        if "NoSuchBucketPolicy" in str(e):
            json_data['BucketName'] = bucket
            json_data['IsPublic'] = False
        else:
            print(colored(
                "[*] {}".format(e), "red"
            ))

    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    print(colored("---------------------------------", "yellow", attrs=['bold']))
    print(colored("{}: {}".format(title_name, bucket), "yellow", attrs=['bold']))
    print(colored("---------------------------------", "yellow", attrs=['bold']))
    for key,value in json_data.items():
        print("\t{}: {}".format(colored(key,"red",attrs=['bold']), colored(value,"blue")))
    print(colored("---------------------------------", "yellow", attrs=['bold']))