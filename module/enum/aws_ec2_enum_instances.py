import json
from termcolor import colored
from datetime import datetime
#from pypager.source import GeneratorSource
#from pypager.pager import Pager
import sys
from pydoc import pipepager

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE":{
        "value":"ec2",
        "required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },

    "INSTANCE-ID":{
        "value":"",
        "required":"false",
        "description":"The ID of the instance you want to enumerate. If not supplied, all instances will be enumerated."
    }
}

aws_command = "aws ec2 describe-instances --region {} --profile {}"

description = "Describes instances attribues: Instances, VCP, Zones, Images, Security Groups, Snapshots, Subnets, Tags, Volumes. Requires Secret Key and Access Key of an IAM that has access to all or any of the API calls: DescribeAvailabilityZones, DescribeImages, DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups, DescribeSnapshots, DescribeSubnets, DescribeTags, DescribeVolumes, DescribeVpcs"

def exploit(profile, workspace):
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
            output = print_output(inst)

            with open(filename, 'w') as outfile:
                json.dump(workspaces, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
        else:
            inst = profile.describe_instances()
            workspaces["Reservations"] = inst["Reservations"]

            with open(filename, 'w') as outfile:
                json.dump(workspaces, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

            output = print_output(inst)

    except:
        output += extra_exploit(profile, filename)

    pipepager(output, cmd='less -R')

def extra_exploit(profile, filename):
    instance_attribs = {}
    output = ""
    try:
        inst = profile.describe_images()
        instance_attribs["Images"] = inst["Images"]
        output += print_output_other(inst, "Images", "Images")
    except:
        print(colored("[*] you have no rights to Describe Images. ","red"))

    try:
        inst = profile.describe_security_groups()
        instance_attribs["SecurityGroups"] = inst["SecurityGroups"]
        output += print_output_other(inst, "SecurityGroups", "SecurityGroups")
    except:
        print(colored("[*] you have no rights to Describe Security Groups. ","red"))

    try:
        inst = profile.describe_snapshots()
        instance_attribs["Snapshots"] = inst["Snapshots"]
        output += print_output_other(inst, "Snapshots", "SnapshotId")
    except:
        print(colored("[*] you have no rights to Describe Snapshots. ","red"))

    try:
        inst = profile.describe_key_pairs()
        instance_attribs["KeyPairs"] = inst["KeyPairs"]
        output += print_output_other(inst, "KeyPairs", "KeyPairId")
    except:
        print(colored("[*] you have no rights to Describe Key Pairs. ","red"))

    try:
        inst = profile.describe_subnets()
        instance_attribs["Subnets"] = inst["Subnets"]
        output += print_output_other(inst, "Subnets", "SubnetId")
    except:
        print(colored("[*] you have no rights to Describe Subnets. ","red"))

    try:
        inst = profile.describe_tags()
        instance_attribs["Tags"] = inst["Tags"]
        output += print_output_other(inst, "Tags", "TagId")
    except:
        print(colored("[*] you have no rights to Describe Tags. ","red"))

    try:
        inst = profile.describe_volumes()
        instance_attribs["Volumes"] = inst["Volumes"]
        output += print_output_other(inst, "Volumes", "VolumeId")
    except:
        print(colored("[*] you have no rights to Describe Volumes. ","red"))

    try:
        inst = profile.describe_vpcs()
        instance_attribs["Vpcs"] = inst["Vpcs"]
        output += print_output_other(inst, "Vpcs", "VpcId")
    except:
        print(colored("[*] you have no rights to Describe VCPs. ","red"))

    with open(filename, 'w') as outfile:
        json.dump(instance_attribs, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

    return output

def print_output(inst):
    output = colored("----------------------------------------------\n", "yellow", attrs=['bold'])
    for x in inst["Reservations"]:
        for y in x["Instances"]:
            name = y["InstanceId"]
            output += "{}: {}\n".format(colored("Instance","red",attrs=['bold']), colored(name,"yellow"))
            output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
            for key,value in y.items():
                if isinstance(value, dict):
                    output += "\t{}:\t{}\n".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue"))

                if isinstance(value, list):
                    output += "\t{}:\t{}\n".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue"))

                else:
                    output += "\t{}:\t{}\n".format(colored(key, "red"),colored(value, "blue"))

            output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
    return output

def print_output_other(inst, index, name):
    output = ""
    output += colored("----------------------------------------------\n", "yellow", attrs=['bold'])
    for y in inst[index]:
        name = y[name]
        output += "{}: {}\n".format(colored("Instance","red",attrs=['bold']), colored(name,"yellow"))
        output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
        for key,value in y.items():
            if isinstance(value, dict):
                output += "\t{}:\t{}\n".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue"))

            if isinstance(value, list):
                output += "\t{}:\t{}\n".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue"))

            else:
                output += "\t{}:\t{}\n".format(colored(key, "red"),colored(value, "blue"))

        output += colored("----------------------------------------------\n","yellow",attrs=['bold'])
    return output

def print_output_other_2(inst, index, name):
    print(colored("----------------------------------------------", "yellow", attrs=['bold']))
    for y in inst[index]:
        name = y[name]
        print("{}: {}".format(colored("Instance","red",attrs=['bold']), colored(name,"yellow")))
        print(colored("----------------------------------------------","yellow",attrs=['bold']))
        for key,value in y.items():
            if isinstance(value, dict):
                print("\t{}:\t{}".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue")))

            if isinstance(value, list):
                print("\t{}:\t{}".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue")))

            else:
                print("\t{}:\t{}".format(colored(key, "red"),colored(value, "blue")))

        print(colored("----------------------------------------------","yellow",attrs=['bold']))

def print_output_2(inst):
    print(colored("----------------------------------------------", "yellow", attrs=['bold']))
    for x in inst["Reservations"]:
        for y in x["Instances"]:
            name = y["InstanceId"]
            print("{}: {}".format(colored("Instance","red",attrs=['bold']), colored(name,"yellow")))
            print(colored("----------------------------------------------","yellow",attrs=['bold']))
            for key,value in y.items():
                if isinstance(value, dict):
                    print("\t{}:\t{}".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue")))

                if isinstance(value, list):
                    print("\t{}:\t{}".format(colored(key,"red"), colored(json.dumps(value, indent=4, default=str),"blue")))

                else:
                    print("\t{}:\t{}".format(colored(key, "red"),colored(value, "blue")))

            print(colored("----------------------------------------------","yellow",attrs=['bold']))
