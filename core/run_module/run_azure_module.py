#import azure.identity

'''
+ DeviceCode
   - ClientID
+ InteractiveBrowser
   - No Args
+ User & Pass
+ Service Principal user + pass
+ Service Principal Certifiate
'''

def run_azure_module(imported_module, all_sessions, cred_prof, workspace, useragent):
    if imported_module.needs_creds:
        print("You ran an azure module")
    else:
        imported_module.exploit(workspace)
