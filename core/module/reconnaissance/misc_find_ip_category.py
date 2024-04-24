from termcolor import colored
from datetime import datetime
from pydoc import pipepager
import sys
import json
import re
import socket
import ipaddress
from __ip_source.AWS_IP_Ranges import AWS_IP_RANGE
from __ip_source.Azure_IP_Ranges import AZURE_IP_RANGE
from __ip_source.GCP_IP_Ranges import GCP_IP_RANGE
from __ip_source.DOIPRange import DOIPRange

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
	"IP-FILE": {
		"value": "",
		"required": "false",
		"description": "The path of the file with the IPs (IPv4 and IPv6) or Domain Name to test."
	}
}
description = "Checks for subdomains of the domain by enumerating certificates from crt.sh"
aws_command = "None"

all_hosts = {
	"resolved": {
		"ipv4": {},
		"ipv6": {},
		"domain": {}
	},
	"unresolved": {
		"domain": {}
	},
}


def exploit(workspace):
	split_by_services = {
		"Services": {

		}
	}

	IPv4_REGEX = "^[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}$"
	IPv6_REGEX = "^([0-9a-fA-F]{1,4}[:]{0,2}){1,8}$"

	ip_file = variables['IP-FILE']['value']
	split_by_services['IP-FILE'] = ip_file
	all_domain = []

	try:
		ipfile = open(ip_file, 'r')

		for ip in ipfile.readlines():
			if re.match(IPv4_REGEX, ip.strip()):
				(all_hosts["resolved"]['ipv4'][ip.strip()]) = {}

			elif re.match(IPv6_REGEX, ip.strip()):
				(all_hosts["resolved"]['ipv6'][ip.strip()]) = {}

			else:
				all_domain.append(ip.strip())

		if len(all_domain) > 0:
			for d in all_domain:
				try:
					resolved_domain = socket.gethostbyname(d)
					(all_hosts["resolved"]["domain"][d]) = {
						"IP": resolved_domain
					}

				except socket.gaierror:
					(all_hosts["unresolved"]["domain"][d]) = {
							"IP": "Unresolved, Probably does not exist"
						}

		if len(all_hosts["resolved"]["domain"]) > 0:
			for key, value in (all_hosts["resolved"]["domain"]).items():
				service = find_aws_category(value['IP'], 'ip_prefix')
				(all_hosts["resolved"]["domain"][key]["Service"]) = service
				(all_hosts["resolved"]["domain"][key]["network_border_group"]) = service
				(all_hosts["resolved"]["domain"][key]["region"]) = service
				(all_hosts["resolved"]["domain"][key]["vendor"]) = "Amazon"
				thedict = value
				thedict["domain"] = key

				try:
					if not split_by_services["Services"][service]:
						split_by_services["Services"][service] = []

				except KeyError:
					split_by_services["Services"][service] = []

				(split_by_services["Services"][service]).append(thedict)

		if len(all_hosts["resolved"]['ipv4']) > 0:
			for key, value in (all_hosts["resolved"]["domain"]).items():
				service = find_aws_category(value['IP'], 'ip_prefixes')
				(all_hosts["resolved"]['ipv4'][key]["Service"]) = service
				(all_hosts["resolved"]['ipv4'][key]["network_border_group"]) = service
				(all_hosts["resolved"]['ipv4'][key]["region"]) = service
				(all_hosts["resolved"]["ipv4"][key]["vendor"]) = "Amazon"
				thedict = value
				thedict['IP'] = key

				try:
					if not split_by_services["Services"][service]:
						split_by_services["Services"][service] = []

				except KeyError:
					split_by_services["Services"][service] = []

				(split_by_services["Services"][service]).append(thedict)

		if len(all_hosts["resolved"]['ipv6']) > 0:
			for key, value in (all_hosts["resolved"]["domain"]).items():
				service = find_aws_category(value['IP'], 'ipv6_prefix')
				(all_hosts["resolved"]['ipv6'][key]["Service"]) = service
				(all_hosts["resolved"]['ipv6'][key]["network_border_group"]) = service
				(all_hosts["resolved"]['ipv6'][key]["region"]) = service
				(all_hosts["resolved"]["ipv6"][key]["vendor"]) = "Amazon"
				thedict = value
				thedict['IP'] = key

				try:
					if not split_by_services["Services"][service]:
						split_by_services["Services"][service] = []

				except KeyError:
					split_by_services["Services"][service] = []

				(split_by_services["Services"][service]).append(thedict)

		del key
		del value

		ipfile.close()

		for key in split_by_services['Services']:
			if key == None:
				del split_by_services['Services'][key]
				break

		return {
				   "IP-FILE": split_by_services
			   }, 200

	except:
		e = sys.exc_info()
		return {"error": str(e)}, 500

def find_aws_ips(ips):
	unresolved = []
	resolved = []
	return {
		"resolved": resolved,
		"unresolved": unresolved,
	}


def find_aws_category(ip, type):
	an_address = ipaddress.ip_address(ip)
	for ip4 in AWS_IP_RANGE['prefixes']:
		a_network = ipaddress.ip_network(ip4[type])
		if an_address in a_network:
			return ip4['service']


def find_azure_ips(ips):
	print()


def find_gcp_ips(ips):
	print()


def find_o365_ips(ips):
	print()

def find_do_ip(ips):
	DOIPs = []
	for ip in ips:
		an_address = ipaddress.ip_address(ip)
		for doIP in DOIPRange:
			a_network = ipaddress.ip_network(doIP['IPRange'])
			if an_address in a_network:
				DOIPs.append({"IP": ip, "Region": doIP['Region']})
	return DOIPs