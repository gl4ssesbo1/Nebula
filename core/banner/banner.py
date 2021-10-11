from termcolor import colored
from justifytext import justify
import os

def banner():
	head()
	module_count()
	disclaimer()

def head():
	print(colored("""
	                                              ...........                                                           
                                              ...''''''''''''''...                                                      
                                           ..'''''...........''''''............                                         
                                         ..''''..             ...'''''''''''''''...                                     
                                       ..'''..                   ..............'''''..                                  
                                      .''''.          .;loddool:'.              ..''''..                                
                                     ..'''.          .;clokXWWMWNKkl;.             .''''.                               
                                     .'''.      .',,'..    ';dNMMMMMWKko;.           .'''..                             
                                    .''''.   .cx0NWWNX0koc;,'cKMMMMMMMMMWXOo:.        .''''....                         
                                    .'''.   .',',:oONMMMMMWNNNWMMMMMMWKk0WMMWXx'       .''''''''...                     
                                   ..'''.          .,dXMMMMMMMMMMMMMNOl',oONWWd.        .......'''''..                  
                                ...'''''..   :o'      cXMMMMMMMMMMMMMWNXKKXNWWKxc,.             ..''''..                
                              ..''''....     oNKl'. ..oXMMMMMMMMMMMMMMMMMMMMMMMMMNKOdc,..         ..''''.               
                            ..''''..         ,OWWX0O0XWMMMMMMMMMMMMMMMMMMWWWWMMMMMMMMMWXOxooxk:.    ..'''.              
         ..'''''''''''''''''''''.             .l0NMMMMMMMMMMMMMMMMMMMMN0dc;;;coONMMMMMMMMMMMMMK:     ..'''.             
         .......................                .,dXMMMMMMMMMMMMMMMMMMWX0ko:.  .;OWMMMMMMMMMMMWx.     .'''.             
                                                  .oWMMMMMMMMMMMMMMWNXXXWMMWKd'  .:lccclodOXWMWd.      .'''.            
             ,lc'    ..................   ',.    .,OWMMMMMMMMMMMMXx:'...:0WMMMKl.      .. .'oKO,       .'''.            
            ,0MWx.  .''''''''''''''''''.  ;OKOOOO0NWMMMMMMMMMMMMNl.     .cdoox0XOl;'....... ...        .'''.            
            .;ol'    ...................   ;kXWMMMMMMMMMMMMMMMMMWx.          .:0WNKkdo:.  ...         .'''.             
           ....................              .:ldxk0XWMMMMMMMMMMMW0o'        .';;,.         ....     ..'''.             
         ;k00000000000000000000x'                  ..;lkXWMMMMMMMMMWXkc.                            ..'''.              
        .lXWWWWWWWWWWWWWWWWWWMMWKl.                     ;OWMMMMMMMMMMMWKx:.                       ..''''.               
          .,,,,,,,,,,,,,,,,,:kNMMW0o,.                  'kWMMMMMMMMMMMMMMWKd,.                  ..''''..                
                             .:ONMMMNKkdlc:::::::::ccldkKWMMMMMMMMMMMMMMMMMMNOl'    ...........'''''..                  
                               .,oOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXkc....''''''''''...                     
                                  .':ldkO0000000000000000000000000000000000000000Ox:.  ........                         
                                         ...........................................                                                                                                                
	""", "blue", attrs=['bold']))

	print (colored('''		   
				   _        _______  ______            _        _______ 
				  ( (    /|(  ____ \(  ___ \ |\     /|( \      (  ___  )
				  |  \  ( || (    \/| (   ) )| )   ( || (      | (   ) |
				  |   \ | || (__    | (__/ / | |   | || |      | (___) |
				  | (\ \) ||  __)   |  __ (  | |   | || |      |  ___  |
				  | | \   || (      | (  \ \ | |   | || |      | (   ) |
				  | )  \  || (____/\| )___) )| (___) || (____/\| )   ( |
				  |/    )_)(_______/|/ \___/ (_______)(_______/|/     \|
							Because Clouds are so AWSome'''
				   ,"red",attrs=['bold']))
	print (colored('''
				-------------------------------------------------------------
								Created by: gl4ssesbo1
				-------------------------------------------------------------''', "green"))

