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
                        '''
                        env_aws = {}
                        if os.environ.get('AWS_ACCESS_KEY'):
                            env_aws['AWS_ACCESS_KEY'] = os.environ.get('AWS_ACCESS_KEY')
                            del os.environ['AWS_ACCESS_KEY']
                        os.environ['AWS_ACCESS_KEY'] = sess['access_key_id']
        
                        if os.environ.get('AWS_SECRET_KEY'):
                            env_aws['AWS_SECRET_KEY'] = os.environ.get('AWS_SECRET_KEY')
                            del os.environ['AWS_SECRET_KEY']
                        os.environ['AWS_SECRET_KEY'] = sess['secret_key']
        
                        if os.environ.get('AWS_REGION'):
                            env_aws['AWS_REGION'] = os.environ.get('AWS_REGION')
                            del os.environ['AWS_REGION']
                        os.environ['AWS_REGION'] = sess['region']
                        '''
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

                        '''
                        del os.environ['AWS_ACCESS_KEY']
                        del os.environ['AWS_SECRET_KEY']
                        del os.environ['AWS_REGION']
        
                        if env_aws:
                            os.environ['AWS_ACCESS_KEY'] = env_aws['AWS_ACCESS_KEY']
                            os.environ['AWS_SECRET_KEY'] = env_aws['AWS_SECRET_KEY']
                            os.environ['AWS_REGION'] = env_aws['AWS_REGION']
        
                        del env_aws
                        '''
            else:
                profile_v = {}
                for session in all_sessions:
                    if session['profile'] == cred_prof:
                        profile_v = session
                imported_module.exploit(profile_v)

    else:
        return imported_module.exploit()
