#!/usr/bin/python3

import boto3
import sys
import banner
import os
import argparse
from termcolor import colored
import help
import textwrap
import json
import copy
import botocore
import random
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from colorama import init
import re
from datetime import datetime
import string
from pydoc import pipepager
import platform

path = os.getcwd() + '\\less_binary'

command = "powershell.exe -c '$env:Path = " + path + " + ;$env:Path'"
os.popen(command)

init()

parser = argparse.ArgumentParser()
parser.add_argument("-b", action='store_true', help="Do not print banner")
args = parser.parse_args()

if args.b:
	print(colored("-------------------------------------------------------------","green"))
	banner.module_count_without_banner()
	print(colored("-------------------------------------------------------------\n","green"))
else:
	banner.banner()

particles = [
	{
		"Name": "dnsdwwad",
		"IP":"1.1.1.1",
		"Hostname":"host",
		"LAN IP":"192.168.1.1",
		"Port":"65000",
		"OS": "Linux",
		"User": "host/glb"
	}
]

system = platform.system()

all_sessions = [
]

#all_sessions = []
session = {}
sess_test = {}

show = [
	'cleanup',
	'detection',
	'detectionbypass',
	'enum',
	'exploit',
	'lateralmovement',
	'listeners',
	'persistence',
	'privesc',
	'reconnaissance',
	'stager'
]

def enter_credentials(service, access_key_id, secret_key, region):
	return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

def enter_credentials_with_session_token(service, access_key_id, secret_key, region, session_token):
	return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key, aws_session_token=session_token)

def enter_credentials_with_session_token_and_user_agent(service, access_key_id, secret_key, region, session_token, ua):
	session_config = botocore.config.Config(user_agent=ua)
	return boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key, aws_session_token=session_token, config=session_config)

