import base64
import json

import requests
from termcolor import colored
import adal

class DeviceAuthentication:
    def __init__(self, scope, resource_uri, client_id, proxies, verify, tenant):
        print(
            colored("[*] Authenticating using Device Code...", "yellow", attrs=["bold"])
        )
        self.proxies = proxies
        self.verify = verify
        self.tokendata = {}
        self.resource_uri = resource_uri
        self.scope = scope
        self.client_id = client_id
        self.tenant = tenant

    #resource_uri = 'https://graph.windows.net/'

    def get_authority_url(self):
        if self.tenant is not None:
            return 'https://login.microsoftonline.com/{}'.format(self.tenant)
        return 'https://login.microsoftonline.com/common'

    def authenticate_device_code(self):
        authority_host_uri = self.get_authority_url()

        context = adal.AuthenticationContext(
            authority_host_uri,
            api_version=None,
            proxies=self.proxies,
            verify_ssl=self.verify
        )
        code = context.acquire_user_code(self.resource_uri, self.client_id)
        if 'message' in code:
            print(code['message'])
        responseMessage = context.acquire_token_with_device_code(self.resource_uri, code, self.client_id)
        print(
            colored(f"[*] Authenticated using Device Code!", "green", attrs=["bold"])
        )
        return responseMessage


class UserAuthentication:
    def __init__(self, scope, resource_uri, client_id, email, password, proxies=None, verify=True, tenant=None):
        print(
            colored("[*] Authenticating using Email and Password...", "yellow", attrs=["bold"])
        )
        self.proxies = proxies
        self.verify = verify
        self.tokendata = {}
        self.resource_uri = resource_uri
        self.scope = scope
        self.client_id = client_id
        self.tenant = tenant
        self.email = email
        self.password = password


    # resource_uri = 'https://graph.windows.net/'

    def get_authority_url(self):
        if self.tenant is not None:
            return 'https://login.microsoftonline.com/{}'.format(self.tenant)
        return 'https://login.microsoftonline.com/common'

    def authenticate_username_password(self):
        """
        Authenticate using user w/ username + password.
        This doesn't work for users or tenants that have multi-factor authentication required.
        """
        authority_uri = self.get_authority_url()
        context = adal.AuthenticationContext(authority_uri, api_version=None, proxies=self.proxies, verify_ssl=self.verify)
        print(
            colored("[*] Authenticated using Email and Pass!", "green", attrs=["bold"])
        )
        return context.acquire_token_with_username_password(self.resource_uri, self.username, self.password, self.client_id)

class ClientAuthentication():
    def __init__(self, scope, resource_uri, client_id, client_secret, proxies=None, verify=True, tenant=None):
        self.proxies = proxies
        self.verify = verify
        self.tokendata = {}
        #self.appId = appID
        self.resource_uri = resource_uri
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant

    def authenticate_clientid_clientsecret(self):
        token = requests.post(
            #f"https://login.microsoftonline.com/{self.tenant}/oauth2/token?grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&resource=https%3A%2F%2Fmanagement.azure.com%2F",
            f"https://login.microsoftonline.com/{self.tenant}/oauth2/token",
            data=f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&resource=https://management.azure.com/"
        ).json()

        print(
            colored("[*] Authenticated using Client ID and Client Secret!", "green", attrs=["bold"])
        )

        return token

    def getServicePrincipalObjectID(self):
        accessTokenJSON = self.accessToken.split(".")[1]
        spID = json.loads(base64.b64decode(f"{accessTokenJSON}==".encode()))['tid']
        #spID = accessTokenJSON.encode().decode('base64')


        management_api_url = f"https://management.azure.com/subscriptions/{self.subscriptionId}/providers/Microsoft.Authorization?api-version=2023-07-01"

        # Make the GET request to retrieve service principals
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'Content-Type': 'application/json'
        }

        response = requests.get(management_api_url, headers=headers).json()
        #print(json.dumps(response, indent=4, default=str))

    def acquire_token_with_client_certificate(resource_uri, client_id, certificate, thumbprint):
        print()

class AppConsentAuthentication():
    def __init__(self, scope, resource_uri, client_id, client_secret, proxies=None, verify=True, tenant=None):
        print(
            colored("[*] Authenticating using Client ID and Client Secret...", "yellow", attrs=["bold"])
        )
        self.proxies = proxies
        self.verify = verify
        self.tokendata = {}
        #self.appId = appID
        self.resource_uri = resource_uri
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant

    def authenticate_with_app_consent(self):
        print()