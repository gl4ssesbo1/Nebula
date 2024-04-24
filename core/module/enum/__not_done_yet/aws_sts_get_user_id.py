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
        "value":"sts",
        "required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
    }
}

description = "Get the ID of the current User. Just provide IAM Credentials and run. No extra permissions are needed"

aws_command = "aws ec2 describe-instances --region {} --profile {}"

def exploit(profile, workspace):
    response = profile.get_caller_identity()

    print(colored("------------------------------------------------", "yellow", attrs=['bold']))
    print("{}: {}".format(colored("UserId", "yellow", attrs=['bold']), colored(response['UserId'], "white")))
    print(colored("------------------------------------------------", "yellow", attrs=['bold']))

    print("\t{}: {}".format(colored("UserID", "red", attrs=['bold']), colored(response['UserId'], "blue")))
    print("\t{}: {}".format(colored("Arn", "red", attrs=['bold']), colored(response['Arn'], "blue")))
    print("\t{}: {}".format(colored("Account", "red", attrs=['bold']), colored(response['Account'], "blue")))
    print(colored("------------------------------------------------", "yellow", attrs=['bold']))
