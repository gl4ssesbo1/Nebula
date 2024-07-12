import json
import sys
import botocore
import requests
from mongoengine import DoesNotExist
from core.database.models import DigitalOceanSpace

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "RESOURCE-TYPE": {
        "value": "all",
        "required": "true",
        "description": "The resource type to enumerate. It can be one of the values: accounts, projects, , "
                       "actions, apps, blockstorage, cdn, certificates, containerregistry, databases, "
                       "domains, droplets, firewalls, floatingips, functions, images, kubernetes, loadbalancers, "
                       "regions, reservedips, snapshots, sshkeys, tags, uptime, vpcs or all for all resources."
    }
}

description = "Enumerate all DigitalOcean Resources"
aws_command = ""


def exploit(profile):
    resourceType = variables['RESOURCE-TYPE']['value']
    return_dict = {
        "ResourceType": resourceType,
        "ResourceInfo": None
    }
    RESOURCETYPES = ['accounts', 'projects', 'actions', 'apps', 'blockstorage', 'cdn',
                     'certificates', 'containerregistry', 'databases', 'domains', 'droplets', 'firewalls',
                     'floatingips', 'functions', 'images', 'kubernetes', 'loadbalancers', 'regions', 'reservedips',
                     'snapshots', 'sshkeys', 'tags', 'uptime', 'vpcs']

    token = profile['digitalocean_token']

    if resourceType == "all":
        return_dict["ResourceInfo"] = getAllResourceInfo(token)

    elif resourceType in RESOURCETYPES:
        return_dict["ResourceInfo"] = getResourceInfo(resourceType, token)

    else:
        return {"error": "RESOURCE-TYPE can only be one of the values: accounts, projects, actions, apps, "
                         "billing, blockstorage, cdn, certificates, containerregistry, databases, domains, droplets, "
                         "firewalls, floatingips, functions, images, kubernetes, loadbalancers, regions, reservedips, "
                         "snapshots, sshkeys, tags, uptime, vpcs or all for all resources."}

    return {
        "ResourceType": return_dict
    }, 200


def getResourceInfo(resourceType, token):
    if resourceType == "1clicks":
        return get1clicksResourceInfo(token)

    if resourceType == "accounts":
        return getAccountsResourceInfo(token)

    if resourceType == "projects":
        return getProjectsResourceInfo(token)

    if resourceType == "actions":
        return getActionsResourceInfo(token)

    if resourceType == "apps":
        return getAppsResourceInfo(token)

    if resourceType == "blockstorage":
        return getBlockstorageResourceInfo(token)

    if resourceType == "cdn":
        return getCdnResourceInfo(token)

    if resourceType == "certificates":
        return getCertificatesResourceInfo(token)

    if resourceType == "containerregistry":
        return getContainerregistryResourceInfo(token)

    if resourceType == "databases":
        return getDatabasesResourceInfo(token)

    if resourceType == "domains":
        return getDomainsResourceInfo(token)

    if resourceType == "droplets":
        return getDropletsResourceInfo(token)

    if resourceType == "firewalls":
        return getFirewallsResourceInfo(token)

    if resourceType == "floatingips":
        return getFloatingipsResourceInfo(token)

    if resourceType == "functions":
        return getFunctionsResourceInfo(token)

    if resourceType == "images":
        return getImagesResourceInfo(token)

    if resourceType == "kubernetes":
        return getKubernetesResourceInfo(token)

    if resourceType == "loadbalancers":
        return getLoadbalancersResourceInfo(token)

    if resourceType == "regions":
        return getRegionsResourceInfo(token)

    if resourceType == "reservedips":
        return getReservedipsResourceInfo(token)

    if resourceType == "snapshots":
        return getSnapshotsResourceInfo(token)

    if resourceType == "sshkeys":
        return getSshkeysResourceInfo(token)

    if resourceType == "tags":
        return getTagsResourceInfo(token)

    if resourceType == "uptime":
        return getUptimeResourceInfo(token)

    if resourceType == "vpcs":
        return getVpcsResourceInfo(token)


