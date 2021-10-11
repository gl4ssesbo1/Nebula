from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

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
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "USERS": {
        "value": "",
        "required": "false",
        "description":"The user or users(split by comma) to check the login profile. If not added, all users will be listed."
    }
}

description = "Get info on the policy provided"

aws_command = "aws iam get-login-profile --user-name <user> --region <region> --profile <profile>"

def exploit(profile, workspace):
    dt_string = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_ec2_enum_elastic_ips".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    user_responses = []
    if not variables['USERS']['value'] == "":
        users = (variables['USERS']['value']).split(",")
        output = ""

        for user in users:
            try:
                response = profile.get_login_profile(
                    UserName=user
                )
                user_responses.append(response['LoginProfile'])
                output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                output += ("{}: {}\n".format(colored("UserName", "yellow", attrs=['bold']), user))
                output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                for key, value in (response['LoginProfile']).items():
                    output += (
                        "\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue", attrs=['bold'])))
                print(output)
                output = ""

            except profile.exceptions.NoSuchEntityException:
                output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                output += ("{}: {}\n".format(colored("UserName", "yellow", attrs=['bold']), user))
                output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                output += "{} {} {}\n".format(
                                            colored("[*] User", "yellow"),
                                            colored(user, "blue"),
                                            colored("has no login profile.", "yellow")
                                            )
                output += "\n"
                print(output)
                output = ""
    else:
        try:
            iam_details = profile.list_users()
            users = []
            output = ""
            while iam_details['IsTruncated']:
                iam_details = profile.list_users(Marker=iam_details['Marker'])

            for user in iam_details['Users']:
                users.append(user['UserName'])

            for user in users:
                try:
                    response = profile.get_login_profile(
                        UserName=user
                    )
                    user_responses.append(response['LoginProfile'])
                    output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                    output += ("\t{}: {}\n".format(colored("UserName", "yellow", attrs=['bold']), user))
                    output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                    for key, value in (response['LoginProfile']).items():
                        output += (
                            "{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue", attrs=['bold'])))
                    output += "\n"

                except profile.exceptions.NoSuchEntityException:
                    output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                    output += ("{}: {}\n".format(colored("UserName", "yellow", attrs=['bold']), user))
                    output += (colored("------------------------------------------------\n", "yellow", attrs=['bold']))
                    output += "{} {} {}\n".format(
                                                colored("[*] User","yellow"),
                                                colored(user,"blue"),
                                                colored("has no login profile.","yellow")
                                                )
                    output += "\n"

            pipepager(output, cmd='less -R')
            output = ""
        except:
            print(colored("[*] You have no rights to query all the users Login Profile.", "red"))

    with open(filename, 'w') as outputfile:
        json.dump(user_responses, outputfile, indent=4, default=str)
    print(colored("[*] User output is dumped on file '{}'.".format(filename), "yellow"))