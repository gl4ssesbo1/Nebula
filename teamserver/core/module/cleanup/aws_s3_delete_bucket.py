import boto3
import botocore.exceptions
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

description = "Gets the name of a bucket and deletes it. The bucket policy should allow it."

aws_command = "aws s3 delete-bucket --region {} --profile {}"

def exploit(profile, workspace):
    bucket = variables['BUCKET']['value']
    try:
        profile.delete_bucket(
            Bucket=bucket,
        )
        status = "Successfully Deleted"

    except Exception as e:
        if "BucketNotEmpty" in str(e):
            try:
                objects = profile.list_objects_v2(Bucket=bucket)["Contents"]
                objects = list(map(lambda x: {"Key": x["Key"]}, objects))
                profile.delete_objects(Bucket=bucket, Delete={"Objects": objects})

                profile.delete_bucket(
                    Bucket=bucket,
                )
                status = "Successfully Deleted"
            except Exception as e:
                status = f"Not Deleted: {str(e)}"
        else:
            status = f"Not Deleted: {str(e)}"
    return {
        "Bucket": {
            "Bucket": bucket,
            "Status": status
        }
    }