def runDOAPICalls(token, method, apiendpoint):
    if method == "GET":
        return requests.get(
            f"https://api.digitalocean.com/v2/{apiendpoint}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
    if method == "POST":
        if method == "GET":
            return requests.post(
                f"https://api.digitalocean.com/v2/{apiendpoint}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
    if method == "PUT":
        if method == "GET":
            return requests.put(
                f"https://api.digitalocean.com/v2/{apiendpoint}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
    if method == "PATCH":
        if method == "GET":
            return requests.patch(
                f"https://api.digitalocean.com/v2/{apiendpoint}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
    if method == "DELETE":
        if method == "GET":
            return requests.delete(
                f"https://api.digitalocean.com/v2/{apiendpoint}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )

def get1clicksResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "1-clicks")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "1_clicks" in infoRetrieved.json():
            return infoRetrieved.json()['1_clicks']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text

def getAccountsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "account")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "account" in infoRetrieved.json():
            return infoRetrieved.json()['account']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getProjectsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "projects")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "projects" in infoRetrieved.json():
            return infoRetrieved.json()['projects']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getActionsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "actions")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "actions" in infoRetrieved.json():
            return infoRetrieved.json()['actions']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getAppsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "apps")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "apps" in infoRetrieved.json():
            return infoRetrieved.json()['apps']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getBlockstorageResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "volumes")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "volumes" in infoRetrieved.json():
            return infoRetrieved.json()['volumes']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getCdnResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "cdn/endpoints")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "endpoints" in infoRetrieved.json():
            return infoRetrieved.json()['endpoints']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getCertificatesResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "certificates")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "certificates" in infoRetrieved.json():
            return infoRetrieved.json()['certificates']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getContainerregistryResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "registry")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "registry" in infoRetrieved.json():
            if infoRetrieved.json()['registry'] is not None:
                registryInfo = infoRetrieved.json()['registry']
                repoinfoRetrieved = runDOAPICalls(token, "GET", f"registry/{registryInfo['name']}/repositoriesV2")
                if repoinfoRetrieved.status_code == 200:
                    if "repositories" in repoinfoRetrieved.json():
                        registryInfo['repos'] = repoinfoRetrieved.json()

                dockerCreds = runDOAPICalls(token, "GET", f"registry/docker-credentials")

                if dockerCreds.status_code == 200:

                    registryInfo['docker-credentials'] = dockerCreds.json()

                registryOptions = runDOAPICalls(token, "GET", f"registry/options")
                if registryOptions.status_code == 200:
                    registryInfo['options'] = registryOptions.json()

                registrysubscription = runDOAPICalls(token, "GET", f"registry/subscription")
                if registrysubscription.status_code == 200:
                    registryInfo['subscription'] = registrysubscription.json()

                return registryInfo
            return []
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 404 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getDatabasesResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "databases")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "databases" in infoRetrieved.json():
            return infoRetrieved.json()['databases']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getDomainsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "domains")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "domains" in infoRetrieved.json():
            domainInfo = infoRetrieved.json()['domains']
            if domainInfo is not None:
                if len(domainInfo) > 0:
                    for domain in domainInfo:
                        domainname = domain["name"]
                        domain['records'] = []
                        recordinforetrieved = runDOAPICalls(token, "GET", f"domains/{domainname}/records")
                        if recordinforetrieved.status_code == 200:
                            domain['records'] = recordinforetrieved.json()['domain_records']
                return domainInfo
            return []
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getDropletsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "droplets")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "droplets" in infoRetrieved.json():
            if "account" in infoRetrieved.json():
                return infoRetrieved.json()['droplets']
            else:
                return []
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getFirewallsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "firewalls")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "firewalls" in infoRetrieved.json():
            return infoRetrieved.json()['firewalls']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getFloatingipsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "floating_ips")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "floating_ips" in infoRetrieved.json():
            return infoRetrieved.json()['floating_ips']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getFunctionsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "functions/namespaces")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "namespaces" in infoRetrieved.json():
            functionInfo = infoRetrieved.json()['namespaces']
            if functionInfo is not None:
                if len(functionInfo) > 0:
                    for function in functionInfo:
                        triggerinfoRetrieved = runDOAPICalls(token, "GET", f"functions/namespaces/{function['namespace']}/triggers")
                        if triggerinfoRetrieved.status_code == 200:
                            function['triggers'] = triggerinfoRetrieved.json()['triggers']
                return infoRetrieved.json()['namespaces']
            return []
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getImagesResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "images")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "images" in infoRetrieved.json():
            return infoRetrieved.json()['images']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getKubernetesResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "kubernetes/clusters")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "kubernetes_clusters" in infoRetrieved.json():
            return infoRetrieved.json()['kubernetes_clusters']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getLoadbalancersResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "load_balancers")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "load_balancers" in infoRetrieved.json():
            return infoRetrieved.json()['load_balancers']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getRegionsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "regions")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "regions" in infoRetrieved.json():
            return infoRetrieved.json()['regions']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getReservedipsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "reserved_ips")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "reserved_ips" in infoRetrieved.json():
            return infoRetrieved.json()['reserved_ips']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getSnapshotsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "snapshots")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "snapshots" in infoRetrieved.json():
            return infoRetrieved.json()['snapshots']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getSshkeysResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "account/keys")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "ssh_keys" in infoRetrieved.json():
            return infoRetrieved.json()['ssh_keys']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getTagsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "tags")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "tags" in infoRetrieved.json():
            return infoRetrieved.json()['tags']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getUptimeResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "uptime/checks")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "checks" in infoRetrieved.json():
            return infoRetrieved.json()['checks']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getVpcsResourceInfo(token):
    infoRetrieved = runDOAPICalls(token, "GET", "vpcs")
    if infoRetrieved.status_code == 403:
        return "Forbidden: You are not authorized to perform this operation"

    if infoRetrieved.status_code == 200:
        if "vpcs" in infoRetrieved.json():
            return infoRetrieved.json()['vpcs']
        else:
            return []
    elif infoRetrieved.status_code == 401 or \
            infoRetrieved.status_code == 429 or \
            infoRetrieved.status_code == 500:
        return infoRetrieved.json()
    else:
        return infoRetrieved.text


