from termcolor import colored

def help():
    help_commands()
    credential_commands()
    module_commands()
    useragent_commands()
    workspace_commands()
    shell_help()

def specific_help(command):
    if command == 'user-agent':
        useragent_commands()
    elif command == 'module':
        module_commands()
    elif command == 'workspace':
        workspace_commands()
    elif command == 'credentials':
        credential_commands()
    elif command == 'shell':
        shell_help()
    else:
        print(colored("[*] That help does not exist.", "red"))

def help_commands():
    print (colored('''
    Help Command:                       Description:
    -------------                       ------------''',"green", attrs=['bold']))
    print(colored('''
    help                                Show help for all the commands
    help credentials                    Show help for credentials
    help module                         Show help for modules
    help workspace                      Show help for credentials
    help user-agent                     Show help for credentials
    help shell                          Show help for shell connections
    '''))

def module_commands():
    print(colored('''
    Module Commands                     Description
    ---------------                     -----------''',"green",attrs=['bold']))

    print(colored('''
    show modules                        List all the modules
    show enum                           List all Enumeration modules
    show exploit                        List all Exploit modules
    show persistence                    List all Persistence modules
    show privesc                        List all Privilege Escalation modules
    show reconnaissance                 List all Reconnaissance modules
    show listener                       List all Reconnaissance modules
    show cleanup                        List all Enumeration modules
    show detection                      List all Exploit modules
    show detectionbypass                List all Persistence modules
    show lateralmovement                List all Privilege Escalation modules
    show stager                         List all Reconnaissance modules
    
    use module <module>                 Use a module.
    options                             Show options of a module you have selected.
    run                                 Run a module you have selected. Eg: 'run <module name>'
    search                              Search for a module via pattern. Eg: 'search s3'
    back                                Unselect a module
    set <option>                        Set option of a module. Need to have the module used first.
    unset <option>                      Unset option of a module. Need to have the module used first.
    '''))

def workspace_commands():
    print(colored('''
    Workspace Commands                  Description
    ------------------                  -----------''',"green",attrs=['bold']))

    print(colored('''
    create workspace <wp>               Create a workspace
    use workspace <wp>                  Use one of the workspaces
    remove workspace <wp>               Remove a workspace
    '''))

def useragent_commands():
    print(colored('''
    User-Agent commands                 Description
    -------------------                 -----------''',"green",attrs=['bold']))

    print(colored('''
    set user-agent windows              Set a windows client user agent
    set user-agent linux                Set a linux client user agent
    set user-agent custom               Set a custom client user agent
    show user-agent                     Show the current user-agent
    unset user-agent                    Use the user agent that boto3 produces
    '''))

def credential_commands():
    print(colored('''
    Credential commands                 Description
    -------------------                 -----------''',"green", attrs=['bold']))

    print(colored('''
    set aws-credentials <cred name>     Insert credentials while providing the name as argument
    use credentials <cred name>         Use the credentials you want
    show credentials                    Show all credentials
    show current-creds                  Show credentials you are currently using
    remove credentials                  Delete credentials
    import credentials                  Import credentials dumped before
    dump credentials                    Dump credentials on files stored on directory credentials on Nebula dir
    getuid                              Get the username, arn, account ID from a set of credentials you have found.
    enum_user_privs                     Get the Read Privileges of a set of Credentials
    '''))

def shell_help():
    print(colored('''
    Shell commands                      Description
    -------------------                 -----------''', "green", attrs=['bold']))
    print(colored(
    '''
    shell check_env                     Check the environment you are in, get data and meta-data
    shell exit                          Kill a connection
    shell <command>                     Run a command on a system. You don't need " on the command, just shell <command1> <command2>
    '''))

def user_help():
    print(colored('''
       User commands                       Description
       -------------------                 -----------''', "green", attrs=['bold']))
    print(colored(
        '''
        create user <username>                     Check the environment you are in, get data and meta-data
        shell exit                          Kill a connection
        shell <command>                     Run a command on a system. You don't need " on the command, just shell <command1> <command2>
        '''))