import boto3
from termcolor import colored
import os
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
    "BUCKET":{
        "value":"",
        "required":"true",
        "description":"The name of the bucket to delete."
    }
}

description = "Gets the name of a and deletes it."

aws_command = "aws s3 delete-bucket --region {} --profile {}"

def exploit(profile, workspace):
    bucket = variables['BUCKET']['value']
    profile.delete_bucket(
        Bucket=bucket,
    )
    print(colored("[*] Bucket '{}' deleted.".format(bucket), "green"))
