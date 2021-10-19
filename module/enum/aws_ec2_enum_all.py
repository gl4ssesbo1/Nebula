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
        "value": "ec2",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "ACCOUNTID": {
        "value": "",
        "required": "false",
        "description": "The ID of the account we are testing. Will be used as Owner."
    }
}

aws_command = "aws ec2 describe-instances --region {} --profile {}"

description = "Describes instances attribues: Instances, VCP, Zones, Images, Security Groups, Snapshots, Subnets, Tags, Volumes. Requires Secret Key and Access Key of an IAM that has access to all or any of the API calls: DescribeAvailabilityZones, DescribeImages, DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups, DescribeSnapshots, DescribeSubnets, DescribeTags, DescribeVolumes, DescribeVpcs"

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""


def list_dictionary(d, n_tab):
    global output
    if isinstance(d, list):
        n_tab += 1
        for i in d:
            if not isinstance(i, list) and not isinstance(i, dict):
                output += ("{}{}\n".format("\t" * n_tab, colored(i, colors[n_tab])))
            else:
                list_dictionary(i, n_tab)
    elif isinstance(d, dict):
        n_tab += 1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold']),
                                               colored(value, colors[n_tab + 1])))
            else:
                output += ("{}{}:\n".format("\t" * n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)


def exploit(profile, workspace):
    global output
    n_tab = 0
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_ec2_enum_instances".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    instance_attribs = {}
    accountid = variables['ACCOUNTID']['value']



    print(colored("[*] This might take a while. ", "yellow"))

    try:
        inst = profile.describe_instances()
        if len(inst["Reservations"]) > 0:
            instance_attribs["Reservations"] = inst["Reservations"]
            print(colored("[*] Instances Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Instances. ", "red"))

    try:
        inst = profile.describe_images()
        if len(inst["Images"]) > 0:
            instance_attribs["Images"] = inst["Images"]
            print(colored("[*] Images Done. ", "green"))
            print(colored("[*] You have rights to Describe Images, but the output is big so it's only saved on the file. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Images. ", "red"))

    try:
        inst = profile.describe_security_groups()
        if len(inst["SecurityGroups"]) > 0:
            instance_attribs["SecurityGroups"] = inst["SecurityGroups"]
            print(colored("[*] Security Groups Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Security Groups. ", "red"))

    try:
        inst = profile.describe_snapshots(
            Filters=[
                {
                    'Name': 'owner-id',
                    'Values': [
                        accountid,
                    ]
                },
            ],
        )
        if len(inst["Snapshots"]) > 0:
            instance_attribs["Snapshots"] = inst["Snapshots"]
            print(colored("[*] Snapshots Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Snapshots. ", "red"))

    try:
        inst = profile.describe_key_pairs()
        if len(inst["KeyPairs"]) > 0:
            instance_attribs["KeyPairs"] = inst["KeyPairs"]
            print(colored("[*] Key Pairs Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Key Pairs. ", "red"))

    try:
        inst = profile.describe_subnets()
        if len(inst["Subnets"]) > 0:
            instance_attribs["Subnets"] = inst["Subnets"]
            print(colored("[*] Subnets Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Subnets. ", "red"))

    try:
        inst = profile.describe_tags()
        if len(inst["Tags"]) > 0:
            instance_attribs["Tags"] = inst["Tags"]
            print(colored("[*] Tags Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Tags. ", "red"))

    try:
        inst = profile.describe_volumes()
        if len(inst["Volumes"]) > 0:
            instance_attribs["Volumes"] = inst["Volumes"]
            print(colored("[*] Volumes Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe Volumes. ", "red"))

    try:
        inst = profile.describe_vpcs()
        if len(inst["Vpcs"]) > 0:
            instance_attribs["Vpcs"] = inst["Vpcs"]
            print(colored("[*] VPCs Done. ", "green"))
    except:
        print(colored("[*] you have no rights to Describe VCPs. ", "red"))

    with open(filename, 'w') as outfile:
        json.dump(instance_attribs, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    for key, value in instance_attribs.items():
        if key == "Images":
            continue
        else:
            output += colored("==========================================================================\n",
                              "yellow", attrs=['bold'])
            output += colored("                                  " + key + " \n", "yellow", attrs=['bold'])
            output += colored("==========================================================================\n",
                              "yellow", attrs=['bold'])
            if isinstance(value, list):
                for data in value:
                    list_dictionary(data, n_tab)
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            else:
                output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                list_dictionary(value, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])

    pipepager(output, cmd='less -R')