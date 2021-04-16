import json
from termcolor import colored
from datetime import datetime
from pydoc import pipepager

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
        "description": "The service that will be used to run the module. It cannot be changed."
	}
}

description = "Enumerates the permissions of all users, groups, policies, roles or just any of them if required. The IAM whose credentials are provided needs to have IAMReadOnlyAccess, IAMFullAccess, or have permissions: "

aws_command = "aws iam get-account-authorization-details --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_iam_enum_all".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    iam = {}

    try:
        iam_details = profile.get_account_authorization_details()
        while iam_details['IsTruncated']:
            iam_details = profile.get_account_authorization_details(
                Marker=iam_details['Marker']
            )
        iam['UserDetailList'] = iam_details['UserDetailList']
        iam['GroupDetailList'] = iam_details['GroupDetailList']
        iam['RoleDetailList'] = iam_details['RoleDetailList']

        pol_dict = []
        for x in iam_details['Policies']:
            default_version = x['DefaultVersionId']
            for k in x['PolicyVersionList']:
                if k['VersionId'] == default_version:
                    pol_dict.append(k)
        iam['Policies'] = pol_dict
        with open(filename,'w') as outputfile:
            json.dump(iam, outputfile, indent=4, default=str)

        outputfile.close()
        print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"), colored(".", "green"))

        users = iam['UserDetailList']
        groups = iam['GroupDetailList']
        roles = iam['RoleDetailList']

        output = print_output(users, groups, roles)
        pipepager(output, cmd='less -R')

    except profile.exceptions.ServiceFailureException:
        print(colored("[*] Are you sure you have the rights to execute 'GetAccountAuthorizationDetails' API Call?","red"))

def print_output(users, groups, roles):
    output = ""
    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    output += colored("                                  Users\n","yellow",attrs=['bold'])
    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    if isinstance(users, list):
        for user in users:
            output += print_user_output(user)

    elif isinstance(users, dict):
        output += print_user_output(users)

    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    output += colored("                                  Groups\n","yellow",attrs=['bold'])
    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    if isinstance(groups, list):
        for group in groups:
            output += print_group_output(group)

    elif isinstance(groups, dict):
        output += print_group_output(groups)

    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    output += colored("                                  Roles\n","yellow",attrs=['bold'])
    output += colored("==========================================================================\n","yellow",attrs=['bold'])
    if isinstance(roles, list):
        for role in roles:
            output += print_role_output(role)

    elif isinstance(roles, dict):
        output += print_role_output(roles)

    return output

def print_user_output(x):
    output = ""
    output += (colored("------------------------\n", "yellow", attrs=['bold']))
    output += ("{}: {}\n".format(colored("Username", "yellow", attrs=['bold']), x['UserName']))
    output += (colored("------------------------\n", "yellow", attrs=['bold']))

    output += ("\t{}: {}\n".format(colored("Path", "red", attrs=['bold']), colored(x['Path'], "blue")))
    output += ("\t{}: {}\n".format(colored("UserName", "red", attrs=['bold']), colored(x['UserName'], "blue")))
    output += ("\t{}: {}\n".format(colored("UserId", "red", attrs=['bold']), colored(x['UserId'], "blue")))
    output += ("\t{}: {}\n".format(colored("Arn", "red", attrs=['bold']), colored(x['Arn'], "blue")))
    output += ("\t{}: {}\n".format(colored("CreateDate", "red", attrs=['bold']), colored(x['CreateDate'], "blue")))
    output += "\n"

    if 'UserPolicyList' in x:
        output += ("\t{}: \n".format(colored("UserPolicyList", "red", attrs=['bold'])))
        for k in x['UserPolicyList']:
            output += ("\t\t{}: {}\n".format(colored("PolicyName", "yellow", attrs=['bold']), colored(k['PolicyName'], "green")))
            output += ("\t\t{}: \n".format(colored("PolicyDocument", "yellow", attrs=['bold'])))
            output += ("\t\t\t{}: {}\n".format(colored("Version", "green", attrs=['bold']), colored(k['PolicyDocument']['Version'], "magenta")))
            output += ("\t\t\t{}:\n".format(colored("Statement", "green", attrs=['bold'])))
            for statement in (k['PolicyDocument']['Statement']):
                output += ("\t\t\t\t{}: {}\n".format(colored("Sid", "magenta", attrs=['bold']), colored(statement['Sid'], "white")))
                output += ("\t\t\t\t{}: {}\n".format(colored("Effect", "magenta", attrs=['bold']), colored(statement['Effect'], "white")))
                output += ("\t\t\t\t{}:\n".format(colored("Action", "magenta", attrs=['bold'])))
                if not len(statement['Action']) == 0:
                    for action in statement['Action']:
                        output += ("\t\t\t\t\t{}\n".format(colored(action, "white", attrs=['bold'])))
                output += ("\t\t\t\t{}: {}\n".format(colored("Resource", "magenta", attrs=['bold']), colored(statement['Resource'], "white")))
        output += "\n"

    if x['GroupList']:
        output += ("\t{}: \n".format(colored("GroupList", "red", attrs=['bold'])))
        for k in x['GroupList']:
            output += ("\t\t{}\n".format(colored(k, "yellow", attrs=['bold'])))
        output += "\n"

    if 'AttachedManagedPolicies' in x:
        output += ("\t{}: \n".format(colored("AttachedManagedPolicies", "red", attrs=['bold'])))
        for k in x['AttachedManagedPolicies']:
            for p, v in k.items():
                output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
            output += "\n"
        output += "\n"

    if 'PermissionsBoundary' in x:
        output += ("\t{}: \n".format(colored("PermissionsBoundary", "red", attrs=['bold'])))
        for p, v in (x['PermissionsBoundary']).items():
            output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
        output += "\n"

    if x['Tags']:
        output += ("\t{}: \n".format(colored("Tags", "red", attrs=['bold'])))
        for k in x['Tags']:
            for p, v in k.items():
                output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
        output += "\n"

    return output