def enter_credentials_with_user_agent(service, access_key_id, secret_key, region, ua):
	session_config = botocore.config.Config(user_agent=ua)
	return boto3.client(service, config=session_config, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

def enter_session(session_name, region, service):
	boto_session = boto3.session.Session(profile_name=session_name, region_name=region)
	return boto_session.client(service)

def main():
	cred_prof = ""
	module_char = ""
	terminal = colored("AWS",'yellow')
	particle = ""

	sess_token = ""

	useragent = ""
	user_agents_windows = [
		'Boto3/1.7.48 Python/3.9.1 Windows/10 Botocore/1.10.48',
		'Boto3/1.7.48 Python/3.8.1 Windows/10 Botocore/1.10.48',
		'Boto3/1.7.48 Python/2.7.0 Windows/10 Botocore/1.10.48',
		'Boto3/1.7.48 Python/3.9.1 Windows/8 Botocore/1.10.48',
		'Boto3/1.7.48 Python/3.8.1 Windows/8 Botocore/1.10.48',
		'Boto3/1.7.48 Python/2.7.0 Windows/8 Botocore/1.10.48',
		'Boto3/1.7.48 Python/3.9.1 Windows/7 Botocore/1.10.48',
		'Boto3/1.7.48 Python/3.8.1 Windows/7 Botocore/1.10.48',
		'Boto3/1.7.48 Python/2.7.0 Windows/7 Botocore/1.10.48'
	]
	user_agents_linux = [
		'Boto3/1.9.89 Python/2.7.12 Linux/4.1.2-34-generic',
		'Boto3/1.9.89 Python/3.8.1 Linux/4.1.2-34-generic',
		'Boto3/1.9.89 Python/3.9.1 Linux/5.9.0-34-generic'
	]

	workspaces = []
	workspace = ""

	allmodules = []
	for module in show:
		arr = os.listdir("./module/" + module)
		for x in arr:
			if "__" in x:
				continue
			elif ".git" in x:
				continue
			else:
				mod = "{}/{}".format(module,x.split(".py")[0])
				allmodules.append(mod)

	comms = {
		"show":{
			"credentials": None,
			"workspaces": None,
			"modules": None,
			"user-agent":None,
			"current-creds": None,
		},
		"search":None,
		"exit":None,
		"use":{
			"credentials":{},
			"workspace": {},
			"module": WordCompleter(
				words=(allmodules),
				pattern=re.compile(r'([a-zA-Z0-9_\\/]+|[^a-zA-Z0-9_\s]+)')
                                ),
		},
		"create": {
			"workspace": None
		},
		"set": {
			"credentials": None,
			"user-agent": {
				"linux":None,
				"windows":None,
				"custom":None
			}
		},
		"help":None,
		"help": {
			"workspace":None,
			"user-agent":None,
			"module":None,
			"credentials": None
		},
		"options": None,
		"back": None,
		"remove":{
			"workspace": {},
			"credentials": {},
		},
		"run": None,
		"unset": {
			"user-agent":None
		},
		"dump": {
			"credentials": None,
		},
		"import": {
			"credentials": {},
		},

	}
	for c in show:
		comms['show'][c] = None

	for c in all_sessions:
		comms['use']['credentials'][c['profile']] = None

	for c in all_sessions:
		comms['remove']['credentials'][c['profile']] = None
	
	if not os.path.isdir('./credentials/'):
		os.mkdir('./credentials/')
		
	arr = os.listdir("./credentials/")
	for x in arr:
		if "__" in x:
			continue
		elif ".git" in x:
			continue
		else:
			comms['import']['credentials'][x] = None

	if not os.path.isdir('./workspaces/'):
		os.mkdir('./workspaces/')
	
	arr = os.listdir("./workspaces/")
	for x in arr:
		if "__" in x:
			continue
		elif ".git" in x:
			continue
		else:
			workspaces.append(x)
	for x in workspaces:
		comms['remove']['workspace'][x] = None
		comms['use']['workspace'][x] = None

	completer = NestedCompleter.from_nested_dict(comms)

	com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

	try:
		history_file = FileHistory(".nebula-history-file")
		session = PromptSession(history=history_file)
		command = session.prompt(
			ANSI(
				com
			),
			completer=completer,
			complete_style=CompleteStyle.READLINE_LIKE
		)

		while (True):
			if command == None or command == "":
				com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

				for x in workspaces:
					comms['remove']['workspace'][x] = None
				completer = NestedCompleter.from_nested_dict(comms)
				history_file = FileHistory(".nebula-history-file")
				session = PromptSession(history=history_file)
				command = session.prompt(
					ANSI(
						com
					),
					completer=completer,
					complete_style=CompleteStyle.READLINE_LIKE
				)

			elif command == 'exit':
				command = session.prompt(
					ANSI(
						colored("Are you sure? [y/N] ","red")
					)
				)
				if command == "Y" or command == "y":
					exit()

			elif command == 'help':
				help.help()

			elif len(command.split(" ")) > 1 and command.split(" ")[0] == 'help':
				help_comm = command.split(" ")[1]
				help.specific_help(help_comm)

			elif command == "create":
				print("{} {}".format(colored("[*] The exact command is:", "red"), colored("create wordspace <workspace name>", "yellow")))

			elif command.split(" ")[0] == "create":
				if command.split(" ")[1] == "workspace":
					if len(command.split(" ")) < 3:
						print("{} {}".format(colored("[*] The exact command is:", "red"),colored("create wordspace <workspace name>", "yellow")))

					else:
						if not os.path.exists("./workspaces"):
							os.makedirs("./workspaces")

						if not os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
							os.makedirs("./workspaces/{}".format(command.split(" ")[2]))
							workspaces.append(command.split(" ")[2])
							workspace = command.split(" ")[2]
							for x in workspaces:
								comms['remove']['workspace'][x] = None
							completer = NestedCompleter.from_nested_dict(comms)
							print(colored("[*] Workspace '"+(command.split(" ")[2])+"' created.","green"))
							print(colored("[*] Current workspace set at '"+(command.split(" ")[2])+"'.", "green"))
						else:
							print(colored("[*] The workspace already exists. Either use it, remove it, or create a different one.", "red"))

			elif command == "search":
				print(colored("[*] Enter a pattern to search! Eg: search s3", "red"))

			elif command.split(" ")[0] == 'search':
				arr = os.listdir("./module/")
				search_dir = []
				for x in arr:
					if "__" in x:
						continue
					elif ".git" in x:
						continue
					elif os.path.isdir("./module/{}".format(x)):
						dir = os.listdir("./module/{}/".format(x))
						for y in dir:
							if not os.path.isdir(y):
								if "__" in y:
									continue
								elif ".git" in y:
									continue
								else:
									search_dir.append(x+"/"+(y.split(".py")[0]).split(".")[0])
					else:
						continue
				List = []
				list2 = []
				for x in search_dir:
					if command.split(" ")[1] in x:
						thedir = x.split("/")[0]
						sys.path.insert(0, "./module/" + thedir)
						imported_module = __import__(x.split("/")[1])
						list2.append("\t{}".format(colored(x, "blue")))
						list2.append("\t{}".format(colored(imported_module.description, "yellow")))
						List.append(list2)
						list2 = []

				indention = 80
				max_line_length = 60

				for i in range(len(List)):
					out = List[i][0].ljust(indention, ' ')
					cur_indent = 0
					for line in List[i][1].split('\n'):
						for short_line in textwrap.wrap(line, max_line_length):
							out += ' ' * cur_indent + short_line.lstrip() + "\n"
							cur_indent = indention
						print(out)

			elif command == 'back':
				module_char = ""
				terminal = colored("AWS",'yellow')

			elif command == "use":
				print(colored("[*] Enter a module to use! ", "red"))

			elif command.split(" ")[0] == 'use':
				if command.split(" ")[1] == 'credentials':
					if len(command.split(" ")) == 3:
						for sess in all_sessions:
							if sess['profile'] == command.split(" ")[2]:
								cred_prof = command.split(" ")[2]
								print(colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored("Use ","green") + colored("'show current-creds' ","blue") + colored("to check them.","green"))

				elif command.split(" ")[1] == 'particle':
					if not len(command.split(" ")) == 3:
						print(colored("[*] Usage: use particles <name of particle>", "red"))
					else:
						par_test = 1
						for par in particles:
							if par['Name'] == command.split(" ")[2]:
								particle = par['Name']
								par_test = 0
						if par_test == 1:
							print(colored("[*] No session named: {}".format(command.split(" ")[1]), "red"))

				elif command.split(" ")[1] == "workspace":
					for x in workspaces:
						comms['remove']['workspace'][x] = None
					completer = NestedCompleter.from_nested_dict(comms)
					if len(command.split(" ")) < 3:
						print("{} {}".format(colored("[*] The exact command is:", "red"),colored("use wordspace <workspace name>", "yellow")))

					else:
						if len(workspaces) == 0:
							print(colored("[*] There are no workspaces configured", "red"))
						else:
							right = 0
							for w in workspaces:
								if w == command.split(" ")[2]:
									workspace = w
									right = 1

								if right == 0:
									print(colored("[*] The workstation name is wrong.", "red"))

				elif command.split(" ")[1] == 'module':
					if not "/" in command.split(" ")[2]:
						print(colored("[*] Exact module format is <type>/<name>. Eg: use module enum/s3_list_buckets","red"))

					else:
						try:
							thedir = (command.split(" ")[2]).split("/")[0]
							#thedir = "./" + (command.split(" ")[2]).split("/")[0]
							sys.path.insert(0, "./module/" + thedir)
							terminal = colored(command.split(" ")[2], "blue")
							module_char = (command.split(" ")[2]).split("/")[1]
							imported_module = __import__(module_char)
							comms['set'] = {
								"credentials":None
							}
							comms['unset'] = {}
							for c,v in imported_module.variables.items():
								if c == 'SERVICE':
									pass
								else:
									comms['set'][c] = None
									comms['unset'][c] = None
							completer = NestedCompleter.from_nested_dict(comms)

						except(ModuleNotFoundError):
							print(colored("[*] Module does not exist","red"))
							terminal = colored("AWS",'yellow')
							module_char = ""

			elif command.split(" ")[0] == 'remove':
				if command.split(" ")[1] == 'credentials':
					if len(command.split(" ")) == 2:
						command = input(colored("You are about to remove all credentials. Are you sure? [y/N] ","red"))
						if command == "Y" or command == "y":
							all_sessions.clear()
							print(colored("[*] All credentials removed.", "yellow"))

					elif len(command.split(" ")) == 3:
						if command.split(" ")[2] == "" or command.split(" ")[2] == None:
							for sess in all_sessions:
								if sess['profile'] == "":
									command = input(colored("You are about to remove credential '{}'. Are you sure? [y/N] ".format(sess['profile']),"red"))
									if command == "Y" or command == "y":
										all_sessions.remove(sess)
										print(colored("[*] Credential '{}' removed.".format(sess['profile']), "yellow"))

						else:
							for sess in all_sessions:
								if sess['profile'] == command.split(" ")[2]:
									command = input(colored("You are about to remove credential '{}'. Are you sure? [y/N] ".format(sess['profile']),"red"))
									if command == "Y" or command == "y":
										all_sessions.remove(sess)

					else:
						print(colored("[*] Set the credential profile to remove.", "red"))

				elif command.split(" ")[1] == "workspace":
					if len(command.split(" ")) < 3:
						print("{} {}".format(colored("[*] The exact command is:", "red"), colored("remove wordspace <workspace name>", "yellow")))

					else:
						if os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
							yo = input(colored("[*] Are you sure you want to delete the workspace? [y/N] ","red"))
							if yo == 'y' or yo == 'Y':
								os.rmdir("./workspaces/{}".format(command.split(" ")[2]))
								workspaces.remove(command.split(" ")[2])
						else:
							print(colored("[*] The workstation name is wrong.", "red"))

			elif command.split(" ")[0] == 'run':
				if module_char == "":
					print(colored("[*] Choose a module first.","red"))

				else:
					if workspace == "":
						history_file = FileHistory(".nebula-history-file")
						session = PromptSession(history=history_file)
						letters = string.ascii_lowercase
						w = ''.join(random.choice(letters) for i in range(8))
						command = session.prompt(
							ANSI(
								colored("A workspace is not configured. Workstation '" + w + "' will be created. Are you sure? [y/N] ", "red")
							)
						)
						if command == "Y" or command == "y":
							if not os.path.exists("./workspaces"):
								os.makedirs("./workspaces")

							if not os.path.exists("./workspaces/{}".format(command.split(" ")[2])):
								os.makedirs("./workspaces/{}".format(command.split(" ")[2]))
								workspaces.append(command.split(" ")[2])
							else:
								print(colored(
									"[*] The workspace already exists. Either use it, remove it, or create a different one.",
									"red"))

					if not workspace == "":
						count = 0
						for key, value in imported_module.variables.items():
							if value['required'] == 'true' and value['value'] == "":
								print(colored("[*] Option '{}' is not set!".format(key), "red"))
								count += 1

						for sess in all_sessions:
							if sess['profile'] == cred_prof:
								for key,value in sess.items():
									if key == 'session_token':
										continue

									if value == "":
										print (colored("[*] Credential '{}' not set yet!".format(key),"red"))
										count = count + 1

						if count == 0:
							try:
								service = imported_module.variables['SERVICE']['value']
								if imported_module.needs_creds:
									for sess in all_sessions:
										if sess['profile'] == cred_prof:
											if not 'session_token' in sess:
												if not useragent == "":
													profile_v = enter_credentials_with_user_agent(service,
																								  sess['access_key_id'],
																								  sess['secret_key'],
																								  sess['region'],
																								  useragent
																								  )
													imported_module.exploit(profile_v, workspace)

												else:
													profile_v = enter_credentials(service,
																				  sess['access_key_id'],
																				  sess['secret_key'],
																				  sess['region']
																				  )
													imported_module.exploit(profile_v, workspace)
											elif 'session_token' in sess and sess['session_token'] != "":
												if not useragent == "":
													profile_v = enter_credentials_with_session_token(service,
																							sess['access_key_id'],
																							sess['secret_key'],
																							sess['region'],
																							sess['session_token']
																							)
													imported_module.exploit(profile_v, workspace)
												else:
													profile_v = enter_credentials_with_session_token_and_user_agent(service,
																								  sess['access_key_id'],
																								  sess['secret_key'],
																								  sess['region'],
																								  sess['session_token'],
																								  useragent)
													imported_module.exploit(profile_v, workspace)
											else:
												print(colored("[*] Check if the session key is empty.","yellow"))
								else:
									imported_module.exploit(workspace)

							except:
								e = sys.exc_info()[1]
								print(colored("[*] {}".format(e), "red"))
								print (colored("[*] Either a Connection Error or you don't have permission to use this module. Please check internet or credentials provided.'", "red"))

					else:
						print(colored(
							"[*] Create a workstation first using 'create workstation <workstation name>'.",
							"red"))

			elif command.split(" ")[0] == "shell":
				if not particle:
						print(colored("[*] You need to have or choose a session first. To choose a session, enter 'use particle <session name>'.", "red"))

				else:
					if len((command).split(" ")) == 1:
						print(colored(
								"[*] Enter a command to run on the remote system. Eg: 'shell <command>'", "red"))
					else:
						print(command.split(" ")[0])

					#elif len(command.split(" ")) > 2:
					#	sess_command = ""
					#	for c in command.split(" "):
					#		sess_command += c
					#		sess_command += " "
							#shell.write(sess_command)
							#print(shell.read())

					#else:
					#	shell.write(command.split(" ")[1])
					#	print(shell.read())

			elif command.split(" ")[0] == "options":
				if module_char == "":
					print(colored("[*] Choose a module first.","red"))

				else:
					print (colored("Desctiption:","yellow",attrs=["bold"]))
					print (colored("-----------------------------","yellow",attrs=["bold"]))
					print (colored("\t{}".format(imported_module.description),"green"))

					print(colored("\nAuthor:", "yellow", attrs=["bold"]))
					print(colored("-----------------------------", "yellow", attrs=["bold"]))
					for x, y in imported_module.author.items():
						print("\t{}:\t{}".format(colored(x, "red"), colored(y, "blue")))

					print()
					print("{}: {}".format(colored("Needs Credentials", "yellow", attrs=["bold"]),
										  colored(imported_module.needs_creds, "green")))
					print(colored("-----------------------------", "yellow", attrs=["bold"]))

					print(colored("\nAWSCLI Command:", "yellow", attrs=["bold"]))
					print(colored("---------------------"
								  "--------", "yellow", attrs=["bold"]))
					aws_comm = imported_module.aws_command
					print("\t" + aws_comm)

					print(colored("\nOptions:", "yellow", attrs=["bold"]))
					print(colored("-----------------------------","yellow",attrs=["bold"]))
					for key,value in imported_module.variables.items():
						if (value['required']).lower() == "true":
							print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

						elif (value['required']).lower() == "false":
							print("\t{}:\t{}\n\t\t{}: {}\n\t\t{}: {}".format(colored(key,"red"),colored(value['value'],"blue"),colored("Required","yellow"), colored(value['required'],"green"), colored("Description","yellow"), colored(value['description'],"green")))

						else:
							print("\t{}:\t{}".format(colored(key, "red"), colored(value['value'], "blue")))
						print()

			elif command == 'set':
				print(colored("Option 'set' is used with another option. Use help for more.","red"))

			elif command.split(" ")[0] == 'set':
				if command.split(" ")[1] == 'credentials':
					profile_name = ""
					if len(command.split(" ")) == 2:
						profile_name = input("Profile Name: ")
					elif len(command.split(" ")) > 2:
						print("Profile Name: {}".format(command.split(" ")[2]))
						profile_name = command.split(" ")[2]

					access_key_id = input("Access Key ID: ")
					secret_key = input("Secret Key ID: ")
					region = input("Region: ")

					sess_test['profile'] = str(profile_name)
					sess_test['access_key_id'] = str(access_key_id)
					sess_test['secret_key'] = str(secret_key)
					sess_test['region'] = str(region)
					yon = input("\nDo you also have a session token?[y/N] ")
					if yon == 'y' or yon == 'Y':
						sess_token = input("Session Token: ")
						sess_test['session_token'] = sess_token

					comms['use']['credentials'][profile_name] = None

					if sess_test['profile'] == "" and sess_test['access_key_id'] == "" and sess_test['secret_key'] == "" and sess_test['region'] == "":
						pass

					else:
						cred_prof = sess_test['profile']
						all_sessions.append(copy.deepcopy(sess_test))

					print (colored("[*] Credentials set. Use ","green") + colored("'show credentials' ","blue") + colored("to check them.","green"))
					print(colored("[*] Currect credential profile set to ", "green") + colored("'{}'.".format(cred_prof), "blue") + colored("Use ","green") + colored("'show current-creds' ","blue") + colored("to check them.","green"))

				elif command.split(" ")[1] == 'user-agent':
					if len(command.split(' ')) < 3 or len(command.split('"')) > 3:
						print(colored("[*] Usage: set user-agent <linux | windows | custom>","red"))

					elif len(command.split(' ')) == 3:
						ua = command.split(' ')[2].lower()

						if ua == "linux":
							useragent = random.choice(user_agents_linux)
						elif ua == "windows":
							useragent = random.choice(user_agents_windows)
						elif ua == "custom":
							useragent = input("Enter the User-Agent you want: ")
						else:
							print(colored("[*] Usage: set user-agent <linux | windows | custom>", "red"))

						print(colored("User Agent: {} was set".format(useragent),"green"))

				else:
					if module_char == "":
						print(colored("[*] Choose a module first.","red"))

					elif len(command.split(" ")) < 3:
						print (colored("[*] The right form is: set <OPTION> <VALUE>","red"))

					elif (command.split(" ")[1]).upper() == 'SERVICE':
						print(colored("[*] You can't change service.", "red"))

					else:
						count = 1
						for key, value in imported_module.variables.items():
							argument = ((command.split(" ")[1]).upper()).strip()
							if key == argument:
								count = 0
								imported_module.variables[key]['value'] = command.split(" ")[2]
								break

						if count == 1:
							print(colored("[*] That option does not exist on this module","red"))

			elif command.split(" ")[0] == 'unset':
				if (command.split(" ")[1]).lower() == 'user-agent':
					useragent = ""
					print(colored("[*] User Agent set to empty.", "green"))

				else:
					if module_char == "":
						print(colored("[*] Choose a module first.","red"))

					elif len(command.split(" ")) > 2:
						print (colored("[*] The right form is: unset <OPTION>","red"))

					elif (command.split(" ")[1]).upper() == 'SERVICE':
						print(colored("[*] You can't change service.", "red"))

					else:
						count = 1
						for key, value in imported_module.variables.items():
							argument = ((command.split(" ")[1]).upper()).strip()
							if key == argument:
								count = 0
								imported_module.variables[key]['value'] = ""
								break

						if count == 1:
							print(colored("[*] That option does not exist on this module","red"))

			elif command.split(" ")[0] == 'show':
				if command.split(" ")[1] == 'credentials':
					print(json.dumps(all_sessions, indent=4, default=str))

				# Ongoing
				elif command.split(" ")[1] == 'particles':
					if not particles:
						print(colored("[*] You have no current sessions!\n", "yellow"))
					else:
						c = 0
						print(colored("--------------------------------------------------------------------------------------------", "yellow"))
						for part in particles:
								print("Session {} | {} | {} | {} | {} | {} | {} | {} |".format(
									colored(c, "blue"),
									colored(part['Name'], "red"),
									colored(part['IP'], "yellow"),
									colored(part['Hostname'], "yellow"),
									colored(part['LAN IP'], "green"),
									colored(part['Port'], "magenta"),
									colored(part['OS'], "cyan"),
									colored(part['User'], "yellow")
								))
								if c < (len(particles) - 1):
									print()
								c += 1
						print(colored("--------------------------------------------------------------------------------------------", "yellow"))

				elif command.split(" ")[1] == "workspaces":
					print(colored("-----------------------------------", "yellow"))
					print("{}:".format(colored("Workspaces", "yellow")))
					print(colored("-----------------------------------", "yellow"))
					for w in workspaces:
						print("\t{}".format(w))
					print()

				elif (command.split(" ")[1]).lower() == 'user-agent':
					if useragent == "":
						print("{}".format(colored("[*] User Agent is empty.", "green")))
					else:
						print("{}: {}".format(colored("[*] User Agent is", "green"), colored(useragent, "yellow")))

				elif command.split(" ")[1] == 'current-creds':
					for sess in all_sessions:
						if sess['profile'] == cred_prof:
							print(json.dumps(sess, indent=4, default=str))

				elif command.split(" ")[1] == 'modules':
					for module in show:
						arr = os.listdir("./module/" + module)
						for x in arr:
							if "__" in x:
								continue
							elif ".git" in x:
								continue
							else:
								List = []
								list2 = []
								indention = 80
								max_line_length = 60

								mod = module + "/" + x.split(".py")[0]
								thedir = mod.split("/")[0]
								sys.path.insert(0, "./module/" + thedir)
								imported_module = __import__(mod.split("/")[1])
								list2.append("\t{}".format(colored(mod, "blue")))
								list2.append("\t{}".format(colored(imported_module.description, "yellow")))
								List.append(list2)

								for i in range(len(List)):
									out = List[i][0].ljust(indention, ' ')
									cur_indent = 0
									for line in List[i][1].split('\n'):
										for short_line in textwrap.wrap(line, max_line_length):
											out += ' ' * cur_indent + short_line.lstrip() + "\n"
											cur_indent = indention
										print(out)

								List = []
								list2 = []


				elif command.split(" ")[1] in show:
					terminal = colored(command.split(" ")[1],"blue")
					arr = os.listdir("./module/" + command.split(" ")[1])
					for x in arr:
						if "__" in x:
							continue
						elif ".git" in x:
							continue
						else:
							List = []
							list2 = []
							indention = 80
							max_line_length = 60

							mod = command.split(" ")[1] + "/" + x.split(".py")[0]
							thedir = mod.split("/")[0]
							if "\\" in thedir:
								thedir = thedir.replace("\\","/")
							sys.path.insert(0, "./module/" + thedir)
							imported_module = __import__(mod.split("/")[1])
							list2.append("\t{}".format(colored(mod, "blue")))
							list2.append("\t{}".format(colored(imported_module.description, "yellow")))
							List.append(list2)

							for i in range(len(List)):
								out = List[i][0].ljust(indention, ' ')
								cur_indent = 0
								for line in List[i][1].split('\n'):
									for short_line in textwrap.wrap(line, max_line_length):
										out += ' ' * cur_indent + short_line.lstrip() + "\n"
										cur_indent = indention
									print(out)
							List = []
							list2 = []
							out = ""
				else:
					print (colored("[*] '{}' is not a valid command".format(command.split(" ")[1]), "red"))

			elif command.split(" ")[0] == 'dump':
				if len(command.split(" ")) < 2:
					print(colored("[*] Correct command is 'dump credentials'", "red"))

				if command.split(" ")[1] == 'credentials':
					if not all_sessions:
						print(colored("[*] You have no credentials at the moment. Pease add some first, then save them latter.", "red"))
					else:
						now = datetime.now()
						dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
						if not os.path.exists('./credentials'):
							os.makedir('./credentials')

						with open("./credentials/{}".format(dt_string), 'w') as outfile:
							json.dump(all_sessions, outfile)
							print(colored("[*] Credentials dumped on file '{}'.".format("./credentials/{}".format(dt_string)), "green"))
				else:
					print(colored("[*] Correct command is 'dump credentials'", "red"))

			elif command.split(" ")[0] == 'import':
				if command.split(" ")[1] == 'credentials':
					if len(command.split(" ")) < 3:
						print(colored("[*] Usage: import credentials <cred name>","red"))
					else:
						if "/" in command.split(" ")[2] or "\\" in command.split(" ")[2]:
							print(colored("[*] Just enter the credential file name, not the whole path. That being said, no \\ or / should be on the file name.","red"))
						else:	
							with open("./credentials/{}".format(command.split(" ")[2]), 'r') as outfile:
								sessions = json.load(outfile)
								for s in sessions:
									name = s['profile']
									comms['use']['credentials'][name] = None
									all_sessions.append(s)

				else:
					print(colored("[*] Correct command is 'import credentials'.", "red"))

			elif command == 'getuid':
				print()

			else:
				try:
					if system == 'Windows':
						command = "powershell.exe " + command
						out = os.popen(command).read()
						print(out)
					elif system == 'Linux' or system == 'Darwin':
						out = os.popen(command).read()
						print(out)
				except:
					print (colored("[*] '{}' is not a valid command.".format(command), "red"))

			com = "({})({})({}) >>> ".format(colored(workspace,"green"),colored(particle,"red"), terminal)

			history_file = FileHistory(".nebula-history-file")
			session = PromptSession(history=history_file)
			for x in workspaces:
				comms['remove']['workspace'][x] = None
			completer = NestedCompleter.from_nested_dict(comms)
			command = session.prompt(
				ANSI(
					com
				),
				completer=completer,
				complete_style=CompleteStyle.READLINE_LIKE
			)
	except KeyboardInterrupt:
		command = session.prompt(
			ANSI(
				colored("Are you sure you want to exit? [y/N] ","red")
			)
		)
		if command == "Y" or command == "y":
			exit()
		main()

if __name__ == "__main__":
	main()
