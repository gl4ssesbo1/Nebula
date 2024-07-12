from termcolor import colored
import os
import boto3
import botocore

def s3_enter_credentials(access_key_id, secret_key, region):
    endpoint = 'https://{}.digitaloceanspaces.com'.format(region)

    session = boto3.session.Session()
    return session.client('s3',
                          region_name=region,
                          endpoint_url=endpoint,
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_key
                          )

def s3_enter_credentials_with_user_agent(access_key_id, secret_key, region, ua):
    endpoint = 'https://{}.digitaloceanspaces.com'.format(region)
    session_config = botocore.config.Config(user_agent=ua)

    session = boto3.session.Session()
    return session.client('s3',
                          config=session_config,
                          region_name=region,
                          endpoint_url=endpoint,
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_key
                          )

def run_digitalocean_module(imported_module, all_sessions, cred_prof, useragent):
    service = imported_module.variables['SERVICE']['value']

    if imported_module.needs_creds:
        if cred_prof == "":
            return {"error": "{}{}{}{}{}".format(
                colored("[*] No credentials set. Use '", 'red'),
                colored("use credentials", "blue"),
                colored("' or '", "red"),
                colored("set credentials", "blue"),
                colored("' to continue", "red")
                )
            }

        else:
            if service == "SPACE":
                for session in all_sessions:
                    if session['profile'] == cred_prof:
                        if not useragent == "":
                            profile_v = s3_enter_credentials_with_user_agent(
                                                                          session['access_key_id'],
                                                                          session['secret_key'],
                                                                          session['region'],
                                                                          useragent
                                                                          )
                            return imported_module.exploit(profile_v)

                        else:
                            profile_v = s3_enter_credentials(
                                                          session['access_key_id'],
                                                          session['secret_key'],
                                                          session['region'],
                                                             )

                            return imported_module.exploit(profile_v)

            else:
                profile_v = {}
                for session in all_sessions:
                    if session['profile'] == cred_prof:
                        profile_v = session
                return imported_module.exploit(profile_v)

    else:
        return imported_module.exploit()
