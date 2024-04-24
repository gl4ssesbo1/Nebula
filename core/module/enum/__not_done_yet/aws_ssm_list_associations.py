import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import sys

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "ssm",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "ASSOCIATION-ID": {
        "value": "",
        "required": "false",
        "description":"Lists commands issued against this instance ID."
    },
    "ASSOCIATION-NAME": {
        "value": "",
        "required": "false",
        "description":"Lists associations with the name or part of name."
    },
    "ASSOCIATION-STATUS-NAME": {
        "value": "",
        "required": "false",
        "description":"Lists commands with a specific Status."
    },
    "EXECUTION-STAGE": {
        "value": "",
        "required": "false",
        "description":"Lists commands on a specific Execution Stage."
    },
    "INVOKED-BEFORE": {
        "value": "",
        "required": "false",
        "description":"Lists commands Invoked before a specific date. It uses the date format: 2018-07-07T00:00:00Z to see a list of command executions occurring before July 7, 2018 on 00:00"
    },
    "INVOKED-AFTER": {
        "value": "",
        "required": "false",
        "description":"Lists commands Invoked before a specific date. It uses the date format: 2018-07-07T00:00:00Z to see a list of command executions occurring July 7, 2018 on 00:00, and later."
    }
}
description = "Get a list of the commands that were or are currently executed. Can be filtered using CommandID, InstanceID, Time invoked (either before or after a specific time), Status and Execution Stage. Requires ssm:ListCommands permission."

aws_command = "aws ssm list-commands --region <region> --profile <profile>\n" \
              "\taws ssm list-commands --command-id <command ID> --region <region> --profile <profile>"

colors = [
    "not-used",
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
        n_tab+=1
        for key, value in d.items():
            if not isinstance(value, dict) and not isinstance(value, list):
                output += ("{}{}: {}\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold']) , colored(value, colors[n_tab+1])))
            else:
                output += ("{}{}:\n".format("\t"*n_tab, colored(key, colors[n_tab], attrs=['bold'])))
                list_dictionary(value, n_tab)

def exploit(profile, workspace):
    try:
        n_tab = 0
        global output

        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        file = "{}_ssm_list_associations".format(dt_string)
        filename = "./workspaces/{}/{}".format(workspace, file)

        command_id = variables['COMMAND-ID']['value']
        documentname = variables['DOCUMENTNAME']['value']
        instance_id = variables['INSTANCE-ID']['value']
        status = variables['STATUS']['value']
        invoked_before = variables['INVOKED-BEFORE']['value']
        invoked_after = variables['INVOKED-AFTER']['value']
        execution_stage = variables['EXECUTION-STAGE']['value']

        args = {}
        filters = []

        if not command_id == "":
            args['CommandId'] = command_id

        if not instance_id == "":
            args['InstanceId'] = instance_id

        if not status == "":
            a = {}
            a['key'] = 'Status'
            a['value'] = status
            filters.append(a)

        if not invoked_before == "":
            a = {}
            a['key'] = 'InvokedBefore'
            a['value'] = invoked_before
            filters.append(a)

        if not invoked_after == "":
            a = {}
            a['key'] = 'InvokedAfter'
            a['value'] = invoked_after
            filters.append(a)

        if not execution_stage == "":
            a = {}
            a['key'] = 'ExecutionStage'
            a['value'] = execution_stage
            filters.append(a)

        if not documentname == "":
            a = {}
            a['key'] = 'DocumentName'
            a['value'] = documentname
            filters.append(a)

        if filters:
            args['Filters'] = filters

        response = profile.list_commands(
            **args
        )

        json_data = response['Commands']
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, default=str)
            print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

        title_name = "CommandId"
        output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        for data in json_data:
            output += colored("{}: {}\n".format(title_name, data[title_name]), "yellow", attrs=['bold'])
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            list_dictionary(data, n_tab)
            output += "\n"
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
        pipepager(output, "less -R")
        output = ""

    except:
        e = sys.exc_info()[1]
        print(colored("[*] {}".format(e), "red"))