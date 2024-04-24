from termcolor import colored
import sys
import json

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
    "POLICYARN": {
        "value": "",
        "required": "true",
        "description":"The arn of the Policy to enumerate."
    }
}

description = "Get info on the policy provided"

aws_command = "aws iam list-entities-for-policy --policy-arn <policy arn> --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_list_entities_for_policy".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    response = profile.list_entities_for_policy(
        PolicyArn=variables['POLICYARN']['value'],
    )

    while response['IsTruncated']:
        response = profile.list_attached_user_policies(
            Marker=response['Marker']
        )
    
    with open(filename,'w') as outputfile:
        json.dump(response, outputfile, indent=4, default=str)

    outputfile.close()
    print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))


    policyname = (variables['POLICYARN']['value']).split("/")[1]
    print(colored("-----------------------------------", "yellow", attrs=['bold']))
    print("{}: {}".format(colored("Policy", "yellow", attrs=['bold']), policyname))
    print(colored("-----------------------------------", "yellow", attrs=['bold']))

    print(colored("\t-----------", "yellow", attrs=['bold']))
    print("\t{}:".format(colored("Groups", "yellow", attrs=['bold'])))
    print(colored("\t-----------", "yellow", attrs=['bold']))
    for group in response['PolicyGroups']:
        for key, value in group.items():
            print("\t\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
        print()

    print(colored("\t-----------", "yellow", attrs=['bold']))
    print("\t{}:".format(colored("Users", "yellow", attrs=['bold'])))
    print(colored("\t-----------", "yellow", attrs=['bold']))
    for users in response['PolicyUsers']:
        for key, value in users.items():
            print("\t\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
        print()

    print(colored("\t-----------", "yellow", attrs=['bold']))
    print("\t{}:".format(colored("Roles", "yellow", attrs=['bold'])))
    print(colored("\t-----------", "yellow", attrs=['bold']))
    for roles in response['PolicyRoles']:
        for key, value in roles.items():
            print("\t\t{}: {}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
        print()