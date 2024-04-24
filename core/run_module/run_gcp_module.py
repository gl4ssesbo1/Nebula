def run_gcp_module(imported_module, all_sessions, cred_prof, workspace, useragent=""):
    if imported_module.needs_creds:
        return {"message": "You ran a GCP module"}
    else:
        return imported_module.exploit()