def getAllResourceInfo(token):
    return_dict = {"Accounts": getAccountsResourceInfo(token),
                   "Projects": getProjectsResourceInfo(token), "Actions": getActionsResourceInfo(token),
                   "Apps": getAppsResourceInfo(token),
                   "Blockstorage": getBlockstorageResourceInfo(token), "Cdn": getCdnResourceInfo(token),
                   "Certificates": getCertificatesResourceInfo(token),
                   "Containerregistry": getContainerregistryResourceInfo(token), "Databases": getDatabasesResourceInfo(token),
                   "Domains": getDomainsResourceInfo(token), "Droplets": getDropletsResourceInfo(token),
                   "Firewalls": getFirewallsResourceInfo(token), "Floatingips": getFloatingipsResourceInfo(token),
                   "Functions": getFunctionsResourceInfo(token), "Images": getImagesResourceInfo(token),
                   "Kubernetes": getKubernetesResourceInfo(token), "Loadbalancers": getLoadbalancersResourceInfo(token),
                   "Regions": getRegionsResourceInfo(token), "Reservedips": getReservedipsResourceInfo(token),
                   "Snapshots": getSnapshotsResourceInfo(token), "Sshkeys": getSshkeysResourceInfo(token),
                   "Tags": getTagsResourceInfo(token), "Uptime": getUptimeResourceInfo(token), "Vpcs": getVpcsResourceInfo(token)}
    return return_dict