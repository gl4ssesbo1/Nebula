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
    try:
        user = variables['USERNAME']['value']
        access_key = variables['ACCESS-KEY']['value']

        profile.delete_access_key(
            UserName=user,
            AccessKeyId=access_key
        )
        print(colored("Access Key {} of User {} was successfully deleted.".format(colored(user, "blue"), colored(access_key, "blue")), "green"))

    except profile.exceptions.NoSuchEntityException:
        print(colored("[*] This user does not exist or has no Login Profile.", "red"))
    except profile.exceptions.LimitExceededException:
        print("Limited thing")