from mongoengine import DoesNotExist
from termcolor import colored
import dns.resolver
import xml.etree.ElementTree as ET
from datetime import datetime
import os
from pydoc import pipepager
import sys
import urllib.request
from requests.exceptions import ConnectionError
from core.database import models
import flask_mongoengine

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
    "BASENAME": {
        "value": "",
        "required": "false",
        "description": "Either put this or DOMAIN AND COUNTRY. A single basename or several basenames spearated by comma."
    },
    "DOMAIN": {
        "value": "",
        "required": "false",
        "description": "The domain of the target. If you use this, you'll also need to add the target's COUNTRY."
    },
    "COUNTRY_CODE": {
        "value": "",
        "required": "false",
        "description": "The code of country the target operates in. If you use this, you'll also need to add the target's DOMAIN."
    }

}

description = "Gets the name of a basename or a list of basenames separated by comma (',') or domain and country and generates the wordlist and bruteforces the name of the services by sending DNS Requests to them."

aws_command = "No awscli command"


def exploit(workspace):
    objects = []
    basenames = {}

    dns_suffixes = {
        "azurewebsites.net": "App Services",
        "scm.azurewebsites.net": "App Services Management",
        "p.azurewebsites.net": "App Services",
        "cloudapp.net": "App Services",
        "file.core.windows.net": "Storage Accounts: Files",
        "blob.core.windows.net": "Storage Accounts: Blobs",
        "queue.core.windows.net": "Storage Accounts: Queues",
        "table.core.windows.net": "Storage Accounts - Tables",
        "redis.cache.windows.net": "Databases - Redis",
        "documents.azure.com": "Databases - Cosmos DB",
        "database.windows.net": "Databases - MSSQL",
        "vault.azure.net": "Key Vaults",
        "onmicrosoft.com": "Microsoft Hosted Domain",
        "mail.protection.outlook.com": "Email",
        "sharepoint.com": "SharePoint",
        "azureedge.net": "CDN",
        "search.windows.net": "Search Appliance",
        "azure-api.net": "API Services",
        "atp.azure.com": "Advanced Threat Protection"
    }

    '''
    dns_suffixes = [
        "azurewebsites.net",
        "scm.azurewebsites.net",
        "p.azurewebsites.net",
        "cloudapp.net",
        "file.core.windows.net",
        "blob.core.windows.net",
        "queue.core.windows.net",
        "table.core.windows.net",
        "redis.cache.windows.net",
        "documents.azure.com",
        "database.windows.net",
        "vault.azure.net",
        "onmicrosoft.com",
        "mail.protection.outlook.com",
        "sharepoint.com",
        "azureedge.net",
        "search.windows.net",
        "azure-api.net"
    ]
    '''

    try:
        if variables['DOMAIN']['value'] == "" and variables['BASENAME']['value'] == "" and variables['COUNTRY_CODE'][
            'value'] == "":
            return {"error": "[*] Either enter Basenames or Targets Domain and Country!"}

        elif variables['DOMAIN']['value'] != "" and variables['BASENAME']['value'] == "":
            if variables['COUNTRY_CODE']['value'] == "":
                return {"error": "[*] Please enter country name too!"}
            else:
                domain = variables['DOMAIN']['value']
                country_code = variables['COUNTRY_CODE']['value']

                country_code.upper()

                try:
                    country = COUNTRIES[country_code]
                except KeyError:
                    return {"error": "[*] Country does not exist or is incorrect!"}

                all_basenameets = generate_basename(domain, country, country_code)['Domain']['Basenames']

                for basename in all_basenameets:
                    basename = basename.replace("\n", "").strip()
                    for dns_suffix, explanation in dns_suffixes.items():
                        try:
                            dns.resolver.resolve("{0}.{1}".format(basename, dns_suffix))
                            basenames["{0}.{1}".format(basename, dns_suffix)] = explanation
                        except Exception as e:
                            pass

                    if basenames == {}:
                        pass
                    else:
                        all_services = {
                            "azure_services_base_name": basename,
                            "azure_services_dns_list": basenames
                        }
                        objects.append(all_services)
                        basenames = {}

                        try:
                            models.AzureServices.objects().get(azure_services_base_name=basename).update(
                                **all_services)

                        except flask_mongoengine.DoesNotExist:
                            models.AzureServices(**all_services).save()
                        except Exception as e:
                            pass

                return {"azure_services_base_name": objects}, 200

        elif variables['BASENAME']['value'] != "":
            if variables['DOMAIN']['value'] != "" or variables['DOMAIN']['value'] != "":
                return {"error": "[*] Either enter Basenames or Targets Domain and Country!"}

            all_basenameets = variables['BASENAME']['value'].split(",")

            for basename in all_basenameets:
                basename = basename.replace("\n", "").strip()
                for dns_suffix, explanation in dns_suffixes.items():
                    try:
                        dns.resolver.resolve("{0}.{1}".format(basename, dns_suffix))
                        basenames["{0}.{1}".format(basename, dns_suffix)] = explanation
                    except Exception as e:
                        pass

                if basenames == None:
                    pass
                else:
                    all_services = {
                        "azure_services_base_name": basename,
                        "azure_services_dns_list": basenames
                    }
                    objects.append(all_services)
                    basenames = {}

                    try:
                        models.AzureServices.objects().get(azure_services_base_name=basename).update(
                            **all_services)

                    except flask_mongoengine.DoesNotExist:
                        models.AzureServices(**all_services).save()
                    else:
                        pass

            return {"azure_services_base_name": objects}, 200
        else:
            return {"error": "[*] Please enter at least Basenames or Targets Domain and Country!"}, 404

    except Exception as e:
        return {"error": str(e)}, 500

