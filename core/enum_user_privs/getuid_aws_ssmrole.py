import boto3
import botocore
from datetime import datetime
import json
from termcolor import colored
import sys
from core.createSession.giveMeClient import giveMeClient

from core.database.models import AWSUsers


def getuidssmrole(all_sessions, cred_prof, useragent, web_proxies):
    '''region = profile_dict['aws_region']
    access_key_id = profile_dict['aws_access_key']
    secret_key = profile_dict['aws_secret_key']
    session_token = ""

    if "aws_session_token" in profile_dict:
        session_token = profile_dict['aws_session_token']
    '''

    all_info = {
        "UserName": None,
        "UserID": None,
        "AmazonEC2RoleforRCEUsed": None,
    }

    try:
        client = giveMeClient(
            all_sessions=all_sessions,
            cred_prof=cred_prof,
            useragent=useragent,
            web_proxies=web_proxies,
            service="sts"
        )

        try:
            stsResponse = client.get_caller_identity()
            del (client)
            del (stsResponse['ResponseMetadata'])
            all_info['UserID'] = stsResponse
            all_info['UserName'] = (stsResponse['Arn']).split("/")[-1]

            try:
                client = giveMeClient(
                    all_sessions=all_sessions,
                    cred_prof=cred_prof,
                    useragent=useragent,
                    web_proxies=web_proxies,
                    service="ds"
                )
                dsResponse = client.describe_directories()

                del (dsResponse['ResponseMetadata'])

                # all_info['DirectoryService'] = dsResponse
                del (client)

                client = giveMeClient(
                    all_sessions=all_sessions,
                    cred_prof=cred_prof,
                    useragent=useragent,
                    web_proxies=web_proxies,
                    service="logs"
                )

                dsResponse = client.describe_log_groups()
                del (dsResponse['ResponseMetadata'])
                # all_info['DirectoryService'] = dsResponse

                all_info['AmazonEC2RoleforRCEUsed'] = "AmazonEC2RoleforRCE seems to be used for this role. Use aws_misc_amazonec2roleforssm_permissions to enumerate the services allowed by the role."
                fixed_db_data = db_data(all_info)
            except:
                all_info['AmazonEC2RoleforRCEUsed'] = dsResponse["message"]
                fixed_db_data = db_data(all_info)

        except:
            return {"error": "Invalid Credentials"}


    except:
        return {"error": f"[*] {str(sys.exc_info())}"}

    return fixed_db_data


def db_data(all_info):
    return_data = {}

    try:
        return_data['UserName'] = all_info['UserName']
    except KeyError:
        pass

    try:
        return_data['UserInfo'] = all_info['UserID']
    except KeyError:
        pass

    try:
        return_data['AmazonEC2RoleforRCEUsed'] = all_info['AmazonEC2RoleforRCEUsed']
    except KeyError:
        pass

    return return_data
