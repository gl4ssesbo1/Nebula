import sys

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
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"USERNAME": {
        "value": "",
        "required": "true",
        "description": "The user to delete the access to the Management Console."
    }
}
description = "Delete access of a user to the Management Console"

aws_command = "aws iam delete-login-profile --user-name Bob --region <region> --profile <profile>"

def exploit(profile, workspace):
    user = variables['USERNAME']['value']

    try:
        profile.delete_login_profile(
            UserName=user
        )

        status = f"Successfully removed Login Profile for User {user}"

    except:
        status = f"Login Profile for User {user} was not removed with error code: {str(sys.exc_info()[1])}."

    return {
        "User": {
            "User": user,
            "Status": status
        }
    }