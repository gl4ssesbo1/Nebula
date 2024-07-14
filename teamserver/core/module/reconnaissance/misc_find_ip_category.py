import ipaddress
import re
import sys

from dns import resolver

from __ip_source.AWS_IP_Ranges import AWS_IP_RANGE
from __ip_source.Azure_IP_Ranges import AZURE_IP_RANGE
from __ip_source.DOIPRange import DOIPRange
from __ip_source.GCP_IP_Ranges import GCP_IP_RANGE

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "IP-FILE": {
        "value": "",
        "required": "true",
        "description": "The path of the file with the IPs (IPv4 and IPv6) or Domain Name to test.",
        "iswordlist": True,
        "wordlistvalue": []
    }
}

description = "Checks for subdomains of the domain by enumerating certificates from crt.sh"
aws_command = "None"


def exploit(workspace):
    IPv4_REGEX = "^[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}[.]{1}[0-9]{1,3}$"
    IPv6_REGEX = "^([0-9a-fA-F]{1,4}[:]{0,2}){1,8}$"

    ipfilename = variables['IP-FILE']['value']
    ipfile = variables['IP-FILE']['wordlistvalue']
    all_domain = []
    all_ips = []

    split_by_services = {
        "IP-FILE": ipfilename,
        "Vendors": {
            "AWS": [],
            "AZURE": [],
            "GCP": [],
            "DigitalOcean": [],
            "NoVendor": []
        }
    }

    try:
        for ip in ipfile:
            if re.match(IPv4_REGEX, ip.strip()):
                all_ips.append(ip.strip())

            elif re.match(IPv6_REGEX, ip.strip()):
                all_ips.append(ip.strip())

            else:
                all_domain.append(ip.strip())

        for d in all_domain:
            singlehost = {
                "Host": d,
                "Resolved": "",
                "Region": "",
                "Service": ""
            }
            try:
                resolved_domain = resolver.resolve(d, 'CNAME')[0].to_text()
                singlehost["Resolved"] = resolved_domain
                vendor = findDomainVendor(resolved_domain)
                if vendor is not None:
                    singlehost["Region"] = vendor[1]
                    singlehost["Service"] = vendor[2]
                    split_by_services["Vendors"][vendor[0]].append(singlehost)

                else:
                    split_by_services["Vendors"]["NoVendor"].append(singlehost)

            except resolver.NoAnswer:
                try:
                    resolved_domain = resolver.resolve(d, 'A')[0].to_text()

                    singlehost["Resolved"] = resolved_domain
                    vendor = findIPVendor(resolved_domain)

                    if vendor is not None:
                        if vendor[0] == "DigitalOcean":
                            singlehost["Service"] = "droplet"
                        else:
                            singlehost["Service"] = vendor[2]
                        singlehost["Region"] = vendor[1]
                        split_by_services["Vendors"][vendor[0]].append(singlehost)

                    else:
                        split_by_services["Vendors"]["NoVendor"].append(singlehost)

                except resolver.NoAnswer:
                    resolved_domain = resolver.resolve(d, 'AAAA')[0].to_text()
                    singlehost["Resolved"] = resolved_domain
                    vendor = findIPVendor(resolved_domain)
                    if vendor is not None:
                        if vendor[0] == "DigitalOcean":
                            singlehost["Service"] = "droplet"
                        else:
                            singlehost["Service"] = vendor[2]
                        singlehost["Region"] = vendor[1]
                        singlehost["Service"] = vendor[2]
                        split_by_services["Vendors"][vendor[0]].append(singlehost)

                    else:
                        split_by_services["Vendors"]["NoVendor"].append(singlehost)

            except resolver.NXDOMAIN:
                singlehost["Resolved"] = "Noresolve"
                singlehost["Service"] = None

                split_by_services["Vendors"]["NoVendor"].append(singlehost)

        for i in all_ips:
            singlehost = {
                "Host": i,
                "Resolved": i,
                "Region": "",
                "Service": ""
            }
            try:
                vendor = findIPVendor(i)
                if vendor is not None:
                    singlehost["Region"] = vendor[1]
                    singlehost["Service"] = vendor[2]
                    split_by_services["Vendors"][vendor[0]].append(singlehost)

                else:
                    split_by_services["Vendors"]["NoVendor"].append(singlehost)

            except Exception as e:
                singlehost["Resolved"] = "Noresolve"
                singlehost["Service"] = None

                split_by_services["Vendors"]["NoVendor"].append(singlehost)



        return {
            "IP-FILE": split_by_services
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def findDomainVendor(host):
    if "amazonaws.com" in host:
        return findAWSService(resolver.resolve(host, 'A')[0].to_text())
    elif "azure" in host or "windows" in host:
        return findAzureService(resolver.resolve(host, 'A')[0].to_text())
    elif "google" in host:
        return findGCPService(resolver.resolve(host, 'A')[0].to_text())
    elif "digitalocean" in host:
        servicelist = findDODomain(host)
        if servicelist[1] is None:
            region = findDOService(resolver.resolve(host, 'A')[0].to_text())
            if region is not None:
                servicelist[1] = region[1]
        return servicelist
    else:
        return None

def findDODomain(host):
    if "digitaloceanspaces.com" in host:
        return ["DigitalOcean", host.split(".")[1], "space"]
    elif "k8s.ondigitalocean.com" in host:
        return ["DigitalOcean", None, "kube"]
    elif "doserverless.co" in host:
        return ["DigitalOcean", host.split("-")[1], "function"]
    elif "ondigitalocean.com" in host:
        return ["DigitalOcean", host.split("-")[2], "database"]
    elif "ondigitalocean.app" in host:
        return ["DigitalOcean", None, "app"]
    elif "registry.digitalocean.com/crbsides" in host:
        return ["DigitalOcean", None, "app"]

def findIPVendor(host):
    awsservice = findAWSService(host)
    if awsservice is not None:
        return awsservice

    azureService = findAzureService(host)
    if azureService is not None:
        return azureService

    gcpService = findGCPService(host)
    if gcpService is not None:
        return gcpService

    doService = findDOService(host)
    if doService is not None:
        return doService

    return None

def findGCPService(host):
    an_address = ipaddress.ip_address(host)
    for gcpIP in GCP_IP_RANGE:
        if "ipv6Prefix" in gcpIP:
            gcpnetwork = gcpIP['ipv6Prefix']
        else:
            gcpnetwork = gcpIP['ipv4Prefix']

        if an_address in ipaddress.ip_network(gcpnetwork):
            return ["GCP", gcpIP['region'], gcpIP["service"]]
    return None


def findAzureService(host):
    an_address = ipaddress.ip_address(host)
    for azIPJSON in AZURE_IP_RANGE:
        for azIP in azIPJSON['properties']['addressPrefixes']:
            if an_address in ipaddress.ip_network(azIP):
                if azIPJSON['properties']['region'] == "":
                    return ["AZURE", "global", azIPJSON["name"].split(",")[0]]

                return ["AZURE", azIPJSON['properties']['region'], azIPJSON["name"].split(",")[0]]
    return None


def findDOService(host):
    an_address = ipaddress.ip_address(host)
    for doIP in DOIPRange:
        if an_address in ipaddress.ip_network(doIP['IPRange']):
            return ["DigitalOcean", doIP["Location"], None]
    return None


def findAWSService(host):
    an_address = ipaddress.ip_address(host)

    for ip4 in AWS_IP_RANGE['prefixes']:
        if "ip_prefix" in ip4:
            if an_address in ipaddress.ip_network(ip4["ip_prefix"]):
                return ["AWS", ip4['region'], ip4['service']]
        else:
            if an_address in ipaddress.ip_network(ip4["ipv6_prefix"]):
                return ["AWS", ip4['region'], ip4['service']]
    return None
