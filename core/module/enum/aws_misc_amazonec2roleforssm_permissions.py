import sys

import boto3
import json
import botocore.exceptions

from core.database.models import AWSUsers
from flask_mongoengine import DoesNotExist

from core.createSession.giveMeClient import giveMeClient

import os

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "BUCKETNAME": {
        "value": "",
        "required": "false",
        "description": "A single bucket name to test. Either put this or BUCKETFILE, not both."
    },
    "BUCKETFILE": {
        "value": "",
        "required": "false",
        "description": "A file with bucket names to check. Either put this or BUCKETNAME, not both.",
        "iswordlist": True
    }
}

description = "Test most common privilege escalation APIs to get privesc on the account."

calls = [
    'sts:GetCallerIdentity',
    'ds:DescribeDirectories',
    'iam:GetUser',
    'iam:ListGroupsForUser',
    'iam:ListUserPolicies',
    'iam:ListAttachedUserPolicies'
]

aws_command = "aws iam get-account-authorization-details --region <region> --profile <profile>"

def listObjects(client, bucketName):
    try:
        bucketObjects = client.list_objects()
        del(bucketObjects['ResponseMetadata'])

        return bucketObjects['Contents']
    except botocore.exceptions.NoSuchBucket:
        return {"error": f"Bucket {bucketName} does not exist. Check the name provided or provide an existing one."}

def exploit(all_sessions, cred_prof, useragent, web_proxies):
    bucketName = variables['BUCKETNAME']['value']
    bucketFile = variables['BUCKETFILE']['value']

    all_info = {
        "BucketInfo": {}
    }

    try:
        client = giveMeClient(
            all_sessions,
            cred_prof,
            useragent,
            web_proxies,
            "s3"
        )

        if bucketName != "" and bucketFile != "":
            return {"error": "[*] Either put BUCKETFILE or BUCKETNAME, not both."}

        elif bucketName != "" and bucketFile == "":
            bucketObjects = listObjects(client, bucketName)
            if "error" in bucketObjects:
                all_info['BucketInfo'] = {
                    bucketName: {
                        "error": bucketObjects['error']
                    }
                }
            else:
                all_info['BucketInfo'] = {
                    bucketName: bucketObjects
                }
        elif bucketName == "" and bucketFile != "":
            for bucket in bucketFile:
                bucketObjects = listObjects(client, bucket)
                if "error" in bucketObjects:
                    all_info['BucketInfo'] = {
                        bucketName: bucketObjects['error']
                    }
                else:
                    all_info['BucketInfo'] = {
                        bucketName: bucketObjects
                    }
        else:
            return {"error": "[*] Either put BUCKETFILE or BUCKETNAME, not both."}

    except:
        all_info['BucketInfo'] = dict(error=str(sys.exc_info()))

    try:
        client = giveMeClient(
            all_sessions,
            cred_prof,
            useragent,
            web_proxies,
            "ds"
        )

        directoryInfo = client.describe_instances()
        del (directoryInfo['ResponseMetadata'])

        all_info['DirectoryMessage'] = "AmazonEC2RoleforSSM seems to be used. Try exploit/aws_ds_createdirectorycomputeraccount to create a computer account on any directory if you need it."
        all_info['DirectoryInfo'] = directoryInfo

    except:
        exception = str(sys.exc_info())
        if "Access Denied" in exception:
            all_info['DirectoryMessage'] = "AmazonEC2RoleforSSM seems to be used."
            all_info['DirectoryInfo'] = {}
        else:
            all_info['DirectoryMessage'] = dict(error=exception)
            all_info['DirectoryInfo'] = {}

