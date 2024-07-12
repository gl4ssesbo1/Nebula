import boto3
from termcolor import colored
from datetime import datetime
import json
from pydoc import pipepager

'''
    If you want to be recognized about your contribution, you can add your name/nickname and contacts here. It will be outputed when user types "options".
'''
author = {
    "name": "",
    "twitter": "",
    "github": "",
    "email": ""
}

needs_creds = False

variables = {
    "SERVICE": {
        "value": "none",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "DOMAIN": {
        "value": "",
        "required": "true",
        "description": "Target's domain. From here, you'll get the whole basename."
    },
    "COUNTRY_CODE": {
        "value": "",
        "required": "true",
        "description": "Target's country. Needed to get the Country Code."
    }
}
description = "Description of your Module"

aws_command = "None"


def exploit(workspace):
    domain = variables['DOMAIN']['value']

    country_code = variables['COUNTRY_CODE']['value']

    country_code.upper()

    try:
        country = COUNTRIES[country_code]

    except KeyError:
        return {"error": {"error": "Country does not exist or is incorrect!"}}

    return generate_basename(domain, country, country_code.capitalize())


COUNTRIES = {'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'WF': 'Wallis and Futuna', 'BL': 'Saint Barthelemy', 'BM': 'Bermuda', 'BN': 'Brunei', 'BO': 'Bolivia', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BT': 'Bhutan', 'JM': 'Jamaica', 'BV': 'Bouvet Island', 'BW': 'Botswana', 'WS': 'Samoa', 'BQ': 'Bonaire, Saint Eustatius and Saba ', 'BR': 'Brazil', 'BS': 'Bahamas', 'JE': 'Jersey', 'BY': 'Belarus', 'BZ': 'Belize', 'RU': 'Russia', 'RW': 'Rwanda', 'RS': 'Serbia', 'TL': 'East Timor', 'RE': 'Reunion', 'TM': 'Turkmenistan', 'TJ': 'Tajikistan', 'RO': 'Romania', 'TK': 'Tokelau', 'GW': 'Guinea-Bissau', 'GU': 'Guam', 'GT': 'Guatemala', 'GS': 'South Georgia and the South Sandwich Islands', 'GR': 'Greece', 'GQ': 'Equatorial Guinea', 'GP': 'Guadeloupe', 'JP': 'Japan', 'GY': 'Guyana', 'GG': 'Guernsey', 'GF': 'French Guiana', 'GE': 'Georgia', 'GD': 'Grenada', 'GB': 'United Kingdom', 'GA': 'Gabon', 'SV': 'El Salvador', 'GN': 'Guinea', 'GM': 'Gambia', 'GL': 'Greenland', 'GI': 'Gibraltar', 'GH': 'Ghana', 'OM': 'Oman', 'TN': 'Tunisia', 'JO': 'Jordan', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'HK': 'Hong Kong', 'HN': 'Honduras', 'HM': 'Heard Island and McDonald Islands', 'VE': 'Venezuela', 'PR': 'Puerto Rico', 'PS': 'Palestinian Territory', 'PW': 'Palau', 'PT': 'Portugal', 'SJ': 'Svalbard and Jan Mayen', 'PY': 'Paraguay', 'IQ': 'Iraq', 'PA': 'Panama', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 'PE': 'Peru', 'PK': 'Pakistan', 'PH': 'Philippines', 'PN': 'Pitcairn', 'PL': 'Poland', 'PM': 'Saint Pierre and Miquelon', 'ZM': 'Zambia', 'EH': 'Western Sahara', 'EE': 'Estonia', 'EG': 'Egypt', 'ZA': 'South Africa', 'EC': 'Ecuador', 'IT': 'Italy', 'VN': 'Vietnam', 'SB': 'Solomon Islands', 'ET': 'Ethiopia', 'SO': 'Somalia', 'ZW': 'Zimbabwe', 'SA': 'Saudi Arabia', 'ES': 'Spain', 'ER': 'Eritrea', 'ME': 'Montenegro', 'MD': 'Moldova', 'MG': 'Madagascar', 'MF': 'Saint Martin', 'MA': 'Morocco', 'MC': 'Monaco', 'UZ': 'Uzbekistan', 'MM': 'Myanmar', 'ML': 'Mali', 'MO': 'Macao', 'MN': 'Mongolia', 'MH': 'Marshall Islands', 'MK': 'Macedonia', 'MU': 'Mauritius', 'MT': 'Malta', 'MW': 'Malawi', 'MV': 'Maldives', 'MQ': 'Martinique', 'MP': 'Northern Mariana Islands', 'MS': 'Montserrat', 'MR': 'Mauritania', 'IM': 'Isle of Man', 'UG': 'Uganda', 'TZ': 'Tanzania', 'MY': 'Malaysia', 'MX': 'Mexico', 'IL': 'Israel', 'FR': 'France', 'IO': 'British Indian Ocean Territory', 'SH': 'Saint Helena', 'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands', 'FM': 'Micronesia', 'FO': 'Faroe Islands', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NA': 'Namibia', 'VU': 'Vanuatu', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NZ': 'New Zealand', 'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'CK': 'Cook Islands', 'XK': 'Kosovo', 'CI': 'Ivory Coast', 'CH': 'Switzerland', 'CO': 'Colombia', 'CN': 'China', 'CM': 'Cameroon', 'CL': 'Chile', 'CC': 'Cocos Islands', 'CA': 'Canada', 'CG': 'Republic of the Congo', 'CF': 'Central African Republic', 'CD': 'Democratic Republic of the Congo', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'CX': 'Christmas Island', 'CR': 'Costa Rica', 'CW': 'Curacao', 'CV': 'Cape Verde', 'CU': 'Cuba', 'SZ': 'Swaziland', 'SY': 'Syria', 'SX': 'Sint Maarten', 'KG': 'Kyrgyzstan', 'KE': 'Kenya', 'SS': 'South Sudan', 'SR': 'Suriname', 'KI': 'Kiribati', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 'KM': 'Comoros', 'ST': 'Sao Tome and Principe', 'SK': 'Slovakia', 'KR': 'South Korea', 'SI': 'Slovenia', 'KP': 'North Korea', 'KW': 'Kuwait', 'SN': 'Senegal', 'SM': 'San Marino', 'SL': 'Sierra Leone', 'SC': 'Seychelles', 'KZ': 'Kazakhstan', 'KY': 'Cayman Islands', 'SG': 'Singapore', 'SE': 'Sweden', 'SD': 'Sudan', 'DO': 'Dominican Republic', 'DM': 'Dominica', 'DJ': 'Djibouti', 'DK': 'Denmark', 'VG': 'British Virgin Islands', 'DE': 'Germany', 'YE': 'Yemen', 'DZ': 'Algeria', 'US': 'United States', 'UY': 'Uruguay', 'YT': 'Mayotte', 'UM': 'United States Minor Outlying Islands', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LA': 'Laos', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TT': 'Trinidad and Tobago', 'TR': 'Turkey', 'LK': 'Sri Lanka', 'LI': 'Liechtenstein', 'LV': 'Latvia', 'TO': 'Tonga', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LR': 'Liberia', 'LS': 'Lesotho', 'TH': 'Thailand', 'TF': 'French Southern Territories', 'TG': 'Togo', 'TD': 'Chad', 'TC': 'Turks and Caicos Islands', 'LY': 'Libya', 'VA': 'Vatican', 'VC': 'Saint Vincent and the Grenadines', 'AE': 'United Arab Emirates', 'AD': 'Andorra', 'AG': 'Antigua and Barbuda', 'AF': 'Afghanistan', 'AI': 'Anguilla', 'VI': 'U.S. Virgin Islands', 'IS': 'Iceland', 'IR': 'Iran', 'AM': 'Armenia', 'AL': 'Albania', 'AO': 'Angola', 'AQ': 'Antarctica', 'AS': 'American Samoa', 'AR': 'Argentina', 'AU': 'Australia', 'AT': 'Austria', 'AW': 'Aruba', 'IN': 'India', 'AX': 'Aland Islands', 'AZ': 'Azerbaijan', 'IE': 'Ireland', 'ID': 'Indonesia', 'UA': 'Ukraine', 'QA': 'Qatar', 'MZ': 'Mozambique'}


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

    basenames.append("{}{}prod".format(domain.replace(".",""),country))
    basenames.append("{}{}prod".format(domain.replace(".",""),country_code))

    basenames.append("{}{}prod".format(domain.replace(".", "-"), country))
    basenames.append("{}{}prod".format(domain.replace(".", "-"), country_code))

    basenames.append("{}{}prod".format(domain.replace(".", "_"), country))
    basenames.append("{}{}prod".format(domain.replace(".", "_"), country_code))


    return {"Domain": {"Domain": domain, "Basenames": basenames}}