COUNTRIES = {'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria',
             'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'WF': 'Wallis and Futuna', 'BL': 'Saint Barthelemy',
             'BM': 'Bermuda', 'BN': 'Brunei', 'BO': 'Bolivia', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin',
             'BT': 'Bhutan', 'JM': 'Jamaica', 'BV': 'Bouvet Island', 'BW': 'Botswana', 'WS': 'Samoa',
             'BQ': 'Bonaire, Saint Eustatius and Saba ', 'BR': 'Brazil', 'BS': 'Bahamas', 'JE': 'Jersey',
             'BY': 'Belarus', 'BZ': 'Belize', 'RU': 'Russia', 'RW': 'Rwanda', 'RS': 'Serbia', 'TL': 'East Timor',
             'RE': 'Reunion', 'TM': 'Turkmenistan', 'TJ': 'Tajikistan', 'RO': 'Romania', 'TK': 'Tokelau',
             'GW': 'Guinea-Bissau', 'GU': 'Guam', 'GT': 'Guatemala',
             'GS': 'South Georgia and the South Sandwich Islands', 'GR': 'Greece', 'GQ': 'Equatorial Guinea',
             'GP': 'Guadeloupe', 'JP': 'Japan', 'GY': 'Guyana', 'GG': 'Guernsey', 'GF': 'French Guiana',
             'GE': 'Georgia', 'GD': 'Grenada', 'GB': 'United Kingdom', 'GA': 'Gabon', 'SV': 'El Salvador',
             'GN': 'Guinea', 'GM': 'Gambia', 'GL': 'Greenland', 'GI': 'Gibraltar', 'GH': 'Ghana', 'OM': 'Oman',
             'TN': 'Tunisia', 'JO': 'Jordan', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'HK': 'Hong Kong',
             'HN': 'Honduras', 'HM': 'Heard Island and McDonald Islands', 'VE': 'Venezuela', 'PR': 'Puerto Rico',
             'PS': 'Palestinian Territory', 'PW': 'Palau', 'PT': 'Portugal', 'SJ': 'Svalbard and Jan Mayen',
             'PY': 'Paraguay', 'IQ': 'Iraq', 'PA': 'Panama', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea',
             'PE': 'Peru', 'PK': 'Pakistan', 'PH': 'Philippines', 'PN': 'Pitcairn', 'PL': 'Poland',
             'PM': 'Saint Pierre and Miquelon', 'ZM': 'Zambia', 'EH': 'Western Sahara', 'EE': 'Estonia', 'EG': 'Egypt',
             'ZA': 'South Africa', 'EC': 'Ecuador', 'IT': 'Italy', 'VN': 'Vietnam', 'SB': 'Solomon Islands',
             'ET': 'Ethiopia', 'SO': 'Somalia', 'ZW': 'Zimbabwe', 'SA': 'Saudi Arabia', 'ES': 'Spain', 'ER': 'Eritrea',
             'ME': 'Montenegro', 'MD': 'Moldova', 'MG': 'Madagascar', 'MF': 'Saint Martin', 'MA': 'Morocco',
             'MC': 'Monaco', 'UZ': 'Uzbekistan', 'MM': 'Myanmar', 'ML': 'Mali', 'MO': 'Macao', 'MN': 'Mongolia',
             'MH': 'Marshall Islands', 'MK': 'Macedonia', 'MU': 'Mauritius', 'MT': 'Malta', 'MW': 'Malawi',
             'MV': 'Maldives', 'MQ': 'Martinique', 'MP': 'Northern Mariana Islands', 'MS': 'Montserrat',
             'MR': 'Mauritania', 'IM': 'Isle of Man', 'UG': 'Uganda', 'TZ': 'Tanzania', 'MY': 'Malaysia',
             'MX': 'Mexico', 'IL': 'Israel', 'FR': 'France', 'IO': 'British Indian Ocean Territory',
             'SH': 'Saint Helena', 'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands', 'FM': 'Micronesia',
             'FO': 'Faroe Islands', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NA': 'Namibia',
             'VU': 'Vanuatu', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria',
             'NZ': 'New Zealand', 'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'CK': 'Cook Islands', 'XK': 'Kosovo',
             'CI': 'Ivory Coast', 'CH': 'Switzerland', 'CO': 'Colombia', 'CN': 'China', 'CM': 'Cameroon', 'CL': 'Chile',
             'CC': 'Cocos Islands', 'CA': 'Canada', 'CG': 'Republic of the Congo', 'CF': 'Central African Republic',
             'CD': 'Democratic Republic of the Congo', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'CX': 'Christmas Island',
             'CR': 'Costa Rica', 'CW': 'Curacao', 'CV': 'Cape Verde', 'CU': 'Cuba', 'SZ': 'Swaziland', 'SY': 'Syria',
             'SX': 'Sint Maarten', 'KG': 'Kyrgyzstan', 'KE': 'Kenya', 'SS': 'South Sudan', 'SR': 'Suriname',
             'KI': 'Kiribati', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 'KM': 'Comoros',
             'ST': 'Sao Tome and Principe', 'SK': 'Slovakia', 'KR': 'South Korea', 'SI': 'Slovenia',
             'KP': 'North Korea', 'KW': 'Kuwait', 'SN': 'Senegal', 'SM': 'San Marino', 'SL': 'Sierra Leone',
             'SC': 'Seychelles', 'KZ': 'Kazakhstan', 'KY': 'Cayman Islands', 'SG': 'Singapore', 'SE': 'Sweden',
             'SD': 'Sudan', 'DO': 'Dominican Republic', 'DM': 'Dominica', 'DJ': 'Djibouti', 'DK': 'Denmark',
             'VG': 'British Virgin Islands', 'DE': 'Germany', 'YE': 'Yemen', 'DZ': 'Algeria', 'US': 'United States',
             'UY': 'Uruguay', 'YT': 'Mayotte', 'UM': 'United States Minor Outlying Islands', 'LB': 'Lebanon',
             'LC': 'Saint Lucia', 'LA': 'Laos', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TT': 'Trinidad and Tobago',
             'TR': 'Turkey', 'LK': 'Sri Lanka', 'LI': 'Liechtenstein', 'LV': 'Latvia', 'TO': 'Tonga', 'LT': 'Lithuania',
             'LU': 'Luxembourg', 'LR': 'Liberia', 'LS': 'Lesotho', 'TH': 'Thailand',
             'TF': 'French Southern Territories', 'TG': 'Togo', 'TD': 'Chad', 'TC': 'Turks and Caicos Islands',
             'LY': 'Libya', 'VA': 'Vatican', 'VC': 'Saint Vincent and the Grenadines', 'AE': 'United Arab Emirates',
             'AD': 'Andorra', 'AG': 'Antigua and Barbuda', 'AF': 'Afghanistan', 'AI': 'Anguilla',
             'VI': 'U.S. Virgin Islands', 'IS': 'Iceland', 'IR': 'Iran', 'AM': 'Armenia', 'AL': 'Albania',
             'AO': 'Angola', 'AQ': 'Antarctica', 'AS': 'American Samoa', 'AR': 'Argentina', 'AU': 'Australia',
             'AT': 'Austria', 'AW': 'Aruba', 'IN': 'India', 'AX': 'Aland Islands', 'AZ': 'Azerbaijan', 'IE': 'Ireland',
             'ID': 'Indonesia', 'UA': 'Ukraine', 'QA': 'Qatar', 'MZ': 'Mozambique'}
