import base64
import random

from termcolor import colored
import os
import boto3, botocore


def enter_credentials(service, access_key_id, secret_key, region, ua, proxy_definitions):
    args = {
        "service_name": service,
        "region_name": region,
        "aws_access_key_id": access_key_id,
        "aws_secret_access_key": secret_key
    }

    session_config_args = {}

    if not len(proxy_definitions) == 0:
        web_proxy = random.choice(proxy_definitions)

        for key, value in web_proxy.items():
            proxy_config = {
                # "http": key.split('//')[1],
                key.split('//')[0]: key.split('//')[1]
                # key.split("//")[0]: key.split('//')[1]
            }

            with open("/tmp/cert.pem", 'w') as certfile:
                certfile.write(base64.b64decode(value.encode()).decode())

            proxy_configurations = {
                'proxy_client_cert': "/tmp/cert.pem"
            }
            session_config_args["proxies"] = proxy_config
            session_config_args["proxies_config"] = proxy_configurations
            # session_config_args["proxies"] = proxy_definitions

    if not ua == "":
        session_config_args["user_agent"] = ua

    if not session_config_args == {}:
        session_config = botocore.config.Config(**session_config_args)
        args["config"] = session_config

    return boto3.client(**args)


def enter_credentials_with_session_token(service, access_key_id, secret_key, region, session_token, ua,
                                         proxy_definitions):
    args = {
        "service_name": service,
        "region_name": region,
        "aws_access_key_id": access_key_id,
        "aws_secret_access_key": secret_key,
        "aws_session_token": session_token
    }

    session_config_args = {}

    if not len(proxy_definitions) == 0:
        web_proxy = random.choice(proxy_definitions)

        session_config_args["proxies"] = {
            web_proxy.split(":")[0]: web_proxy
        }
        # session_config_args["proxies"] = proxy_definitions

    if not ua == "":
        session_config_args["user_agent"] = ua

    if not session_config_args == {}:
        session_config = botocore.config.Config(**session_config_args)
        args["config"] = session_config

    return boto3.client(**args)


def enter_session(session_name, region, service, ua, proxy_definitions):
    boto_session = boto3.session.Session(profile_name=session_name, region_name=region)
    args = {
        "service_name": service,
    }

    session_config_args = {}

    if not len(proxy_definitions) == 0:
        web_proxy = random.choice(proxy_definitions)

        session_config_args["proxies"] = {
            web_proxy.split(":")[0]: web_proxy
        }

    if not ua == "":
        session_config_args["user_agent"] = ua

    if not session_config_args == {}:
        session_config = botocore.config.Config(**session_config_args)
        args["config"] = session_config

    return boto_session.client(**args)


def giveMeClient(all_sessions, cred_prof, useragent, web_proxies, service):
    sess = {}
    # proxy_definitions = {}

    # if not web_proxies == []:
    #    for proxy in web_proxies:
    #        proxy_definitions[proxy.split(":")[0]] = proxy
    # else:
    #    proxy_definitions = None

    proxy_definitions = web_proxies

    c = 0
    if cred_prof == "":
        return {"error": ("{}{}{}{}".format(
            colored("[*] No credentials set. Use '", 'red'),
            colored("set aws-credentials", "blue"),
            colored("' or '", "red"),
            colored("set azure-credentials", "blue"),
            colored("' to set credentials.", "red")
        ))}
        c = 1
    else:
        for session in all_sessions:
            if session['profile'] == cred_prof:
                sess = session
                break

        for key, value in sess.items():
            if key == 'session_token':
                continue
            elif key == 'region' and value == "":
                return {"error": ("{}{}{}".format(
                    colored("[*] No region set. Use '", 'red'),
                    colored("set region <region>", "blue"),
                    colored("' to set a region.", "red")
                ))}
                c = 1
            elif value == "":
                return {"error": ("{}{}{}".format(
                    colored("[*] '", 'red'),
                    colored("", "blue"),
                    colored("' not set. Check credentials.", "red")
                ))}
                c = 1

        if c == 0:
            """            env_aws = {}
            if os.environ.get('AWS_ACCESS_KEY'):
                env_aws['AWS_ACCESS_KEY'] = os.environ.get('AWS_ACCESS_KEY')
                del os.environ['AWS_ACCESS_KEY']
            os.environ['AWS_ACCESS_KEY'] = sess['access_key_id']

            if os.environ.get('AWS_SECRET_KEY'):
                env_aws['AWS_SECRET_KEY'] = os.environ.get('AWS_SECRET_KEY')
                del os.environ['AWS_SECRET_KEY']
            os.environ['AWS_SECRET_KEY'] = sess['secret_key']

            if os.environ.get('AWS_SESSION_TOKEN'):
                if 'session_token' in sess and sess['session_token'] != "":
                    env_aws['AWS_SESSION_TOKEN'] = os.environ.get('AWS_SESSION_TOKEN')
                    del os.environ['AWS_SESSION_TOKEN']
                os.environ['AWS_SESSION_TOKEN'] = sess['session_token']

            if os.environ.get('AWS_REGION'):
                env_aws['AWS_REGION'] = os.environ.get('AWS_REGION')
                del os.environ['AWS_REGION']
            os.environ['AWS_REGION'] = sess['region']"""

            if not 'session_token' in sess:
                profile = enter_credentials(service,
                                            sess['access_key_id'],
                                            sess['secret_key'],
                                            sess['region'],
                                            useragent,
                                            proxy_definitions
                                            )
                """                del os.environ['AWS_ACCESS_KEY']
                del os.environ['AWS_SECRET_KEY']
                del os.environ['AWS_REGION']
                if os.environ.get('AWS_SESSION_TOKEN'):
                    del os.environ['AWS_SESSION_TOKEN']

                if env_aws:
                    os.environ['AWS_ACCESS_KEY'] = env_aws['AWS_ACCESS_KEY']
                    os.environ['AWS_SECRET_KEY'] = env_aws['AWS_SECRET_KEY']
                    os.environ['AWS_REGION'] = env_aws['AWS_REGION']
                    if 'AWS_SESSION_TOKEN' in env_aws:
                        os.environ['AWS_SESSION_TOKEN'] = env_aws['AWS_SESSION_TOKEN']"""

                #del env_aws
                return profile

            elif 'session_token' in sess and sess['session_token'] != "":

                profile = enter_credentials_with_session_token(service,
                                                            sess['access_key_id'],
                                                            sess['secret_key'],
                                                            sess['region'],
                                                            sess['session_token'],
                                                            useragent,
                                                            proxy_definitions
                                                            )
                """del os.environ['AWS_ACCESS_KEY']
                del os.environ['AWS_SECRET_KEY']
                del os.environ['AWS_REGION']
                if os.environ.get('AWS_SESSION_TOKEN'):
                    del os.environ['AWS_SESSION_TOKEN']

                if env_aws:
                    os.environ['AWS_ACCESS_KEY'] = env_aws['AWS_ACCESS_KEY']
                    os.environ['AWS_SECRET_KEY'] = env_aws['AWS_SECRET_KEY']
                    os.environ['AWS_REGION'] = env_aws['AWS_REGION']
                    if 'AWS_SESSION_TOKEN' in env_aws:
                        os.environ['AWS_SESSION_TOKEN'] = env_aws['AWS_SESSION_TOKEN']

                del env_aws"""

                return profile
            else:
                return {"error": (colored("[*] Check if the session key is empty.", "yellow"))}
