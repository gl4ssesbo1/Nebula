import os
import sys
import webbrowser

import requests

from simulib.Azure.Authentication.Authentication import DeviceAuthentication
from simulib.Azure.Authentication.Authentication import ClientAuthentication
from simulib.Azure.Authentication.Authentication import UserAuthentication

from simulib.Other.printOutput import printOutput
from simulib.Other.PrintError import printError

def generateGraphDeviceCodeToken(clientID, tenantID):
    graphapi = DeviceAuthentication(
        #scope="https://graph.microsoft.com/.default",
        scope="https://graph.microsoft.com/UserAuthenticationMethod.ReadWrite.All Policy.ReadWrite.AuthenticationMethod",
        #scope="https://graph.microsoft.com/Directory.ReadWrite.All UserAuthenticationMethod.ReadWrite.All UserAuthenticationMethod.ReadWrite.All",
        resource_uri="https://graph.microsoft.com",
        #client_id="c44b4083-3bb0-49c1-b47d-974e53cbdf3c",
        #client_id="50483e42-d915-4231-9639-7fdb7fd190e5",
        client_id=clientID,#"1b730954-1685-4b74-9bfd-dac224a7b894",
        #client_id="de8bc8b5-d9f9-48b1-a8ad-b748da725064",
        proxies=None,
        verify=True,
        tenant=tenantID
    )
    graphTokenData = graphapi.authenticate_device_code()
    graphAccessToken = graphTokenData['accessToken']
    graphRefreshToken = graphTokenData['refreshToken']

    return {"accessToken": graphAccessToken, "refreshToken": graphRefreshToken}

def generateGraphClientSecretOld(client_secret, client_id, tenant):
    graphapi = ClientAuthentication(
        #scope="https://graph.microsoft.com/.default",
        scope="https://graph.microsoft.com/.default",
        resource_uri="https://graph.microsoft.com",
        client_id=client_id,
        client_secret=client_secret,
        proxies=None,
        verify=True,
        tenant=tenant
    )
    # appID, scope, resource_uri, client_id, client_secret, proxies=None, verify=True, tenant=None


    graphTokenData = graphapi.authenticate_clientid_clientsecret()
    #print(graphTokenData)
    try:
        graphAccessToken = graphTokenData['access_token']
        #graphRefreshToken = graphTokenData['refreshToken']

        return {"accessToken": graphAccessToken, "refreshToken": None}
    except:
        return None

def generateGraphClientSecret(client_secret, client_id, tenant):
    #webbrowser.open(f'https://login.microsoftonline.com/{tenant}/adminconsent?client_id={client_id}&redirect_uri=http://localhost/myapp/permissions')
    #webbrowser.open(f'https://login.microsoftonline.com/{tenant}/adminconsent?client_id={client_id}&redirect_uri=http://localhost')

    graphTokenData = requests.post(
        f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=f'client_id={client_id}&client_secret={client_secret}&scope=https://graph.microsoft.com/.default&grant_type=client_credentials'
    ).json()
    # appID, scope, resource_uri, client_id, client_secret, proxies=None, verify=True, tenant=None


    #graphTokenData = graphapi.authenticate_clientid_clientsecret()
    #print(graphTokenData)
    if "error" in graphTokenData:
        printOutput("Lucr3 AzureAD Authentication", f"Error authenticating: {graphTokenData['error_description']}", "error")
        return None
    else:
        graphAccessToken = graphTokenData['access_token']
        #graphRefreshToken = graphTokenData['refreshToken']

        return {"accessToken": graphAccessToken, "refreshToken": None}


def generateGraphUserPass(azuread_identity_id, azuread_identity_secret, tenant=None):
    # appID, scope, resource_uri, client_id, email, password, proxies=None, verify=True, tenant=None
    graphAPI = UserAuthentication(
        client_id="1b730954-1685-4b74-9bfd-dac224a7b894",
        scope="https://graph.microsoft.com/.default",
        resource_uri="https://graph.microsoft.com",
        email=azuread_identity_id,
        password=azuread_identity_secret,
        proxies=None,
        verify=True,
        tenant=tenant
    )
    graphTokenData = graphAPI.authenticate_username_password()
    graphAccessToken = graphTokenData['accessToken']
    graphRefreshToken = graphTokenData['refreshToken']

    return {"accessToken": graphAccessToken, "refreshToken": graphRefreshToken}

