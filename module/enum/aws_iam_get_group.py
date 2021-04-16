from termcolor import colored
import sys
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
    "GROUPS": {
        "value": "",
        "required": "false",
        "description":"The group to test. Can add one or more split by comma. If not added, all groups will be enumerated."
    }
}

description = "Enumerates information on a specific group."

aws_command = """
aws iam get-group --group-name <groupname> --region <region> --profile <profile>
aws iam get-account-authorization-details --region <region> --profile <profile> --query "Group['*']"
"""

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_group".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    outputfile = open(filename,'w')

    if not variables['GROUPS']['value'] == "":
        groups = (variables['GROUPS']['value']).split(",")
        try:
            iam_details = profile.get_account_authorization_details()
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(Marker=iam_details['Marker'])

            json.dump(iam_details['GroupDetailList'], outputfile, indent=4, default=str)

            for group in groups:
                for iam in iam_details['GroupDetailList']:
                    groupname = iam['GroupName']
                    if group == groupname:
                        print(colored("------------------------", "yellow", attrs=['bold']))
                        print("{}:\t{}".format(colored("IAM", "yellow", attrs=['bold']), groupname))
                        print(colored("------------------------", "yellow", attrs=['bold']))
                        for key, value in iam.items():
                            if key == "AttachedManagedPolicies":
                                print("\t{}".format(colored(key, "red", attrs=['bold'])))
                                for x in value:
                                    for a, b in x.items():
                                        print("\t\t{}:\t{}".format(colored(a, "green", attrs=['bold']), b))
                                    print()
                            else:
                                print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

                        print("\t{}".format(colored("Members:", "red", attrs=['bold'])))
                        members = profile.get_group(GroupName=groupname)['Users']
                        for user in members:
                            for key, value in user.items():
                                print("\t\t{}:\t{}".format(colored(key, "yellow", attrs=['bold']), value))
                            print()

        except:
            group_2 = []
            iam_details = profile.list_groups()['Groups']
            json.dump(iam_details['Groups'], outputfile, indent=4, default=str)

            for group in iam_details:
                if group['GroupName'] in groups:
                    group_2.append(group['GroupName'])

            for group in group_2:
                print(colored("----------------------------------", "yellow"))
                print("{}: {}".format(colored("GroupName", "yellow", attrs=['bold']), group))
                print(colored("----------------------------------", "yellow"))

                members = profile.get_group(GroupName=group)

                for key, value in (members['Group']).items():
                    print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
                print()

                print("\t{}:".format(colored("Members", "red", attrs=['bold'])))
                for user in members['Users']:
                    for key, value in user.items():
                        print("\t\t{}:\t{}".format(colored(key, "yellow", attrs=['bold']), value))
                    print()

        else:
            e = sys.exc_info()[0]
            print(colored("[*] {}".format(e), "red"))

    else:
        try:
            iam_details = profile.get_account_authorization_details()
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(Marker=iam_details['Marker'])

            json.dump(iam_details['GroupDetailList'], outputfile, indent=4, default=str)
            for iam in iam_details['GroupDetailList']:
                groupname = iam['GroupName']
                print(colored("------------------------", "yellow", attrs=['bold']))
                print("{}:\t{}".format(colored("IAM", "yellow", attrs=['bold']), groupname))
                print(colored("------------------------", "yellow", attrs=['bold']))
                for key, value in iam.items():
                    if key == "AttachedManagedPolicies":
                        print("\t{}".format(colored(key, "red", attrs=['bold'])))
                        for x in value:
                            for a, b in x.items():
                                print("\t\t{}:\t{}".format(colored(a, "green", attrs=['bold']), b))
                            print()
                    else:
                        print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

                print("\t{}".format(colored("Members:", "red", attrs=['bold'])))
                members = profile.get_group(GroupName=groupname)['Users']
                for user in members:
                    for key,value in user.items():
                        print("\t\t{}:\t{}".format(colored(key, "yellow", attrs=['bold']), value))
                    print()

        except:
            groups = []
            iam_details = profile.list_groups()['Groups']
            json.dump(iam_details, outputfile, indent=4, default=str)
            for group in iam_details:
                groups.append(group['GroupName'])

            for group in groups:
                print(colored("----------------------------------", "yellow"))
                print("{}: {}".format(colored("GroupName", "yellow", attrs=['bold']),group))
                print(colored("----------------------------------", "yellow"))

                members = profile.get_group(GroupName=group)

                for key, value in (members['Group']).items():
                    print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
                print()

                print("\t{}:".format(colored("Members", "red", attrs=['bold'])))
                for user in members['Users']:
                    for key, value in user.items():
                        print("\t\t{}:\t{}".format(colored(key, "yellow", attrs=['bold']), value))
                    print()

        else:
            e = sys.exc_info()[0]
            print(colored("[*] {}".format(e), "red"))

    outputfile.close()
    print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))