import boto3
import botocore
from datetime import datetime
import json
from termcolor import colored
import sys

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""


def list_dictionary(d, n_tab):
    global output
    if isinstance(d, list):
        n_tab += 1
        for i in d:
            if not isinstance(i, list) and not isinstance(i, dict):
                output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
            else:
                list_dictionary(i, n_tab)
    elif isinstance(d, dict):
        n_tab += 1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold']),
                                               colored(value, colors[n_tab + 1])))
            else:
                output += ("{}{}:\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)


def getuid(profile_dict, workspace):
    global output
    n_tab = 0
    region = profile_dict['region']
    access_key_id = profile_dict['access_key_id']
    secret_key = profile_dict['secret_key']
    session_token = ""

    if "session_token" in profile_dict:
        session_token = profile_dict['session_token']

    if region == "":
        print("{}{}{}".format(
            colored("[*] No region set. Use '", 'red'),
            colored("set region <region>", "blue"),
            colored("' to set a region.", "red")
        ))

    else:
        username = ""
        policies = []

        all_info = {}

        try:
            if "session_token" in profile_dict:
                client = boto3.client(
                    "sts",
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_key
                )
            else:
                client = boto3.client(
                    "sts",
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token
                )

            response = client.get_caller_identity()
            del response['ResponseMetadata']
            all_info['UserID'] = response
            username = (response['Arn']).split("/")[-1]

            print(colored("------------------------------------------------", "yellow", attrs=['bold']))
            print("{}: {}".format(colored("UserId", "yellow", attrs=['bold']),
                                  colored(response['UserId'], "white")))
            print(colored("------------------------------------------------", "yellow", attrs=['bold']))

            print("\t{}: {}".format(colored("UserID", "red", attrs=['bold']),
                                    colored(response['UserId'], "blue")))
            print("\t{}: {}".format(colored("Arn", "red", attrs=['bold']),
                                    colored(response['Arn'], "blue")))
            print("\t{}: {}".format(colored("Account", "red", attrs=['bold']),
                                    colored(response['Account'], "blue")))

            if "session_token" in profile_dict:
                client = boto3.client(
                    "iam",
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_key
                )
            else:
                client = boto3.client(
                    "iam",
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_key,
                    aws_session_token = session_token
                )

            if not username == "":
                response = client.get_user(
                    UserName=username
                )
                del response['ResponseMetadata']

                all_info['UserInfo'] = response

                title_name = "User"
                json_data = response[title_name]
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                output += colored("{}: {}\n".format("User", username), "yellow", attrs=['bold'])
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                list_dictionary(json_data, n_tab)
                output += "\n"
                print(output)
                output = ""

                response = client.list_attached_user_policies(
                    UserName=username
                )

                while response['IsTruncated']:
                    response.update(client.list_attached_user_policies(
                        UserName=username,
                        Marker=response['Marker']
                    ))

                if response['ResponseMetadata']:
                    del response['ResponseMetadata']

                all_info['AttachedPolicies'] = response['AttachedPolicies']

                title_name = "AttachedPolicies"

                if len(response[title_name]) > 0:
                    for pol in (response[title_name]):
                        policies.append(pol['PolicyArn'])

                    if isinstance(response[title_name], list):
                        for json_data in response['AttachedPolicies']:
                            output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                            output += colored("\t{}: \n".format(title_name), "blue", attrs=['bold'])
                            output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                            list_dictionary(json_data, n_tab)
                            output += "\n"
                            print(output)
                            output = ""

                    elif isinstance(response[title_name], dict):
                        json_data = response['AttachedPolicies']
                        output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                        output += colored("\t{}:\n".format(title_name), "blue", attrs=['bold'])
                        output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                        list_dictionary(json_data, n_tab)
                        output += "\n"
                        print(output)
                        output = ""
                else:
                    print(colored("[*] No attached policies to the user. ","green"))

            groups_for_users = client.list_groups_for_user(
                UserName=username
            )
            groups_json_data = groups_for_users['Groups']
            while groups_for_users['IsTruncated']:
                groups_for_users = client.list_groups_for_user(
                    UserName=username,
                    Marker=groups_for_users['Marker']
                )
                groups_json_data.extend(groups_for_users['Groups'])

            groups = []
            output = ""

            if len(groups_json_data) > 0:
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                output += colored("Groups: \n", "yellow", attrs=['bold'])
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                for group in (groups_json_data):
                    groups.append(group['GroupName'])

                    output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                    output += colored("\tGroupName: {}\n".format(group['GroupName']), "blue", attrs=['bold'])
                    output += colored("\t---------------------------------\n", "blue", attrs=['bold'])
                    list_dictionary(group, n_tab)
                    output += "\n"

                print(output)
                output = ""
                del group

            group_policies = {}
            if len(groups) > 0:
                for group in groups:
                    group_response = client.list_group_policies(
                        GroupName=group
                    )
                    group_policies[group] = {
                        'InlinePolicies':[]
                    }

                    group_policies[group]['InlinePolicies'] = group_response['PolicyNames']

                    while group_response['IsTruncated']:
                        group_response = client.list_group_policies(
                            GroupName=group,
                            Marker=groups_for_users['Marker']
                        )
                        (group_policies[group]['InlinePolicies']).extend(group_response['PolicyNames'])

                    del group_response

                    group_response = client.list_attached_group_policies(
                        GroupName=group
                    )
                    group_policies[group] = {
                        'AttachedPolicies': {}
                    }
                    group_policies[group]['AttachedPolicies'] = group_response['AttachedPolicies']
                    while group_response['IsTruncated']:
                        group_response = client.list_attached_group_policies(
                            GroupName=group,
                            Marker=groups_for_users['Marker']
                        )
                        (group_policies[group]['AttachedPolicies']).extend(group_response['AttachedPolicies'])

                    for pol in group_policies[group]['AttachedPolicies']:
                        policies.append(pol['PolicyArn'])

                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                    output += colored("Group: {}\n".format(group), "yellow", attrs=['bold'])
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                    list_dictionary(group_policies[group], n_tab)
                    output += "\n"
                    print(output)
                    output = ""

            if len(policies) > 0:
                pol_output = []
                for pol in policies:
                    response = client.get_policy(
                        PolicyArn=pol
                    )
                    if response['ResponseMetadata']:
                        del response['ResponseMetadata']
                    pol_output.append(response)

                if len(pol_output) > 0:
                    for json_data in pol_output:
                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                        output += colored("{}: {}\n".format("Policy", json_data["Policy"]['PolicyName']), "yellow", attrs=['bold'])
                        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                        list_dictionary(json_data, n_tab)
                        output += "\n"
                        print(output)
                        output = ""

            all_info['Policies'] = pol_output

        except:
            e = sys.exc_info()
            print(colored("[*] {}".format(e), "red"))

        if not username == "":
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            file = "{}_getuid_{}".format(dt_string, username)
            filename = "./workspaces/{}/{}".format(workspace, file)

            with open(filename, 'w') as dump_file:
                json.dump(all_info, dump_file, indent=4, default=str)
                dump_file.close()

            print(colored("[*] Output is saved to '{}'".format(filename), "green"))
