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
        return {"error": "Country does not exist or is incorrect!"}

    return generate_basename(domain, country, country_code.capitalize())


COUNTRIES = {'Bangladesh': 'BD', 'Belgium': 'BE', 'Burkina Faso': 'BF', 'Bulgaria': 'BG',
             'Bosnia and Herzegovina': 'BA', 'Barbados': 'BB', 'Wallis and Futuna': 'WF', 'Saint Barthelemy': 'BL',
             'Bermuda': 'BM', 'Brunei': 'BN', 'Bolivia': 'BO', 'Bahrain': 'BH', 'Burundi': 'BI', 'Benin': 'BJ',
             'Bhutan': 'BT', 'Jamaica': 'JM', 'Bouvet Island': 'BV', 'Botswana': 'BW', 'Samoa': 'WS',
             'Bonaire, Saint Eustatius and Saba ': 'BQ', 'Brazil': 'BR', 'Bahamas': 'BS', 'Jersey': 'JE',
             'Belarus': 'BY', 'Belize': 'BZ', 'Russia': 'RU', 'Rwanda': 'RW', 'Serbia': 'RS', 'East Timor': 'TL',
             'Reunion': 'RE', 'Turkmenistan': 'TM', 'Tajikistan': 'TJ', 'Romania': 'RO', 'Tokelau': 'TK',
             'Guinea-Bissau': 'GW', 'Guam': 'GU', 'Guatemala': 'GT',
             'South Georgia and the South Sandwich Islands': 'GS', 'Greece': 'GR', 'Equatorial Guinea': 'GQ',
             'Guadeloupe': 'GP', 'Japan': 'JP', 'Guyana': 'GY', 'Guernsey': 'GG', 'French Guiana': 'GF',
             'Georgia': 'GE', 'Grenada': 'GD', 'United Kingdom': 'GB', 'Gabon': 'GA', 'El Salvador': 'SV',
             'Guinea': 'GN', 'Gambia': 'GM', 'Greenland': 'GL', 'Gibraltar': 'GI', 'Ghana': 'GH', 'Oman': 'OM',
             'Tunisia': 'TN', 'Jordan': 'JO', 'Croatia': 'HR', 'Haiti': 'HT', 'Hungary': 'HU', 'Hong Kong': 'HK',
             'Honduras': 'HN', 'Heard Island and McDonald Islands': 'HM', 'Venezuela': 'VE', 'Puerto Rico': 'PR',
             'Palestinian Territory': 'PS', 'Palau': 'PW', 'Portugal': 'PT', 'Svalbard and Jan Mayen': 'SJ',
             'Paraguay': 'PY', 'Iraq': 'IQ', 'Panama': 'PA', 'French Polynesia': 'PF', 'Papua New Guinea': 'PG',
             'Peru': 'PE', 'Pakistan': 'PK', 'Philippines': 'PH', 'Pitcairn': 'PN', 'Poland': 'PL',
             'Saint Pierre and Miquelon': 'PM', 'Zambia': 'ZM', 'Western Sahara': 'EH', 'Estonia': 'EE', 'Egypt': 'EG',
             'South Africa': 'ZA', 'Ecuador': 'EC', 'Italy': 'IT', 'Vietnam': 'VN', 'Solomon Islands': 'SB',
             'Ethiopia': 'ET', 'Somalia': 'SO', 'Zimbabwe': 'ZW', 'Saudi Arabia': 'SA', 'Spain': 'ES', 'Eritrea': 'ER',
             'Montenegro': 'ME', 'Moldova': 'MD', 'Madagascar': 'MG', 'Saint Martin': 'MF', 'Morocco': 'MA',
             'Monaco': 'MC', 'Uzbekistan': 'UZ', 'Myanmar': 'MM', 'Mali': 'ML', 'Macao': 'MO', 'Mongolia': 'MN',
             'Marshall Islands': 'MH', 'Macedonia': 'MK', 'Mauritius': 'MU', 'Malta': 'MT', 'Malawi': 'MW',
             'Maldives': 'MV', 'Martinique': 'MQ', 'Northern Mariana Islands': 'MP', 'Montserrat': 'MS',
             'Mauritania': 'MR', 'Isle of Man': 'IM', 'Uganda': 'UG', 'Tanzania': 'TZ', 'Malaysia': 'MY',
             'Mexico': 'MX', 'Israel': 'IL', 'France': 'FR', 'British Indian Ocean Territory': 'IO',
             'Saint Helena': 'SH', 'Finland': 'FI', 'Fiji': 'FJ', 'Falkland Islands': 'FK', 'Micronesia': 'FM',
             'Faroe Islands': 'FO', 'Nicaragua': 'NI', 'Netherlands': 'NL', 'Norway': 'NO', 'Namibia': 'NA',
             'Vanuatu': 'VU', 'New Caledonia': 'NC', 'Niger': 'NE', 'Norfolk Island': 'NF', 'Nigeria': 'NG',
             'New Zealand': 'NZ', 'Nepal': 'NP', 'Nauru': 'NR', 'Niue': 'NU', 'Cook Islands': 'CK', 'Kosovo': 'XK',
             'Ivory Coast': 'CI', 'Switzerland': 'CH', 'Colombia': 'CO', 'China': 'CN', 'Cameroon': 'CM', 'Chile': 'CL',
             'Cocos Islands': 'CC', 'Canada': 'CA', 'Republic of the Congo': 'CG', 'Central African Republic': 'CF',
             'Democratic Republic of the Congo': 'CD', 'Czech Republic': 'CZ', 'Cyprus': 'CY', 'Christmas Island': 'CX',
             'Costa Rica': 'CR', 'Curacao': 'CW', 'Cape Verde': 'CV', 'Cuba': 'CU', 'Swaziland': 'SZ', 'Syria': 'SY',
             'Sint Maarten': 'SX', 'Kyrgyzstan': 'KG', 'Kenya': 'KE', 'South Sudan': 'SS', 'Suriname': 'SR',
             'Kiribati': 'KI', 'Cambodia': 'KH', 'Saint Kitts and Nevis': 'KN', 'Comoros': 'KM',
             'Sao Tome and Principe': 'ST', 'Slovakia': 'SK', 'South Korea': 'KR', 'Slovenia': 'SI',
             'North Korea': 'KP', 'Kuwait': 'KW', 'Senegal': 'SN', 'San Marino': 'SM', 'Sierra Leone': 'SL',
             'Seychelles': 'SC', 'Kazakhstan': 'KZ', 'Cayman Islands': 'KY', 'Singapore': 'SG', 'Sweden': 'SE',
             'Sudan': 'SD', 'Dominican Republic': 'DO', 'Dominica': 'DM', 'Djibouti': 'DJ', 'Denmark': 'DK',
             'British Virgin Islands': 'VG', 'Germany': 'DE', 'Yemen': 'YE', 'Algeria': 'DZ', 'United States': 'US',
             'Uruguay': 'UY', 'Mayotte': 'YT', 'United States Minor Outlying Islands': 'UM', 'Lebanon': 'LB',
             'Saint Lucia': 'LC', 'Laos': 'LA', 'Tuvalu': 'TV', 'Taiwan': 'TW', 'Trinidad and Tobago': 'TT',
             'Turkey': 'TR', 'Sri Lanka': 'LK', 'Liechtenstein': 'LI', 'Latvia': 'LV', 'Tonga': 'TO', 'Lithuania': 'LT',
             'Luxembourg': 'LU', 'Liberia': 'LR', 'Lesotho': 'LS', 'Thailand': 'TH',
             'French Southern Territories': 'TF', 'Togo': 'TG', 'Chad': 'TD', 'Turks and Caicos Islands': 'TC',
             'Libya': 'LY', 'Vatican': 'VA', 'Saint Vincent and the Grenadines': 'VC', 'United Arab Emirates': 'AE',
             'Andorra': 'AD', 'Antigua and Barbuda': 'AG', 'Afghanistan': 'AF', 'Anguilla': 'AI',
             'U.S. Virgin Islands': 'VI', 'Iceland': 'IS', 'Iran': 'IR', 'Armenia': 'AM', 'Albania': 'AL',
             'Angola': 'AO', 'Antarctica': 'AQ', 'American Samoa': 'AS', 'Argentina': 'AR', 'Australia': 'AU',
             'Austria': 'AT', 'Aruba': 'AW', 'India': 'IN', 'Aland Islands': 'AX', 'Azerbaijan': 'AZ', 'Ireland': 'IE',
             'Indonesia': 'ID', 'Ukraine': 'UA', 'Qatar': 'QA', 'Mozambique': 'MZ'}


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
