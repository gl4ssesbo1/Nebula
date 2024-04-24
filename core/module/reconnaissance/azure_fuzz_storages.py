from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager
import socket

author = {
    "name":"",
    "twitter":"",
    "github":"",
    "email":""
}

needs_creds = False

variables = {
	"SERVICE": {
		"value": "none",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"STORAGE-NAME": {
		"value": "",
		"required": "false",
        "description":"Single storage to test as Blob, File Server, Data Table and Queue. Set either this or STORAGE-WORDLIST."
	},
	"STORAGE-WORDLIST": {
		"value": "",
		"required": "false",
        "description":"Wordlist of storages to test as Blob, File Server, Data Table and Queue. Set either this or STORAGE-NAME."
	},
	"VERBOSITY": {
		"value": "True",
		"required": "true",
        "description": "If set to true, it will show you all the storage if the storage has Private, Blob or Container Access Policy. If set to false, will only list PUBLIC and PRIVATE buckets."
	}
}
description = "Description of your Module"

aws_command = "None"

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

def check_blob():
	print()

def check_table():
	print()

def check_queue():
	print()

def check_file(storage_dns):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((storage_dns, 445))
		s.close()
		return "OPEN"

	except socket.error:
		return "CLOSED"

def exploit(workspace):
	n_tab = 0
	global output

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_ec2_enum_instances".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	json_data = {}
	response = []

	storage_types = [
		"blob",
		"table",
		"queue",
		"file"
	]

	storage_name = variables["STORAGE-NAME"]['value']
	storage_wordlist = variables["STORAGE-WORDLIST"]['value']

	if storage_wordlist == "" and storage_name == "":
		print(
			colored("[*] Enter either STORAGE-NAME or STORAGE-WORDLIST. Not both, not none.", "red")
		)

	elif storage_wordlist == "" and not storage_name == "":
		for type in storage_types:
			try:
				storage_dns = "{}.{}.core.windows.net".format(storage_name, type)
				store_ip = socket.gethostbyname(storage_dns)

				json_data["IP"] = store_ip

				json_data['PORT'] = check_file(storage_dns)


				response[storage_name] = json_data
				print(
					"{}{}{}".format(
						colored("[*] Storage Account '","green"),
						colored(storage_name,"blue"),
						colored("' found! Privileges...","green")
					)
				)

			except:
				print()

	elif storage_name == "" and not storage_wordlist == "":
		print()

	else:
		print(
			colored("[*] Enter either STORAGE-NAME or STORAGE-WORDLIST. Not both, not none.", "red")
		)

	if len(json_data) > 0:
		with open(filename, 'w') as outfile:
			json.dump(json_data, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

		title_name = ""
		if isinstance(json_data, list):
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			for data in json_data:
				output += colored("{}: {}\n".format(title_name, data[title_name]), "yellow", attrs=['bold'])
				list_dictionary(data, n_tab)
				output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		else:
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
			output += colored("{}: {}\n".format(title_name, json_data[title_name]), "yellow", attrs=['bold'])
			list_dictionary(json_data, n_tab)
			output += colored("---------------------------------\n", "yellow", attrs=['bold'])
		pipepager(output, "less -R")