from simulib.Azure.Authentication.Authentication import DeviceAuthentication
from simulib.Azure.Authentication.Authentication import ClientAuthentication

def generateManagementDeviceCodeToken():
    graphapi = DeviceAuthentication(
        scope="https://management.core.windows.net/.default openid profile offline_access",
        resource_uri="https://management.azure.com",
        client_id="1950a258-227b-4e31-a9cf-717495945fc2",
        proxies=None,
        verify=True,
        tenant=None
    )
    graphTokenData = graphapi.authenticate_device_code()
    graphAccessToken = graphTokenData['accessToken']
    graphRefreshToken = graphTokenData['refreshToken']

    return {"accessToken": graphAccessToken, "refreshToken": graphRefreshToken}

def generateManagementClientSecret(args):
    mgmtapi = ClientAuthentication(
        scope="https://management.core.windows.net/.default openid profile offline_access",
        resource_uri="https://management.azure.com/",
        client_id=args.client_id,
        client_secret=args.client_secret,
        proxies=None,
        verify=True,
        tenant=args.tenant
    )
    # appID, scope, resource_uri, client_id, client_secret, proxies=None, verify=True, tenant=None

    mgmtapiData = mgmtapi.authenticate_clientid_clientsecret()
    mgmtapiAccessToken = mgmtapiData['access_token']
    return {"accessToken": mgmtapiAccessToken, "refreshToken": None}