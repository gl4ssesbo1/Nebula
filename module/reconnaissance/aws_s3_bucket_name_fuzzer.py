from termcolor import colored
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from pydoc import pipepager
import sys

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
	"SERVICE": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"BUCKET":{
		"value":"",
		"required":"false",
        "description":"A single bucket or several buckets spearated by comma."
	},
	"WORDLIST":{
		"value":"",
		"required":"false",
        "description":"The wordlist of buckets."
	},
	"REGION":{
		"value":"",
		"required":"true",
        "description":"The region to test the buckets."
	},
	"VERBOSITY":{
		"value":"false",
		"required":"false",
        "description":"If set to true, it will show you all the buckets if they are PUBLIC, PRIVATE or NOT-EXISTANT. If set to false, will only list PUBLIC and PRIVATE buckets."
	}
}

description = "Gets the name of a bucket or a list of buckets separated by comma (',') or a wordlist of the bucket name and bruteforces the name of the bucket by sending a request to https://<bucketname>.s3.<region>.amazonaws.co. The xml files will be saved on ./workspaces/<workspace>/<datetime>_buckets>/<bucketname>.xml"

aws_command = "No awscli command"

def exploit(workspace):
	objects = {}
	try:
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		filen = "{}_buckets".format(dt_string)
		if not os.path.exists(filen):
			os.makedirs("./workspaces/{}/{}".format(workspace,filen))

	except:
		print("file error")

	print()

	if variables['BUCKET']['value'] == "" and variables['WORDLIST']['value'] != "":
		file = open(variables['WORDLIST']['value'], 'r')
		region = variables["REGION"]["value"]
		for buck in file.readlines():
			try:
				s3_url = "https://{0}.s3.{1}.amazonaws.com".format(buck.strip("\n"), region)
				response = urllib.request.urlopen(s3_url).read()

				filename = "./workspaces/{}/{}/{}.xml".format(workspace, filen, buck.strip("\n"))

				file = open(filename, "w")
				file.write((response.decode()).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"', ""))
				file.close()
				print(colored("[*] Bucket '{}' exists and is PUBLIC. Contents dumped on {}".format(buck.strip("\n"), filename),
							  "green"))

				tree = ET.parse(filename)
				root = tree.getroot()
				tag_keys = []
				tag_date = []
				for t in root.findall(".//Key"):
					tag_keys.append(t.text)

				for t in root.findall(".//LastModified"):
					tag_date.append(t.text)

				res = {tag_keys[i]: tag_date[i] for i, _ in enumerate(tag_date)}
				objects[buck] = res

			except urllib.error.HTTPError as e:
				if "Forbidden" in str(e):
					print(colored("[*] Bucket '{}' exists, but you need credentials for that.".format(buck.strip("\n")), "blue"))

				else:
					if variables['VERBOSITY']['value'] == 'true':
						print(colored("[*] Bucket '{}' does not exists exist.".format(buck.strip("\n")), "red", attrs=['bold']))

	elif variables['BUCKET']['value'] != "" and variables['WORDLIST']['value'] == "":
		buckets = variables['BUCKET']['value'].split(",")
		region = variables["REGION"]["value"]
		for buck in buckets:
			try:
				s3_url = "https://{0}.s3.{1}.amazonaws.com".format(buck, region)
				response = urllib.request.urlopen(s3_url).read()

				filename = "./workspaces/{}/{}/{}.xml".format(workspace, filen, buck)

				file = open(filename,"w")
				file.write((response.decode()).replace(' xmlns="http://s3.amazonaws.com/doc/2006-03-01/"',""))
				file.close()
				print(colored("[*] Bucket '{}' exists and is PUBLIC. Contents dumped on {}".format(buck, filename),
							  "green"))

				tree = ET.parse(filename)
				root = tree.getroot()
				tag_keys = []
				tag_date = []
				for t in root.findall(".//Key"):
					tag_keys.append(t.text)

				for t in root.findall(".//LastModified"):
					tag_date.append(t.text)

				res = {tag_keys[i]: tag_date[i] for i, _ in enumerate(tag_date)}
				objects[buck] = res

			except urllib.error.HTTPError as e:
				if "Forbidden" in str(e):
					print (colored("[*] Bucket '{}' exists, but you need credentials for that.".format(buck),"blue"))

				else:
					if variables['VERBOSITY']['value'] == 'true':
						print(colored("[*] Bucket '{}' does not exists exist.".format(buck), "red", attrs=['bold']))
	else:
		print(colored("[*] Add either a bucket or a wordlist of buckets.","red"))

	try:
		yn = input("Do you want to list the files on each public bucket? [y/N] ")
		if yn == 'y' or yn == 'Y':
			output = ""
			for key, value in objects.items():
				output += (
					"{} {}\n".format(colored("\tFiles in Bucket", "yellow", attrs=['bold']), colored(key, "yellow")))
				output += (colored("\t------------------------------------------\n", "yellow", attrs=['bold']))
				for k, v in value.items():
					output += ("\t\t{}:\t{}\n".format(colored(k, "red"), colored(v, "yellow")))
				output += (colored("\t------------------------------------------\n", "yellow", attrs=['bold']))
			pipepager(output, 'less -R')
	except:
		e = sys.exc_info()[1]
		print(colored("[*] {}".format(e), "red"))