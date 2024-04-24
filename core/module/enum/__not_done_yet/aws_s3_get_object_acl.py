from termcolor import colored
import json
import sys
from datetime import datetime
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
		"value":"s3",
		"required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
    "KEY":{
        "value":"",
        "required":"false",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "BUCKET":{
        "value":"",
        "required":"true",
        "description":"The service that will be used to run the module. It cannot be changed."
    }
}

description = "List s3 buckets that are accessible from the IAM provided or public to all. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws ec2 describe-instances --region {} --profile {}"

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
    file = "{}_s3_get_object_acl".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    bucket = variables['BUCKET']['value']
    file_key = variables['KEY']['value']

    if not file_key == "":
        try:
            response = profile.get_object_acl(
                Bucket=bucket,
                Key=file_key
            )

            json_data = {}
            json_data['Grants'] = response['Grants']
            json_data['Owner'] = response['Owner']

            with open(filename,'w') as outputfile:
                json.dump(json_data, outputfile, indent=4, default=str)
            print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
                  colored(".", "green"))

            print (colored("---------------------------", "yellow", attrs=["bold"]))
            print ("{}:\t{}".format(colored("Key","yellow",attrs=['bold']),colored(variables['KEY']['value'],"yellow")))
            print (colored("---------------------------", "yellow", attrs=["bold"]))

            print ("\t{}:".format(colored("Owner","green",attrs=['bold'])))
            for key,value in (response['Owner']).items():
                print("\t\t{}:\t{}".format(colored(key,"magenta",attrs=['bold']),colored(value,"white")))

            for grant in response['Grants']:
                print ("\t{}:".format(colored("Grantee","green",attrs=['bold'])))
                for x,y in (grant['Grantee']).items():
                    print("\t\t{}:\t{}".format(colored(x,"magenta"), y))
                print ("\t{}:\t{}".format(colored("Permission","green",attrs=['bold']),colored(grant["Permission"],"white")))
                print()

        except profile.exceptions.NoSuchBucket:
            print(colored("[*] The Bucket does not exist.", "red"))

        except profile.exceptions.NoSuchKey:
            print(colored("[*] The Key does not exist.", "red"))

    else:
        test = 0
        try:
            key_response = profile.list_objects_v2(
                        Bucket=bucket
                )

        except profile.exceptions.NoSuchBucket as e:
            print(colored("[*] The Bucket does not exist.", "red"))
            test = 1

        except:
            print(colored("[*] Code Problem", "red"))
            e = sys.exc_info()
            print(colored("[*] {}".format(e), "red"))
            test = 1

        if test == 0:
            n_tab = 0
            global output
            try:
                keys = []
                for key in key_response['Contents']:
                    keys.append(key['Key'])

                json_data = {}
                for key in keys:
                    k = []
                    response = profile.get_object_acl(
                        Bucket=bucket,
                        Key=key
                    )
                    k.append(response['Owner'])
                    k.append(response['Grants'])
                    json_data[key] = k

                with open(filename, 'w') as outputfile:
                    json.dump(json_data, outputfile, indent=4, default=str)
                print(colored("[*] Output written to file", "green"), colored("'{}'".format(filename), "blue"),
                      colored(".", "green"))

                output += colored("---------------------------------------------------------------------------------------------------\n", "yellow", attrs=['bold'])
                for key,data in json_data.items():
                    output += colored("{}\n".format(key), "yellow", attrs=['bold'])
                    output += colored("---------------------------------------------------------------------------------------------------\n", "yellow", attrs=['bold'])
                    list_dictionary(data, n_tab)
                    output += "\n"
                    output += colored("---------------------------------------------------------------------------------------------------\n", "yellow", attrs=['bold'])
                pipepager(output, "less -R")
                output = ""

            except profile.exceptions.NoSuchKey:
                print(colored("[*] The Key does not exist.", "red"))