import sys
from pydoc import pipepager
from termcolor import colored
from datetime import datetime
import json

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "s3",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

description = "List s3 buckets that are accessible from the IAM provided or public to all. Requires Secret Key and Access Key of an IAM that has access to it."

aws_command = "aws s3api list-buckets --query \"Buckets[].Name\" --region <region> --profile <profile>"


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
    file = "{}_s3_enum_all".format(dt_string)
    filename = "./workspaces/{}/{}".format(workspace, file)
    json_data = {}
    buckets = []

    try:
        response = profile.list_buckets()
        json_data['Owner'] = response['Owner']

        buckets = []

        for buck in response['Buckets']:
            name = buck['Name']
            json_data[name] = {}
            json_data[name]['CreationDate'] = buck['CreationDate']

        for buck in response['Buckets']:
            buckets.append(buck['Name'])

        del response

    except:
        e = sys.exc_info()[1]
        print(colored(
            "[*] {}".format(e), "red"
        ))

    if len(buckets) > 0:
        for bucket in buckets:
            try:
                response = profile.get_bucket_policy_status(
                    Bucket=bucket
                )
                json_data[bucket]['IsPublic'] = response['PolicyStatus']['IsPublic']
                del response
            except:
                e = sys.exc_info()[1]
                if "NoSuchBucketPolicy" in str(e):
                    json_data[bucket]['IsPublic'] = False
                else:
                    print(colored(
                        "[*] {}".format(e), "red"
                    ))

            try:
                response = profile.get_bucket_policy(
                    Bucket=bucket
                )
                json_data[bucket]['BucketPolicy'] = json.loads(response['Policy'])
                del response
            except:
                e = sys.exc_info()[1]
                if "NoSuchBucketPolicy" in str(e):
                    json_data[bucket]['BucketPolicy'] = {}
                else:
                    print(colored(
                        "[*] {}".format(e), "red"
                    ))

            try:
                maxkeys = 1000
                response = profile.list_objects_v2(
                    Bucket=bucket,
                    MaxKeys=maxkeys
                )

                json_data[bucket]['Contents'] = response['Contents']
                while response['IsTruncated']:
                    response = profile.list_objects_v2(
                        Bucket=bucket,
                        MaxKeys=maxkeys,
                        ContinuationToken=response['NextContinuationToken']
                    )
                    (json_data[bucket]['Contents']).extend(response['Contents'])

                del response

            except:
                e = sys.exc_info()[1]
                print(colored(
                    "[*] {}".format(e), "red"
                ))

            for key in json_data[bucket]['Contents']:
                try:
                    response = profile.get_object_acl(
                        Bucket=bucket,
                        Key=key['Key']
                    )
                    key['Grants'] = response['Grants']

                except:
                    e = sys.exc_info()[1]
                    print(colored(
                        "[*] {}".format(e), "red"
                    ))

    for key, value in json_data.items():
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

    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent=4, default=str)
        print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))
