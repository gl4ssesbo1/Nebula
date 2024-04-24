from termcolor import colored
from __listeners import aws_python_tcp_server
import os

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
    },
    "HOST": {
        "value": "0.0.0.0",
        "required": "true",
        "description": "The Host/IP of the C2 Server."
    },
    "PORT": {
        "value": "",
        "required": "true",
        "description": "The C2 Server Port."
    },
    "ENCRYPTION-KEY": {
        "value": "",
        "required": "false",
        "description": "The 1024 bit XOR key to encrypt the traffic. If left empty, it will auto generate."
    }
}
description = "TCP Listener for Reverse Shell stagers/aws_python_tcp"

aws_command = "None"

def exploit(workspace):
    host = variables['HOST']['value']
    port = int(variables['PORT']['value'])
    enc_key = variables['ENCRYPTION-KEY']['value']

    if os.geteuid() == 0:
        aws_python_tcp_server.main(host, port, workspace, enc_key)
    else:
        print(colored("[*] You need to be root to be able to open ports. Dump credentials to save them and rerun the tool as privileged user.","red"))