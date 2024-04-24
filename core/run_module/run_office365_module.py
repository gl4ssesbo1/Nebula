#import azure.identity
import core.auth.auth_azuread
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

def run_o365_module(imported_module, all_sessions, cred_prof, workspace, useragent=""):
    global tokendata
    if imported_module.needs_creds:
        for sess in all_sessions:
            if cred_prof == sess['profile']:
                return imported_module.exploit(sess, workspace)

    else:
        return imported_module.exploit(workspace)
