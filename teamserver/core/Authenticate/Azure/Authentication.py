import adal
from termcolor import colored

def get_authority_url(tenant):
    if tenant is not None:
        return 'https://login.microsoftonline.com/{}'.format(tenant)
    return 'https://login.microsoftonline.com/common'

def authenticate_device_code(resource_uri, client_id, proxies, verify, tenant):
    authority_host_uri = get_authority_url(tenant)

    context = adal.AuthenticationContext(
        authority_host_uri,
        api_version=None,
        proxies=proxies,
        verify_ssl=verify
    )
    code = context.acquire_user_code(resource_uri, client_id)
    if 'message' in code:
        print(code['message'])
    responseMessage = context.acquire_token_with_device_code(resource_uri, code, client_id)
    print(
        colored(f"[*] Authenticated using Device Code!", "green", attrs=["bold"])
    )
    return responseMessage

def authenticate_username_password(tenant, resource_uri, proxies, verify, username, password, client_id):
    authority_uri = get_authority_url(tenant=tenant)
    context = adal.AuthenticationContext(authority_uri, api_version=None, proxies=proxies, verify_ssl=verify)
    print(
        colored("[*] Authenticated using Email and Pass!", "green", attrs=["bold"])
    )
    return context.acquire_token_with_username_password(resource_uri, username, password, client_id)