def generate_basename(domain, country, country_code):
    basenames = []

    for bn in domain.split(".")[:-1]:
        basenames.append(bn)
        basenames.append("{}-prod".format(bn))
        basenames.append("{}-dev".format(bn))
        basenames.append("{}-test".format(bn))
        basenames.append("{}-my".format(bn))
        basenames.append("{}1-my".format(bn))
        basenames.append("{}2-my".format(bn))
        basenames.append("{}3-my".format(bn))
        basenames.append("{}4-my".format(bn))
        basenames.append("{}5-my".format(bn))

        basenames.append("{}-{}".format(bn, country))
        basenames.append("{}-{}".format(bn, country_code))

        basenames.append("{}-{}-my".format(bn, country))
        basenames.append("{}-{}-my".format(bn, country_code))

        basenames.append("{}_{}_my".format(bn, country))
        basenames.append("{}_{}_my".format(bn, country_code))

        basenames.append("{}_{}-my".format(bn, country))
        basenames.append("{}_{}-my".format(bn, country_code))

        basenames.append("{}-{}_my".format(bn, country))
        basenames.append("{}-{}_my".format(bn, country_code))

        basenames.append("{}_prod".format(bn))
        basenames.append("{}_dev".format(bn))
        basenames.append("{}_test".format(bn))
        basenames.append("{}_my".format(bn))
        basenames.append("{}-my".format(bn))
        basenames.append("{}1_my".format(bn))
        basenames.append("{}2_my".format(bn))
        basenames.append("{}3_my".format(bn))
        basenames.append("{}4_my".format(bn))
        basenames.append("{}5_my".format(bn))

    del bn

    basenames.append(domain.replace(".", ""))
    basenames.append(domain.replace(".", "-"))
    basenames.append(domain.replace(".", "_"))

    basenames.append("{}{}prod".format(domain.replace(".", ""), country))
    basenames.append("{}{}prod".format(domain.replace(".", ""), country_code))

    basenames.append("{}{}prod".format(domain.replace(".", "-"), country))
    basenames.append("{}{}prod".format(domain.replace(".", "-"), country_code))

    basenames.append("{}{}prod".format(domain.replace(".", "_"), country))
    basenames.append("{}{}prod".format(domain.replace(".", "_"), country_code))

    return {"Domain": {"Domain": domain, "Basenames": basenames}}
