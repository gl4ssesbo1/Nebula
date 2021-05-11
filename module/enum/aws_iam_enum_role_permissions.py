from termcolor import colored
from datetime import datetime
import json

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE":{
		"value":"iam",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "ROLENAME":{
		"value":"",
		"required":"false",
        "description":"The name of the Role to test."
	}
}

description = "Get info on the policy provided"

aws_command = """
aws iam get-account-authorization-details --region <region> --profile <profile> --query "RoleDetailList[*]"
aws iam get-account-authorization-details --filters Name=rolename,Values=<rolename> --query "RoleDetailList[*]" --region <region> --profile <profile>
"""

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_enum_role_permissions".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    outputfile = open(filename,'w')

    if variables['ROLENAME']['value'] == "":
        try:
            iam_details = profile.get_account_authorization_details()
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(
                    Marker=iam_details['Marker']
                )

            get_role_details(iam_details)
            
            json.dump(iam_details['RoleDetailList'], outputfile, indent=4, default=str)

        except:
            response = profile.get_role(
                RoleName=variables['ROLENAME']['value']
            )
            get_role_func(response)
            
            json.dump(response, outputfile, indent=4, default=str)

    else:
        try:
            iam_details = profile.get_account_authorization_details()
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(
                    Marker=iam_details['Marker']
                )
            for iam_d in iam_details['RoleDetailList']:
                if iam_d['RoleName'] == variables['ROLENAME']['value']:
                    get_role_details(iam_d)

            json.dump(iam_details['RoleDetailList'], outputfile, indent=4, default=str)

        except:
            iam_details = profile.list_roles()

            while iam_details['IsTruncated']:
                iam_details = profile.list_groups(Marker=iam_details['Marker'])

            roles = []
            for iam_d in iam_details["Roles"]:
                roles.append(iam_d['RoleName'])
            
            json.dump(roles, outputfile, indent=4, default=str)

            for role in roles:
                response = profile.get_role(
                    RoleName=role
                )
                get_role_func(response)

    outputfile.close()
    print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

def get_role_func(role):
    print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))
    print("{}: {}".format(colored("Role", "yellow", attrs=['bold']), role['Role']['RoleName']))
    print("{}".format(colored("-----------------------------", "yellow", attrs=['bold'])))

    for key, value in (role['Role']).items():
        if key == 'AssumeRolePolicyDocument':
            print("\t{}:".format(colored(key, "red", attrs=['bold'])))
            for a, b in value.items():
                if a == 'Statement':
                    print("\t\t{}:".format(colored(a, "green", attrs=['bold'])))
                    for l in b:
                        print("\t\t\t{}:\t{}".format(colored("Effect", "yellow", attrs=['bold']), l['Effect']))
                        print("\t\t\t{}:".format(colored("Principal", "yellow", attrs=['bold'])))
                        for k, v in (l['Principal']).items():
                            print("\t\t\t\t{}:\t{}".format(colored(k, "magenta", attrs=['bold']), v))
                        print("\t\t\t{}:\t{}".format(colored("Action", "yellow", attrs=['bold']), l['Action']))
        else:
            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

def get_role_details(response):
    print(colored("------------------------------------------------", "yellow", attrs=['bold']))
    print("{}: {}".format(colored("RoleName", "yellow", attrs=['bold']), response['RoleName']))
    print(colored("------------------------------------------------", "yellow", attrs=['bold']))
    for key, value in response.items():
        if key == 'AssumeRolePolicyDocument':
            print("\t{}:".format(colored(key, "red", attrs=['bold'])))
            print("\t\t{}:\t{}".format(colored("Version", "green", attrs=['bold']), value['Version']))
            print("\t\t{}:".format(colored("Statement", "green", attrs=['bold'])))
            for statement in value['Statement']:
                print("\t\t\t{}:\t{}".format(colored("Effect", "yellow", attrs=['bold']),
                                             statement['Effect']))
                print("\t\t\t{}:".format(colored("Principal", "yellow", attrs=['bold'])))
                for k, v in (statement['Principal']).items():
                    print("\t\t\t\t{}:\t{}".format(colored(k, "magenta", attrs=['bold']), v))

                print("\t\t\t{}:\t{}".format(colored("Action", "yellow", attrs=['bold']),
                                             statement['Action']))

        elif key == 'AttachedManagedPolicies':
            print("\t{}:".format(colored(key, "red", attrs=['bold'])))
            for policy in value:
                print("\t\t{}:\t{}".format(colored("PolicyName", "yellow", attrs=['bold']),
                                           policy['PolicyName']))
                print("\t\t{}:\t{}".format(colored("PolicyArn", "yellow", attrs=['bold']),
                                           policy['PolicyArn']))
                print()

        elif key == 'InstanceProfileList':
            print("\t{}:".format(colored(key, "red", attrs=['bold'])))
            for iam_d in value:
                print("\t\t{}: {}".format(colored("InstanceProfileName", "yellow", attrs=['bold']),
                                          iam_d['InstanceProfileName']))
            print()

        else:
            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))