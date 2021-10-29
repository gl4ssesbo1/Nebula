#import azure.identity
import adal
'''
+ get_authority_url
+ DeviceCode
   - ClientID
+ InteractiveBrowser
   - No Args
+ User & Pass
+ Service Principal user + pass
+ Service Principal Certifiate
'''

resource_uri = 'https://graph.windows.net/'
global client_id
client_id = ''
proxies = None
verify = True
global tokendata
tokendata = {}

def get_authority_url(tenant):
    if tenant is not None:
        return 'https://login.microsoftonline.com/{}'.format(tenant)
    return 'https://login.microsoftonline.com/common'

def authenticate_device_code(proxies, verify, client_id):
    global tokendata
    authority_host_uri = get_authority_url()

    context = adal.AuthenticationContext(
        authority_host_uri,
        api_version=None,
        proxies=proxies,
        verify_ssl=verify
    )
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    tokendata = context.acquire_token_with_device_code(resource_uri, code, client_id)

def authenticate_username_password(username, password, client_id):
    """
    Authenticate using user w/ username + password.
    This doesn't work for users or tenants that have multi-factor authentication required.
    """
    global tokendata
    authority_uri = get_authority_url()
    context = adal.AuthenticationContext(authority_uri, api_version=None, proxies=proxies, verify_ssl=verify)
    tokendata = context.acquire_token_with_username_password(resource_uri, username, password, client_id)

def run_azure_module(imported_module, all_sessions, cred_prof, workspace, useragent, client_id):
    global tokendata
    global client_id
    if imported_module.needs_creds:
        print("You ran an azure module")
    else:
        imported_module.exploit(workspace)
