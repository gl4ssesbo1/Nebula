import sys
from termcolor import colored
import adal
import json

def auth_user_pass(authority, RESOURCE, username, password, client_id):
    context = adal.AuthenticationContext(authority)
    return context.acquire_token_with_username_password(RESOURCE, username, password, client_id)

def auth_device_code(authority, RESOURCE, client_id):
    context = adal.AuthenticationContext(authority)
    code = context.acquire_user_code(RESOURCE, client_id)
    print(code['message'])
    return context.acquire_token_with_device_code(RESOURCE, code, client_id)

def auth_refresh_token(refresh_token, client_id, RESOURCE, authority):
    context = adal.AuthenticationContext(authority)
    return context.acquire_token_with_refresh_token(refresh_token, client_id, RESOURCE)

'''
def set_azuread_creds_2(command, all_sessions, comms):
    RESOURCE = 'https://graph.windows.net/'
    tenant = ""
    #tenant = '3d1f3321-ab7a-43ac-aeec-5317c326d679'
    authority = get_authority(tenant)
    print(authority)
    username = 'bproko@awsaccthreeprotonmail.onmicrosoft.com'
    password = 'Boqo4838...'
    #client_id = 'b8897d37-4dc9-4246-b84d-a58418bb39c3'
    client_id = '1b730954-1685-4b74-9bfd-dac224a7b894'
    #client_id = 'c44b4083-3bb0-49c1-b47d-974e53cbdf3c'
    print(auth_device_code(authority, RESOURCE, client_id))
    #print(auth_user_pass(username, password, client_id))
'''

def set_azuread_creds(command, all_sessions, comms, cred_prof):
    sess_test = {}
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
    4) Certificate Authentication
>>> """)

            b = 0
            refresh_token = ""

            if not int(connectiontype.strip()) == 1 and not int(connectiontype.strip()) == 2 and not int(connectiontype.strip()) == 3 and not int(connectiontype.strip()) == 4:
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

            client_id = input("Client ID (Empty if none): ")
            if client_id == "":
                client_id = '1b730954-1685-4b74-9bfd-dac224a7b894'
            sess_test['client_id'] = client_id

            tenant = input("Tenant (Empty if none): ")
            if tenant == "":
                tenant = 'common'
            sess_test['tenant'] = tenant

            authority = "https://login.microsoftonline.com/{}".format(tenant)
            sess_test['authority'] = authority

            sess_test['RESOURCE'] = RESOURCE

            try:
                creds = {}
                if int(connectiontype.strip()) == 1:
                    creds = auth_device_code(sess_test['authority'], sess_test['RESOURCE'], sess_test['client_id'])

                elif int(connectiontype.strip()) == 2:
                    creds = auth_user_pass(authority, RESOURCE, sess_test['username'], sess_test['password'], sess_test['client_id'])

                elif int(connectiontype.strip()) == 3:
                    creds = auth_refresh_token(refresh_token, sess_test['client_id'], RESOURCE, authority)
                    print(creds)

                if len(creds) > 0:
                    if not 'error' in creds:
                        sess_test['access_token'] = creds['accessToken']
                        sess_test['refresh_token'] = creds['refreshToken']
                        sess_test['expiresIn'] = creds['expiresIn']
                        sess_test['expiresOn'] = creds['expiresOn']
                        sess_test['userId'] = creds['userId']
                        sess_test['tenantId'] = creds['tenantId']
                        sess_test['clientId'] = creds['_clientId']
                        sess_test['UID'] = creds['oid']
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

    return cred_prof