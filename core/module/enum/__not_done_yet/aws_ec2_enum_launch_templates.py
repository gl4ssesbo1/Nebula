from termcolor import colored
from datetime import datetime
import json
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
    "TEMPLATEID":{
        "value": "",
        "required": "false",
        "description":"The ID of the launch template to enumerate. If not provided, all templates will be enumerated."
    }
}

description = "Enumerate EC2 Launch Templates. EC2 describe-launch-templates call is used and IAM needs access to DescribeLaunchTemplates API."

aws_command = "aws ec2 describe-launch-templates --region <region> --profile <profile>"

def exploit(profile, workspace):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_ec2_enum_launch_templates".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    if variables['TEMPLATEID']['value']:
        id = (variables['TEMPLATEID']['value']).split(",")
        try:
            response = profile.describe_launch_templates(
                LaunchTemplateIds=id,
                MaxResults=1000
            )
            while response.get('NextToken'):
                response = profile.describe_launch_templates(
                    LaunchTemplateIds=id,
                    MaxResults=1000,
                    NextToken=response['NextToken']
                )
            with open(filename, 'w') as outfile:
                json.dump(response['LaunchTemplates'], outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

            print_output(response)
        except:
            print(colored("[*] {}".format("The template ID is incorrect or the template does not exist."), "red"))

    else:
        response = profile.describe_launch_templates()
        while response.get('NextToken'):
            response = profile.describe_launch_templates(
                NextToken=response['NextToken']
            )
        with open(filename, 'w') as outfile:
            json.dump(response['LaunchTemplates'], outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        print_output(response)

def print_output(response):
    output = ""
    for instance in response['LaunchTemplates']:
        output += colored("-------------------------------------\n", "yellow", attrs=['bold'])
        output += "{}: {}\n".format(colored("LaunchTemplateName", "yellow", attrs=['bold']), instance['LaunchTemplateName'])
        output += colored("-------------------------------------\n", "yellow", attrs=['bold'])
        for key,value in instance.items():
            output += "\t{}: {}\n".format(colored(key, "red", attrs=['bold']), colored(value, "blue"))
        output += "\n"
    pipepager(output, cmd='less -R')
