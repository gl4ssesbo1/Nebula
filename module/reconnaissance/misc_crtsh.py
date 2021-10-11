from termcolor import colored
from datetime import datetime
from pydoc import pipepager
from crtsh import crtshAPI
import json

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
	"DOMAIN": {
		"value": "",
		"required": "true",
        "description":"The domain to search for"
	},
	"GENERATE-LIST": {
		"value": "False",
		"required": "false",
        "description":"if set to True, it will get all the domain names from name_value, filter duplicates and generate a wordlist of dns names."
	}
}
description = "Checks for subdomains of the domain by enumerating certificates from crt.sh"

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

def exploit(workspace):
	n_tab = 0
	global output

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_misc_crtsh".format(dt_string)
	dfile = "{}_dns_file".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	domain = variables['DOMAIN']['value']
	json_data = crtshAPI().search(domain)
	for certs in json_data:
		nv = (certs['name_value']).split("\n")
		certs['name_value'] = nv

	yn = variables['GENERATE-LIST']['value']
	if not yn == "":
		if not yn.lower() == 'true' and not yn.lower() == 'false':
			print(
				colored("[*] 'GENERATE-LIST' should be either True or False.")
			)
		elif yn.lower() == 'true':
			dns_names = []
			for cert in json_data:
				for dns in cert['name_value']:
					dns_names.append(dns)
			uniquedns = set(dns_names)
			dns_list = list(uniquedns)
			dfilename = "./workspaces/{}/{}".format(workspace, dfile)
			dnsfile = open(dfilename, "w")
			for dns in dns_list:
				dnsfile.write(dns+"\n")
			dnsfile.close()
			print(colored("[*] DNS List saved on '{}'.".format(dfilename), "green"))

	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4, default=str)
		print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	for data in json_data:
		output += colored("{}: {}\n".format("Common Name", data["common_name"]), "yellow", attrs=['bold'])
		list_dictionary(data, n_tab)
		output += colored("---------------------------------\n", "yellow", attrs=['bold'])
	pipepager(output, "less -R")
	output = ""