def print_group_output(x):
    output = ""
    output += (colored("------------------------\n", "yellow", attrs=['bold']))
    output += ("{}: {}\n".format(colored("GroupName", "yellow", attrs=['bold']), x['GroupName']))
    output += (colored("------------------------\n", "yellow", attrs=['bold']))

    output += ("\t{}: {}\n".format(colored("Path", "red", attrs=['bold']), colored(x['Path'], "blue")))
    output += ("\t{}: {}\n".format(colored("GroupName", "red", attrs=['bold']), colored(x['GroupName'], "blue")))
    output += ("\t{}: {}\n".format(colored("GroupId", "red", attrs=['bold']), colored(x['GroupId'], "blue")))
    output += ("\t{}: {}\n".format(colored("Arn", "red", attrs=['bold']), colored(x['Arn'], "blue")))
    output += ("\t{}: {}\n".format(colored("CreateDate", "red", attrs=['bold']), colored(x['CreateDate'], "blue")))
    output += "\n"

    if 'GroupPolicyList' in x:
        output += ("\t{}: \n".format(colored("GroupPolicyList", "red", attrs=['bold'])))
        for k in x['GroupPolicyList']:
            output += ("\t\t{}: {}\n".format(colored("PolicyName", "yellow", attrs=['bold']), colored(k['PolicyName'], "green")))
            output += ("\t\t{}: \n".format(colored("PolicyDocument", "yellow", attrs=['bold'])))
            output += ("\t\t\t{}: {}\n".format(colored("Version", "green", attrs=['bold']), colored(k['PolicyDocument']['Version'], "magenta")))
            output += ("\t\t\t{}:\n".format(colored("Statement", "green", attrs=['bold'])))
            for statement in (k['PolicyDocument']['Statement']):
                output += ("\t\t\t\t{}: {}\n".format(colored("Sid", "magenta", attrs=['bold']), colored(statement['Sid'], "white")))
                output += ("\t\t\t\t{}: {}\n".format(colored("Effect", "magenta", attrs=['bold']), colored(statement['Effect'], "white")))
                output += ("\t\t\t\t{}:\n".format(colored("Action", "magenta", attrs=['bold'])))
                if not len(statement['Action']) == 0:
                    for action in statement['Action']:
                        output += ("\t\t\t\t\t{}\n".format(colored(action, "white", attrs=['bold'])))
                output += ("\t\t\t\t{}: {}\n".format(colored("Resource", "magenta", attrs=['bold']), colored(statement['Resource'], "white")))
        output += "\n"

    if 'AttachedManagedPolicies' in x:
        output += ("\t{}: \n".format(colored("AttachedManagedPolicies", "red", attrs=['bold'])))
        for k in x['AttachedManagedPolicies']:
            for p, v in k.items():
                output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
            output += "\n"
        output += "\n"

    return output

