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
    "USERS":{
		"value":"",
		"required":"false",
        "description":"The service that will be used to run the module. It cannot be changed."
	}
}

description = "Get info about the current user or specific Users like the Username, ID, ARN, Creation Date, Attached Policies, GroupList and Tags. The IAM whose credentials are provided should have IAMReadOnlyAccess or IAMFullAccess. If the user field is empty, all users' details will be shown. Or you can provide a single user or a group of user separated by comma (',')"

aws_command = "aws iam get-account-authorization-details --query 'UserDetailList[*]' --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_get_user_details".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    user_list = []
    try:
        if not variables['USERS']['value'] == "":
            users = (variables['USERS']['value']).split(",")

            iam_details = profile.get_account_authorization_details(Filter=['User'])
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(Filter=['User'], Marker=iam_details['Marker'])

            for iam in iam_details['UserDetailList']:
                for user in users:
                    if iam['UserName'] == user:
                        user_list.append(iam)

            for iam in user_list:
                print(colored("------------------------", "yellow", attrs=['bold']))
                print("{}:\t{}".format(colored("UserName", "yellow", attrs=['bold']), iam['UserName']))
                print(colored("------------------------", "yellow", attrs=['bold']))
                for key,value in iam.items():
                    if key == "AttachedManagedPolicies":
                        if iam['AttachedManagedPolicies']:
                            print("\t{}:".format(colored(key, "red", attrs=['bold'])))
                            for x in value:
                                for a,b in x.items():
                                    print("\t\t{}:{}".format(colored(a, "green", attrs=['bold']), b))
                                print()
                        else:
                            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored("[]", "blue")))

                    else:
                        print("\t{}:{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))
            
            with open(filename,'w') as outputfile:
                json.dump(user_list, outputfile, indent=4, default=str)

            outputfile.close()
            print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))



        else:
            iam_details = profile.get_account_authorization_details()
            while iam_details['IsTruncated']:
                iam_details = profile.get_account_authorization_details(Marker=iam_details['Marker'])

            for iam in iam_details['UserDetailList']:
                print(colored("------------------------", "yellow", attrs=['bold']))
                print("{}:\t{}".format(colored("IAM", "yellow", attrs=['bold']), iam['UserName']))
                print(colored("------------------------", "yellow", attrs=['bold']))
                for key, value in iam.items():
                    if key == "AttachedManagedPolicies":
                        if iam['AttachedManagedPolicies']:
                            print("\t{}".format(colored(key, "red", attrs=['bold'])))
                            for x in value:
                                for a, b in x.items():
                                    print("\t\t{}:\t{}".format(colored(a, "green", attrs=['bold']), b))
                                print()
                        else:
                            print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored("[]", "blue")))

                    else:
                        print("\t{}:\t{}".format(colored(key, "red", attrs=['bold']), colored(value, "blue")))

            with open(filename,'w') as outputfile:
                json.dump(iam_details, outputfile, indent=4, default=str)

            outputfile.close()
            print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

    except:
            print(colored("[*] IAM Provided does not have enough privileges to enumerate itself or other IAM objects.", "red"))