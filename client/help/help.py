from termcolor import colored

def help():
    help_commands()
    credential_commands()
    module_commands()
    useragent_commands()
    shell_help()
    user_help()

def specific_help(command):
    if command == 'user-agent':
        useragent_commands()
    elif command == 'module':
        module_commands()
    elif command == 'credentials':
        credential_commands()
    elif command == 'user':
        user_help()
    elif command == 'shell':
        shell_help()
    else:
        print(colored("[*] That help does not exist.", "red"))

def help_commands():
    print (colored('''
    Help Command:                       Description:
    -------------                       ------------''',"green", attrs=['bold']))
    print(colored('''    help                                Show help for all the commands
    help credentials                    Show help for credentials
    help module                         Show help for modules
    help user-agent                     Show help for credentials
    help shell                          Show help for shell connections
    '''))

def module_commands():
    print(colored('''
    Module Commands                     Description
    ---------------                     -----------''',"green",attrs=['bold']))

    print(colored('''    show modules                        List all the modules
    use module <module>                 Use a module.
    options                             Show options of a module you have selected.
    run                                 Run a module you have selected. Eg: 'run <module name>'
    back                                Unselect a module
    set <option>                        Set option of a module. Need to have the module used first.
    unset <option>                      Unset option of a module. Need to have the module used first.
    '''))

def useragent_commands():
    print(colored('''
    User-Agent commands                 Description
    -------------------                 -----------''',"green",attrs=['bold']))

    print(colored('''    set user-agent windows              Set a windows client user agent
    set user-agent linux                Set a linux client user agent
    set user-agent custom               Set a custom client user agent
    show user-agent                     Show the current user-agent
    unset user-agent                    Use the user agent that boto3 produces
    '''))

def credential_commands():
    print(colored('''
    Credential commands                 Description
    -------------------                 -----------''',"green", attrs=['bold']))

    print(colored('''    set aws-credentials <cred name>     Insert credentials while providing the name as argument
    set do-credentials <cred name>      Insert credentials while providing the name as argument
    set azure-credentials <cred name>   Insert credentials while providing the name as argument
    use credentials <cred name>         Use the credentials you want
    show credentials                    Show all credentials
    show current-creds                  Show credentials you are currently using
    remove credentials                  Delete credentials
    getuid                              Get the username, arn, account ID from a set of credentials you have found.
    enum_user_privs                     Get the Read Privileges of a set of Credentials
    '''))

def shell_help():
    print(colored('''
    Shell commands                      Description
    -------------------                 -----------''', "green", attrs=['bold']))
    print(colored(
    '''    shell check_env                     Check the environment you are in, get data and meta-data
    shell exit                          Kill a connection
    shell <command>                     Run a command on a system. You don't need " on the command, just shell <command1> <command2>
    '''))

def user_help():
    print(colored('''
    User commands                       Description
    -------------------                 -----------''', "green", attrs=['bold']))
    print(colored(
    '''    create user <username>              Check the environment you are in, get data and meta-data
    '''))