def print_role_output(x):
    output = ""
    output += (colored("------------------------\n", "yellow", attrs=['bold']))
    output += ("{}: {}\n".format(colored("RoleName", "yellow", attrs=['bold']), x['RoleName']))
    output += (colored("------------------------\n", "yellow", attrs=['bold']))

    output += ("\t{}: {}\n".format(colored("Path", "red", attrs=['bold']), colored(x['Path'], "blue")))
    output += ("\t{}: {}\n".format(colored("UserName", "red", attrs=['bold']), colored(x['RoleName'], "blue")))
    output += ("\t{}: {}\n".format(colored("RoleId", "red", attrs=['bold']), colored(x['RoleId'], "blue")))
    output += ("\t{}: {}\n".format(colored("Arn", "red", attrs=['bold']), colored(x['Arn'], "blue")))
    output += ("\t{}: {}\n".format(colored("CreateDate", "red", attrs=['bold']), colored(x['CreateDate'], "blue")))
    output += "\n"

    if 'AssumeRolePolicyDocument' in x:
        #k = x['AssumeRolePolicyDocument']
        output += ("\t{}: \n".format(colored("AssumeRolePolicyDocument", "red", attrs=['bold'])))
        output += ("\t\t\t{}: {}\n".format(colored("Version", "green", attrs=['bold']), colored(x['AssumeRolePolicyDocument']['Version'], "magenta")))
        output += ("\t\t\t{}:\n".format(colored("Statement", "green", attrs=['bold'])))
        for statement in (x['AssumeRolePolicyDocument']['Statement']):
            output += ("\t\t\t\t{}: {}\n".format(colored("Effect", "magenta", attrs=['bold']), colored(statement['Effect'], "white")))
            output += ("\t\t\t\t{}:\n".format(colored("Principal", "magenta", attrs=['bold'])))
            output += ("\t\t\t\t\t{}:\n".format(colored("Service", "white", attrs=['bold'])))
            if isinstance(statement['Principal']['Service'], list):
                for service in statement['Principal']['Service']:
                    output += ("\t\t\t\t\t\t{}\n".format(colored(service, "magenta")))
            else:
                output += ("\t\t\t\t\t\t{}\n".format(colored(statement['Principal']['Service'], "magenta")))
            output += ("\t\t\t\t{}:\n".format(colored("Action", "magenta", attrs=['bold'])))
            if isinstance(statement['Action'], list):
                for action in statement['Action']:
                    output += ("\t\t\t\t\t{}\n".format(colored(action, "white", attrs=['bold'])))
            else:
                output += ("\t\t\t\t\t{}\n".format(colored(statement['Action'], "white", attrs=['bold'])))
        output += "\n"

    if x['InstanceProfileList']:
        output += ("\t{}: \n".format(colored("InstanceProfileList", "red", attrs=['bold'])))
        for k in x['InstanceProfileList']:
            output += ("\t\t{}: {}\n".format(colored("Path", "blue", attrs=['bold']), colored(k['Path'], "green")))
            output += ("\t\t{}: {}\n".format(colored("InstanceProfileName", "blue", attrs=['bold']), colored(k['InstanceProfileName'], "green")))
            output += ("\t\t{}: {}\n".format(colored("InstanceProfileId", "blue", attrs=['bold']), colored(k['InstanceProfileId'], "green")))
            output += ("\t\t{}: {}\n".format(colored("Arn", "blue", attrs=['bold']), colored(k['Arn'], "green")))
            output += ("\t\t{}: {}\n".format(colored("CreateDate", "blue", attrs=['bold']), colored(k['CreateDate'], "green")))
            output += "\n"
            output += ("\t\t{}: \n".format(colored("Roles", "blue", attrs=['bold'])))
            for role in k['Roles']:
                output += ("\t\t\t{}: {}\n".format(colored("Path", "green", attrs=['bold']), colored(role['Path'], "yellow")))
                output += ("\t\t\t{}: {}\n".format(colored("RoleName", "green", attrs=['bold']), colored(role['RoleName'], "yellow")))
                output += ("\t\t\t{}: {}\n".format(colored("RoleId", "green", attrs=['bold']),colored(role['RoleId'], "yellow")))
                output += ("\t\t\t{}: {}\n".format(colored("Arn", "green", attrs=['bold']), colored(role['Arn'], "yellow")))
                output += ("\t\t\t{}: {}\n".format(colored("CreateDate", "green", attrs=['bold']), colored(role['CreateDate'], "yellow")))
                output += "\n"
                if 'AssumeRolePolicyDocument' in role:
                    r = role['AssumeRolePolicyDocument']
                    output += ("\t\t\t{}: \n".format(colored("AssumeRolePolicyDocument", "green", attrs=['bold'])))
                    output += ("\t\t\t\t{}: {}\n".format(colored("Version", "yellow", attrs=['bold']), colored(r['Version'], "magenta")))
                    output += ("\t\t\t\t{}:\n".format(colored("Statement", "yellow", attrs=['bold'])))
                    for statement in (r['Statement']):
                        output += ("\t\t\t\t\t{}: {}\n".format(colored("Effect", "magenta", attrs=['bold']),colored(statement['Effect'], "white")))
                        output += ("\t\t\t\t\t{}:\n".format(colored("Principal", "magenta", attrs=['bold'])))
                        output += ("\t\t\t\t\t\t{}:\n".format(colored("Service", "white", attrs=['bold'])))
                        if isinstance(statement['Principal']['Service'], list):
                            for service in statement['Principal']['Service']:
                                output += ("\t\t\t\t\t\t\t{}\n".format(colored(service, "magenta")))
                        else:
                            output += ("\t\t\t\t\t\t\t{}\n".format(colored(statement['Principal']['Service'], "magenta")))
                        output += ("\t\t\t\t\t\t{}:\n".format(colored("Action", "magenta", attrs=['bold'])))
                        if isinstance(statement['Action'], list):
                            for action in statement['Action']:
                                output += ("\t\t\t\t\t\t\t{}\n".format(colored(action, "white", attrs=['bold'])))
                        else:
                            output += ("\t\t\t\t\t\t\t{}\n".format(colored(statement['Action'], "white", attrs=['bold'])))
                    output += "\n"

    if x['RolePolicyList']:
        output += ("\t{}: \n".format(colored("RolePolicyList", "red", attrs=['bold'])))
        for k in x['RolePolicyList']:
            output += ("\t\t{}: {}\n".format(colored("PolicyName", "yellow", attrs=['bold']), colored(k['PolicyName'], "green")))
            output += ("\t\t{}: \n".format(colored("PolicyDocument", "yellow", attrs=['bold'])))
            output += ("\t\t\t{}: {}\n".format(colored("Version", "green", attrs=['bold']), colored(k['PolicyDocument']['Version'], "magenta")))
            output += ("\t\t\t{}:\n".format(colored("Statement", "green", attrs=['bold'])))
            for statement in (k['PolicyDocument']['Statement']):
                output += ("\t\t\t\t{}: {}\n".format(colored("Sid", "magenta", attrs=['bold']), colored(statement['Sid'], "white")))
                output += ("\t\t\t\t{}: {}\n".format(colored("Effect", "magenta", attrs=['bold']), colored(statement['Effect'], "white")))
                output += ("\t\t\t\t{}:\n".format(colored("Action", "magenta", attrs=['bold'])))
                if not len(statement['Action']) == 0:
                    for action in statement['Action']:
                        output += ("\t\t\t\t\t{}\n".format(colored(action, "white", attrs=['bold'])))
                output += ("\t\t\t\t{}: {}\n".format(colored("Resource", "magenta", attrs=['bold']), colored(statement['Resource'], "white")))
                output += ("\t\t\t\t{}:\n".format(colored("Condition", "magenta", attrs=['bold'])))
                for key,value in (statement['Condition']).items():
                    output += ("\t\t\t\t\t{}: {}\n".format(colored(key, "magenta", attrs=['bold']), colored(value, "white")))
        output += "\n"

    if 'AttachedManagedPolicies' in x:
        output += ("\t{}: \n".format(colored("AttachedManagedPolicies", "red", attrs=['bold'])))
        for k in x['AttachedManagedPolicies']:
            for p, v in k.items():
                output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
            output += "\n"
        output += "\n"

    if 'PermissionsBoundary' in x:
        output += ("\t{}: \n".format(colored("PermissionsBoundary", "red", attrs=['bold'])))
        for p, v in (x['PermissionsBoundary']).items():
            output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
        output += "\n"

    if x['Tags']:
        output += ("\t{}: \n".format(colored("Tags", "red", attrs=['bold'])))
        for k in x['Tags']:
            #output += ("\t\t{}\n".format(colored(k, "yellow", attrs=['bold'])))
            for p, v in k.items():
                output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
        output += "\n"

    if 'RoleLastUsed' in x:
        output += ("\t{}: \n".format(colored("RoleLastUsed", "red", attrs=['bold'])))
        for p, v in (x['RoleLastUsed']).items():
            output += ("\t\t{}: {}\n".format(colored(p, "yellow", attrs=['bold']), colored(v, "green")))
        output += "\n"

    return output