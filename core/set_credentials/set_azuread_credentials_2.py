import sys
from termcolor import colored
import msal
import json

def auth_user_pass(username, password, client_id, scopes):
    context = msal.PublicClientApplication(client_id)
    '''scopes = [
        "https://awsaccthreeprotonmail.onmicrosoft.com/b8897d37-4dc9-4246-b84d-a58418bb39c3/Employees.Write.All",
        "https://awsaccthreeprotonmail.onmicrosoft.com/b8897d37-4dc9-4246-b84d-a58418bb39c3/Employees.Read.All"
    ]'''
    return context.acquire_token_by_username_password(username, password, scopes=scopes)

def auth_device_code(client_id, scopes):
    context = msal.PublicClientApplication(client_id)
    '''scopes = [
        "Employees.Write.All",
        "Employees.Read.All"
    ]
    scope = ["User.Read"]
    '''
    device_flow = context.initiate_device_flow()
    print(device_flow['message'])
    return context.acquire_token_by_device_flow(device_flow)

def auth_refresh_token(refresh_token, client_id, scopes):
    context = msal.PublicClientApplication(client_id)
    return context.acquire_token_by_refresh_token(refresh_token, scopes)

def auth_client_credentials(client_id):
    context = msal.PublicClientApplication(client_id)

def acquire_token_by_auth_code_flow(client_id):
    context = msal.PublicClientApplication(client_id)
    context.acquire_token_by_auth_code_flow()

def set_azuread_creds_2(command, all_sessions, comms):
    username = 'bproko@awsaccthreeprotonmail.onmicrosoft.com'
    password = 'Boqo4838...'
    client_id = 'b8897d37-4dc9-4246-b84d-a58418bb39c3'
    print(auth_device_code(client_id))
    #print(auth_user_pass(username, password, client_id))

def set_azuread_creds(command, all_sessions, comms):
    sess_test = {}

    #client_id = '440230b9-c91e-458c-88f8-63efbecd86e6'
    RESOURCE = 'https://graph.windows.net/'
    if len(command.split(" ")) < 3:
        print(
            colored("[*] The right command is: set azure-credentials <profile name>", "red")
        )
    elif len(command.split(" ")) > 2:
        print("Profile Name: {}".format(command.split(" ")[2]))
        a = 0
        if len(all_sessions) > 0:
            for credentials in all_sessions:
                if credentials['profile'] == command.split(" ")[2]:
                    print(colored("[*] Those credentials exist. Try a new Profile Name", "red"))
                    a = 1

        if a == 0:
            connectiontype = input("""
Choose the connection type:
    1) Device Code
    2) Username and Password
    3) PRT Token
>>> """)

            b = 0
            refresh_token = ""

            if not int(connectiontype.strip()) == 1 and not int(connectiontype.strip()) == 2 and not int(connectiontype.strip()) == 3:
                print(colored(
                    "[*] Either enter 1, 2 or 3 for the connection type.", "red"
                ))

            elif int(connectiontype.strip()) == 1:
                sess_test['provider'] = 'AZUREAD'

            elif int(connectiontype.strip()) == 2:
                sess_test['provider'] = 'AZUREAD'
                username = input("Username: ")
                password = input("Password: ")
                sess_test['username'] = username
                sess_test['password'] = password

            elif int(connectiontype.strip()) == 3:
                sess_test['provider'] = 'AZUREAD'
                refresh_token = input("Refresh Token: ")


            sess_test['profile'] = str(command.split(" ")[2])

            client_id = input("Client ID: ")
            sess_test['client_id'] = client_id

            scope = input("Scopes: ")
            scopes = scope.replace(" ", "").split(",")
            sess_test['scopes'] = scopes

            try:
                creds = {}
                if int(connectiontype.strip()) == 1:
                    creds = auth_device_code(sess_test['client_id'], sess_test['scopes'])

                elif int(connectiontype.strip()) == 2:
                    creds = auth_user_pass(sess_test['username'], sess_test['password'], sess_test['client_id'], sess_test['scopes'])

                elif int(connectiontype.strip()) == 3:
                    creds = auth_refresh_token(refresh_token, sess_test['client_id'], sess_test['scopes'])

                if len(creds) > 0:
                    if not 'error' in creds:
                        sess_test['access_token'] = creds['access_token']
                        sess_test['refresh_token'] = creds['refresh_token']
                        sess_test['id_token'] = creds['id_token']
                        sess_test['expires_in'] = creds['expires_in']
                        sess_test['ext_expires_in'] = creds['ext_expires_in']
                        sess_test['name'] = creds['id_token_claims']['name']
                        sess_test['iss'] = creds['id_token_claims']['iss']
                        sess_test['UID'] = creds['id_token_claims']['oid']
                    else:
                        print(creds['error'])
                        b = 1
                else:
                    b = 1

                if b == 0:
                    cred_prof = sess_test['profile']
                    all_sessions.append(sess_test)
                    comms['use']['credentials'][cred_prof] = None
                    comms['remove']['credentials'][cred_prof] = None

                    print(
                        colored("[*] Credentials set. Use ", "green") +
                        colored("'show credentials' ", "blue") +
                        colored("to check them.", "green")
                    )
                    print(
                        colored("[*] Currect credential profile set to ", "green") +
                        colored("'{}'.".format(cred_prof), "blue") +
                        colored("Use ", "green") +
                        colored("'show current-creds' ", "blue") +
                        colored("to check them.", "green")
                    )
            except:
                e = sys.exc_info()
                print(e)