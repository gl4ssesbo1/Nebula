from termcolor import colored
from datetime import datetime
from pydoc import pipepager
import sys
import json
import re
import socket
import ipaddress
from __ip_source.AWS_IP_Ranges import AWS_IP_RANGE

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
	"IP-FILE": {
		"value": "",
		"required": "false",
        "description":"The path of the file with the IPs (IPv4 and IPv6) or Domain Name to test."
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

	IPv4_REGEX = "^[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}$"

	IPv6_REGEX = "^([0-9a-fA-F]{1,4}[:]{0,2}){1,8}$"

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	file = "{}_aws_find_ip_category".format(dt_string)
	filename = "./workspaces/{}/{}".format(workspace, file)

	ip_file = variables['IP-FILE']['value']

	ipv4 = []
	ipv6 = []
	domain = []
	domain_ip = {}

	try:
		ipfile = open(ip_file, 'r')
		json_data = {}

		for ip in ipfile.readlines():
			if re.match(IPv4_REGEX, ip.strip()):
				ipv4.append(ip.strip())
			elif re.match(IPv6_REGEX, ip.strip()):
				ipv6.append(ip.strip())
			else:
				domain.append(ip.strip())

		if domain:
			for d in domain:
				try:
					resolved_domain = socket.gethostbyname(d)
					domain_ip[d] = resolved_domain
				except socket.gaierror:
					print(colored("[*] Domain '{}' is not resolvable.".format(d), "red"))

		if domain_ip:
			for dom,ip in domain_ip.items():
				an_address = ipaddress.ip_address(ip)
				for ip4 in AWS_IP_RANGE['prefixes']:
					a_network = ipaddress.ip_network(ip4['ip_prefix'])
					if an_address in a_network:
						service = ip4['service']
						if json_data.get(service) is None:
							json_data[service] = []

						data = {}
						data['domain'] = dom
						data['IP'] = ip
						data['ip_prefix'] = ip4['ip_prefix']
						data['region'] = ip4['region']
						data['network_border_group'] = ip4['network_border_group']
						(json_data[service]).append(data)
						continue

				for ip6 in AWS_IP_RANGE['ipv6_prefixes']:
					a_network = ipaddress.ip_network(ip6['ipv6_prefix'])

					if an_address in a_network:
						service = ip6['service']
						if json_data.get(service) is None:
							json_data[service] = []

						data = {}
						data['IP'] = ip
						data['domain'] = dom
						data['ip_prefix'] = ip6['ipv6_prefix']
						data['region'] = ip6['region']
						data['network_border_group'] = ip6['network_border_group']
						(json_data[service]).append(data)
						continue
			del ip

		if ipv4:
			for ip in ipv4:
				an_address = ipaddress.ip_address(ip)
				for ip4 in AWS_IP_RANGE['prefixes']:
					a_network = ipaddress.ip_network(ip4['ip_prefix'])

					if an_address in a_network:
						service = ip4['service']
						if json_data.get(service) is None:
							json_data[service] = []

						data = {}
						data['IP'] = ip
						data['ip_prefix'] = ip4['ip_prefix']
						data['region'] = ip4['region']
						data['network_border_group'] = ip4['network_border_group']
						(json_data[service]).append(data)
						continue
			del ip
		ip = ""
		key = ""
		service = ""
		if ipv6:
			for ip in ipv6:
				an_address = ipaddress.ip_address(ip)
				for ip6 in AWS_IP_RANGE['ipv6_prefixes']:
					a_network = ipaddress.ip_network(ip6['ipv6_prefix'])

					if an_address in a_network:
						service = ip6['service']
						if json_data.get(service) is None:
							json_data[service] = []

						data = {}
						data['IP'] = ip
						data['ip_prefix'] = ip6['ipv6_prefix']
						data['region'] = ip6['region']
						data['network_border_group'] = ip6['network_border_group']
						(json_data[service]).append(data)
						continue
			del ip


		key = service = ip = ""

		for service, ips in json_data.items():
			print(colored("------------------------------", "yellow"))
			print(colored(service, "yellow"))
			print(colored("------------------------------", "yellow"))

			for ip in ips:
				if 'domain' in ip:
					print("\t{} | {} | {} | {}".format(
						colored(ip['IP'], "red"),
						colored(ip['region'], "blue"),
						colored(ip['ip_prefix'], "green"),
						colored(ip['domain'], "yellow"),
					))
				else:
					print("\t{} | {} | {} |".format(
						colored(ip['IP'], "red"),
						colored(ip['region'], "blue"),
						colored(ip['ip_prefix'], "green"),
					))


		with open(filename, 'w') as outfile:
			json.dump(json_data, outfile, indent=4, default=str)
			print(colored("[*] Content dumped on file '{}'.".format(filename), "green"))

	except:
		e = sys.exc_info()[1]
		print(colored("[*] {}".format(e), "red"))