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
    }
}
description = "Delete access of a user to the Management Console"

aws_command = "aws iam delete-login-profile --user-name Bob --region <region> --profile <profile>"

def exploit(profile, workspace):
    try:
        user = variables['USERNAME']['value']
        profile.delete_login_profile(
            UserName=user
        )
        print(colored("User {} was successfully removed the Login Profile.".format(colored(user, "blue")), "green"))

    except profile.exceptions.EntityTemporarilyUnmodifiableException:
        print(colored("[*] This user cannot be modified.", "red"))
    except profile.exceptions.NoSuchEntityException:
        print(colored("[*] This user does not exist or has no Login Profile.", "red"))
    except profile.exceptions.LimitExceededException:
        print()