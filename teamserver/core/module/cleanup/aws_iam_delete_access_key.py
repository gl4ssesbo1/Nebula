import sys

from termcolor import colored

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
    },
	"ACCESS-KEY": {
        "value": "",
        "required": "true",
        "description": "The user to delete the access to the Management Console."
    }
}
description = "Delete access key of a user by providing it."

aws_command = "aws iam delete-access-key --access-key-id <access key> --user-name <user> --region <region> --profile <profile>"

def exploit(profile, workspace):
    user = variables['USERNAME']['value']
    access_key = variables['ACCESS-KEY']['value']

    try:
        profile.delete_access_key(
            UserName=user,
            AccessKeyId=access_key
        )

        status = f"Access Key {access_key} of User {user} was successfully deleted."

    except Exception as e:
        status = f"Access Key {access_key} of User {user} was not deleted with error code: {str(e)}."

    return {
        "User": {
            "User": user,
            "AccessKey": access_key,
            "Status": status
        }
    }