from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "iam",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "USERNAME": {
        "value": "",
        "required": "false",
        "description": "The user to allow access to the Management Console. Either use this ot"
    },
    "USER-FILE": {
        "value": "",
        "required": "false",
        "description": "The file of all the users to allow access to the Management Console."
    },
    "PASSWORD": {
        "value": "",
        "required": "true",
        "description": "The password to give to the user. The password needs to be compatible with the password policy configured. Use enum/aws_iam_get_account_password_policy to check it."
    },
    "PASSWORD-RESET-NEEDED": {
        "value": "false",
        "required": "true",
        "description": "If you want to, and I don't know why, you can make the account needing to reset the password at login."
    }
}
description = "If an IAM user is not allowed to access the Management Console, you can allow it using a password you want."

aws_command = "aws iam create-login-profile --user-name <user> --password <password> <--password-reset-required OR --no-password-reset-required> --region <region> --profile <profile>"

def set_login_profile(profile, workspace, username, password, pass_reset):
    try:
        response = profile.create_login_profile(
            UserName=username,
            Password=password,
            PasswordResetRequired=pass_reset
        )

        json_data = response['LoginProfile']
        json_data['Password'] = password

        return json_data

    except profile.exceptions.EntityAlreadyExistsException:
        print(colored("[*] This user allready can login to the Management Console.", "red"))

    except profile.exceptions.NoSuchEntityException:
        print(colored("[*] This user does not exist.", "red"))

    except profile.exceptions.PasswordPolicyViolationException:
        print(colored("[*] The password does not comply with the password policy.", "red"))

    except profile.exceptions.LimitExceededException:
        print()


colors = [
    "not-used",
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
        n_tab+=1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
            else:
                output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)

def exploit(profile, workspace):
    n_tab = 0
    global output
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_create_user_login_profile".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    username = variables['USERNAME']['value']
    userfile = variables["USER-FILE"]['value']
    password = variables['PASSWORD']['value']

    if variables['PASSWORD-RESET-NEEDED']['value'] == 'true':
        pass_reset = True
    else:
        pass_reset = False

    if username == "" and userfile == "":
        print(colored("[*] At least include USERNAME or USER-FILE.", "red"))

    elif not username == "" and not userfile == "":
        print(colored("[*] At least include USERNAME or USER-FILE.", "red"))

    elif userfile == "" and not username == "":
        json_data = {}
        json_data.append(set_login_profile(profile, workspace, username, password, pass_reset))

    elif not userfile == "" and username == "":
        json_data = []
        ufile = open(userfile, 'r')
        for user in ufile.readlines():
            response = set_login_profile(profile, workspace, user.strip().replace("\n", ""), password, pass_reset)
            json_data.append(response)

    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
    for data in json_data:
        output += colored("UserName: {}\n".format(data['UserName']), "yellow", attrs=['bold'])
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        list_dictionary(data, n_tab)
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])

    pipepager(output, cmd='less -R')
    output = ""