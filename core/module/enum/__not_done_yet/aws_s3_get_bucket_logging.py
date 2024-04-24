from termcolor import colored
import json
import botocore
from datetime import datetime

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE":{
		"value":"s3",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "BUCKET":{
        "value":"",
        "required":"true",
        "description":"The bucket to enumerate."
    }
}

description = "Check if the logs are configured for monitoring the bucket and who has the rights to them."

aws_command = "aws s3api get-bucket-logging --bucket <my-bucket> --region <region> --profile <profile>"

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
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_s3_get_bucket_logging".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)

    try:
        bucket = variables['BUCKET']['value']
        n_tab = 0
        global output
        response = profile.get_bucket_logging(
            Bucket=bucket
        )
        if 'LoggingEnabled' in response:
            json_data = response['LoggingEnabled']

            print(colored("---------------------------", "yellow", attrs=["bold"]))
            print("{}:\t{}".format(colored("Bucket", "yellow", attrs=['bold']),
                                   colored(variables['BUCKET']['value'], "yellow")))
            print(colored("---------------------------", "yellow", attrs=["bold"]))

            list_dictionary(json_data, n_tab)
            output += colored("---------------------------------\n", "yellow", attrs=['bold'])
            print(output)
            with open(filename, 'w') as outfile:
                json.dump(json_data, outfile, indent=4, default=str)
                print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
        else:
            print(colored("[*] Bucket '{}' has not logging configured".format(bucket),"green"))

    except profile.exceptions.NoSuchBucket as e:
        print(colored("[*] The Bucket does not exist.", "red"))
