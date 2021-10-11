from termcolor import colored
import os
import boto3, botocore

def enter_credentials(service, access_key_id, secret_key, region):
    return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

def enter_credentials_with_session_token(service, access_key_id, secret_key, region, session_token):
    return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key, aws_session_token=session_token)

def enter_credentials_with_session_token_and_user_agent(service, access_key_id, secret_key, region, session_token, ua):
    session_config = botocore.config.Config(user_agent=ua)
    return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key, aws_session_token=session_token, config=session_config)

def enter_credentials_with_user_agent(service, access_key_id, secret_key, region, ua):
    session_config = botocore.config.Config(user_agent=ua)
    return boto3.client(service, config=session_config, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

def enter_session(session_name, region, service):
    boto_session = boto3.session.Session(profile_name=session_name, region_name=region)
    return boto_session.client(service)

def run_aws_module(imported_module, all_sessions, cred_prof, workspace, useragent):
    service = imported_module.variables['SERVICE']['value']
    if imported_module.needs_creds:
        c = 0
        if cred_prof == "":
            print("{}{}{}{}".format(
                colored("[*] No credentials set. Use '", 'red'),
                colored("set aws-credentials", "blue"),
                colored("' or '", "red"),
                colored("set azure-credentials", "blue"),
                colored("' to set credentials.", "red")
            ))
            c = 1
        else:
            for sess in all_sessions:
                if sess['profile'] == cred_prof:
                    for key, value in sess.items():
                        if key == 'session_token':
                            continue
                        elif key == 'region' and value == "":
                            print("{}{}{}".format(
                                colored("[*] No region set. Use '", 'red'),
                                colored("set region <region>", "blue"),
                                colored("' to set a region.", "red")
                            ))
                            c = 1
                        elif value == "":
                            print("{}{}{}".format(
                                colored("[*] '", 'red'),
                                colored("", "blue"),
                                colored("' not set. Check credentials.", "red")
                            ))
                            c = 1

        if c == 0:
            env_aws = {}

            if os.environ.get('AWS_ACCESS_KEY'):
                env_aws['AWS_ACCESS_KEY'] = os.environ.get('AWS_ACCESS_KEY')
                del os.environ['AWS_ACCESS_KEY']
            os.environ['AWS_ACCESS_KEY'] = sess['access_key_id']

            if os.environ.get('AWS_SECRET_KEY'):
                env_aws['AWS_SECRET_KEY'] = os.environ.get('AWS_SECRET_KEY')
                del os.environ['AWS_SECRET_KEY']
            os.environ['AWS_SECRET_KEY'] = sess['secret_key']

            if 'session_token' in sess and sess['session_token'] != "":
                if os.environ.get('AWS_SESSION_TOKEN'):
                    env_aws['AWS_SESSION_TOKEN'] = os.environ.get('AWS_SESSION_TOKEN')
                    del os.environ['AWS_SESSION_TOKEN']
                os.environ['AWS_SESSION_TOKEN'] = sess['session_token']

            if os.environ.get('AWS_REGION'):
                env_aws['AWS_REGION'] = os.environ.get('AWS_REGION')
                del os.environ['AWS_REGION']
            os.environ['AWS_REGION'] = sess['region']

            if not 'session_token' in sess:
                if not useragent == "":
                    profile_v = enter_credentials_with_user_agent(service,
                                                                  sess['access_key_id'],
                                                                  sess['secret_key'],
                                                                  sess['region'],
                                                                  useragent
                                                                  )
                    imported_module.exploit(profile_v, workspace)

                else:
                    profile_v = enter_credentials(service,
                                                  sess['access_key_id'],
                                                  sess['secret_key'],
                                                  sess['region']
                                                  )
                    imported_module.exploit(profile_v, workspace)
            elif 'session_token' in sess and sess['session_token'] != "":
                if not useragent == "":
                    profile_v = enter_credentials_with_session_token(service,
                                                            sess['access_key_id'],
                                                            sess['secret_key'],
                                                            sess['region'],
                                                            sess['session_token']
                                                            )
                    imported_module.exploit(profile_v, workspace)
                else:
                    profile_v = enter_credentials_with_session_token_and_user_agent(service,
                                                                  sess['access_key_id'],
                                                                  sess['secret_key'],
                                                                  sess['region'],
                                                                  sess['session_token'],
                                                                  useragent)
                    imported_module.exploit(profile_v, workspace)
            else:
                print(colored("[*] Check if the session key is empty.","yellow"))
            del os.environ['AWS_ACCESS_KEY']
            del os.environ['AWS_SECRET_KEY']
            del os.environ['AWS_REGION']
            if os.environ.get('AWS_SESSION_TOKEN'):
                del os.environ['AWS_SESSION_TOKEN']

            if env_aws:
                os.environ['AWS_ACCESS_KEY'] = env_aws['AWS_ACCESS_KEY']
                os.environ['AWS_SECRET_KEY'] = env_aws['AWS_SECRET_KEY']
                os.environ['AWS_REGION'] = env_aws['AWS_REGION']
                os.environ['AWS_SESSION_TOKEN'] = env_aws['AWS_SESSION_TOKEN']
    else:
        imported_module.exploit(workspace)