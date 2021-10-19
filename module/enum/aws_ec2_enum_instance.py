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
    workspaces = {}

    try:
        if not variables["INSTANCE-ID"]['value'] == "":
            inst = profile.describe_instances(
                InstanceIds=[
                    variables["INSTANCE-ID"]['value']
                ]
            )
            workspaces["Reservations"] = inst["Reservations"]

            with open(filename, 'w') as outfile:
                json.dump(workspaces, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
        else:
            inst = profile.describe_instances()
            workspaces["Reservations"] = inst["Reservations"]

            with open(filename, 'w') as outfile:
                json.dump(workspaces, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        if not len(workspaces["Reservations"]) == 0:
            for key, value in (workspaces["Reservations"]).items():
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                list_dictionary(value, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
    except:
        output += extra_exploit(profile, filename)

    pipepager(output, cmd='less -R')

def extra_exploit(profile, filename):
    n_tab = 0
    instance_attribs = {}
    global output
    try:
        inst = profile.describe_instances()
        instance_attribs["Reservations"] = inst["Reservations"]
    except:
        print(colored("[*] you have no rights to Describe Instances. ", "red"))

    try:
        inst = profile.describe_images()
        instance_attribs["Images"] = inst["Images"]
    except:
        print(colored("[*] you have no rights to Describe Images. ", "red"))

    try:
        inst = profile.describe_security_groups()
        instance_attribs["SecurityGroups"] = inst["SecurityGroups"]
    except:
        print(colored("[*] you have no rights to Describe Security Groups. ", "red"))

    try:
        inst = profile.describe_snapshots()
        instance_attribs["Snapshots"] = inst["Snapshots"]
    except:
        print(colored("[*] you have no rights to Describe Snapshots. ", "red"))

    try:
        inst = profile.describe_key_pairs()
        instance_attribs["KeyPairs"] = inst["KeyPairs"]
    except:
        print(colored("[*] you have no rights to Describe Key Pairs. ", "red"))

    try:
        inst = profile.describe_subnets()
        instance_attribs["Subnets"] = inst["Subnets"]
    except:
        print(colored("[*] you have no rights to Describe Subnets. ", "red"))

    try:
        inst = profile.describe_tags()
        instance_attribs["Tags"] = inst["Tags"]
    except:
        print(colored("[*] you have no rights to Describe Tags. ", "red"))

    try:
        inst = profile.describe_volumes()
        instance_attribs["Volumes"] = inst["Volumes"]
    except:
        print(colored("[*] you have no rights to Describe Volumes. ", "red"))

    try:
        inst = profile.describe_vpcs()
        instance_attribs["Vpcs"] = inst["Vpcs"]
    except:
        print(colored("[*] you have no rights to Describe VCPs. ", "red"))

    with open(filename, 'w') as outfile:
        json.dump(instance_attribs, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    if not len(instance_attribs) == 0:
        for key, value in instance_attribs.items():
            output += colored("==========================================================================\n",
                              "yellow", attrs=['bold'])
            output += colored("                                  " + key + " \n", "yellow", attrs=['bold'])
            output += colored("==========================================================================\n",
                              "yellow", attrs=['bold'])
            if isinstance(value, list):
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                for data in value:
                    list_dictionary(data, n_tab)
                    output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            else:
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])
                output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                list_dictionary(value, n_tab)
                output += colored("---------------------------------\n", "yellow", attrs=['bold'])

    return output