def module_count():
	all_count = 0
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
        'stager',
		'misc'
	]

	nr_of_modules = {
		'cleanup':"",
		'detection':"",
		'detectionbypass':"",
		'enum':"",
		'exploit':"",
		'lateralmovement':"",
		'listeners':"",
		'persistence':"",
		'privesc':"",
		'reconnaissance':"",
		'stager':"",
		'misc':""
	}
	for module in show:
		module_count = 0
		arr = os.listdir("./module/" + module)
		for x in arr:
			if "__" in x:
				continue
			elif ".git" in x:
				continue
			else:
				module_count += 1
				all_count += 1
		if module_count == 0:
			nr_of_modules[module] = "0"
		else:
			nr_of_modules[module] = module_count

	nr_of_cloud_modules = {
		"aws":0,
		"gcp":0,
		"azure":0,
		"o365":0,
		"docker":0,
		"kube":0,
		"misc":0,
		"azuread": 0
	}
	clouds = [
		"aws",
		"gcp",
		"azure",
		"o365",
        "docker",
        "kube",
		"azuread",
		"misc"
	]
	for cloud in clouds:
		module_count = 0
		for module in show:
			arr = os.listdir("./module/" + module)
			for x in arr:
				if "__" in x:
					continue
				elif ".git" in x:
					continue
				else:
					if x.split("_")[0] == cloud:
						module_count += 1
		nr_of_cloud_modules[cloud] = module_count

	print ("\t\t\t\t{} aws\t\t{} gcp\t\t{} azure\t\t{} office365".format(nr_of_cloud_modules['aws'], nr_of_cloud_modules['gcp'], nr_of_cloud_modules['azure'], nr_of_cloud_modules['o365']))
	print ("\t\t\t\t{} docker\t{} kubernetes\t{} misc\t\t{} azuread".format(nr_of_cloud_modules['docker'], nr_of_cloud_modules['kube'], nr_of_cloud_modules['misc'], nr_of_cloud_modules['azuread']))
	print(colored("\t\t\t\t-------------------------------------------------------------", "green"))
	print ("\t\t\t\t{} modules\t{} cleanup\t\t{} detection".format(all_count, nr_of_modules['cleanup'], nr_of_modules['detection']))
	print ("\t\t\t\t{} enum\t\t{} exploit\t\t{} persistence".format(nr_of_modules['enum'], nr_of_modules['exploit'],nr_of_modules['persistence']))
	print ("\t\t\t\t{} listeners\t{} lateral movement\t{} detection bypass".format(nr_of_modules['listeners'], nr_of_modules['lateralmovement'],nr_of_modules['detectionbypass']))
	print ("\t\t\t\t{} privesc\t{} reconnaissance\t{} stager".format(nr_of_modules['privesc'], nr_of_modules['reconnaissance'], nr_of_modules['stager']))
	print ("\t\t\t\t{} misc".format(nr_of_modules['misc']))

def disclaimer():
	print (colored("\n\t\t\t\tRemember:", "red",attrs=['bold']))
	print (colored("\t\t\t\t-------------------------------------------------------------", "yellow"))
	disclaimer1 = '''1) Only use this tool if you have permissions from the infrastructure's owner. Don't be a dick. Don't choose jail. And if you have some scruples, don't hack others just because you can (or cannot, in which case that's why you chose this tool to do it).'''
	disclaimer2 = '''2) There is a template file on module directory that you can use if you want to develop new modules. If you want to contribute on this tool, be my guest.'''
	disclaimer3 = '''3) Thank you for using this tool and Hack the Planet Legally!'''


	for disclaimer in justify(disclaimer1, 61):
		print (colored("\t\t\t\t{}".format(disclaimer),"yellow"))
	print()
	for disclaimer in justify(disclaimer2, 61):
		print(colored("\t\t\t\t{}".format(disclaimer), "yellow"))
	print()
	for disclaimer in justify(disclaimer3, 61):
		print (colored("\t\t\t\t{}".format(disclaimer),"yellow"))
	print (colored("\t\t\t\t{}".format("-------------------------------------------------------------"),"yellow"))

def module_count_without_banner():
	all_count = 0
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
        'stager',
		'misc'
	]

	nr_of_modules = {
		'cleanup':"",
		'detection':"",
		'detectionbypass':"",
		'enum':"",
		'exploit':"",
		'lateralmovement':"",
		'listeners':"",
		'persistence':"",
		'privesc':"",
		'reconnaissance':"",
		'stager':"",
		'misc':""
	}
	for module in show:
		module_count = 0
		arr = os.listdir("./module/" + module)
		for x in arr:
			if "__" in x:
				continue
			elif ".git" in x:
				continue
			else:
				module_count += 1
				all_count += 1
		nr_of_modules[module] = module_count

	nr_of_cloud_modules = {
		"aws":0,
		"gcp":0,
		"azure":0,
		"o365":0,
		"docker":0,
		"kube":0,
		"misc":0,
		"azuread":0
	}
	clouds = [
		"aws",
		"gcp",
		"azure",
		"o365",
        "docker",
        "kube",
		"misc",
		"azuread"
	]
	for cloud in clouds:
		module_count = 0
		for module in show:
			arr = os.listdir("./module/" + module)
			for x in arr:
				if "__" in x:
					continue
				elif ".git" in x:
					continue
				else:
					if x.split("_")[0] == cloud:
						module_count += 1
		nr_of_cloud_modules[cloud] = module_count

	print ("{} aws\t\t{} gcp\t\t{} azure\t\t{} office365".format(nr_of_cloud_modules['aws'], nr_of_cloud_modules['gcp'], nr_of_cloud_modules['azure'], nr_of_cloud_modules['o365']))
	print ("{} docker\t{} kubernetes\t{} misc\t\t{} azuread".format(nr_of_cloud_modules['docker'], nr_of_cloud_modules['kube'], nr_of_cloud_modules['misc'], nr_of_cloud_modules['azuread']))
	print(colored("-------------------------------------------------------------", "green"))
	print ("{} modules\t{} cleanup\t\t{} detection".format(all_count, nr_of_modules['cleanup'], nr_of_modules['detection']))
	print ("{} enum\t\t{} exploit\t\t{} persistence".format(nr_of_modules['enum'], nr_of_modules['exploit'],nr_of_modules['persistence']))
	print ("{} listeners\t{} lateral movement\t{} detection bypass".format(nr_of_modules['listeners'], nr_of_modules['lateralmovement'],nr_of_modules['detectionbypass']))
	print ("{} privesc\t{} reconnaissance\t{} stager".format(nr_of_modules['privesc'], nr_of_modules['reconnaissance'], nr_of_modules['stager']))
	print ("{} misc".format(nr_of_modules['misc']))
