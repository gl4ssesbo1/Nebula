import adal

resource_uri = 'https://graph.windows.net/'
proxies = None
verify = True
global tokendata
tokendata = {}

def get_authority_url(tenant):
    if tenant is not None:
        return 'https://login.microsoftonline.com/{}'.format(tenant)
    return 'https://login.microsoftonline.com/common'

def authenticate_device_code(proxies, verify, client_id, tenant):
    global tokendata
    authority_host_uri = get_authority_url(tenant)

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

def authenticate_clientid_clientsecret(client_id, client_secret, tenant, resource):
    authority_url = get_authority_url(tenant)

    GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'
    RESOURCE = resource

    # uncomment for verbose log
    # turn_on_logging()

    ### Main logic begins
    context = adal.AuthenticationContext(
        authority_url, validate_authority=tenant != 'adfs',
    )

    token = context.acquire_token_with_client_credentials(
        GRAPH_RESOURCE,
        client_id,
        client_secret
    )

    print(token)
    return token

def acquire_token_with_client_certificate(resource_uri, client_id, certificate, thumbprint):
    print()