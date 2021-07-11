import json
from datetime import datetime
import boto3
from termcolor import colored
import sys
import botocore

#SERVICES = ['accessanalyzer', 'acm', 'waiters', 'acmpca', 'waiters', 'alexaforbusiness', 'prometheusservice', 'amplify', 'amplifybackend', 'apigateway', 'apigatewaymanagementapi', 'apigatewayv2', 'appconfig', 'appflow', 'appintegrationsservice', 'applicationautoscaling', 'applicationinsights', 'applicationcostprofiler', 'appmesh', 'apprunner', 'appstream', 'waiters', 'appsync', 'athena', 'auditmanager', 'autoscaling', 'autoscalingplans', 'backup', 'batch', 'braket', 'budgets', 'costexplorer', 'chime', 'cloud9', 'clouddirectory', 'cloudformation', 'waiters', 'service resource', 'event', 'stack', 'stackresource', 'stackresourcesummary', 'cloudfront', 'waiters', 'examples', 'cloudhsm', 'cloudhsmv2', 'cloudsearch', 'cloudsearchdomain', 'cloudtrail', 'cloudwatch', 'waiters', 'service resource', 'alarm', 'metric', 'codeartifact', 'codebuild', 'codecommit', 'codedeploy', 'waiters', 'codegurureviewer', 'waiters', 'codeguruprofiler', 'codepipeline', 'codestar', 'codestarconnections', 'codestarnotifications', 'cognitoidentity', 'cognitoidentityprovider', 'cognitosync', 'comprehend', 'comprehendmedical', 'computeoptimizer', 'configservice', 'connect', 'connectcontactlens', 'connectparticipant', 'costandusagereportservice', 'customerprofiles', 'gluedatabrew', 'dataexchange', 'datapipeline', 'datasync', 'dax', 'detective', 'devicefarm', 'devopsguru', 'directconnect', 'applicationdiscoveryservice', 'dlm', 'databasemigrationservice', 'waiters', 'docdb', 'waiters', 'directoryservice', 'dynamodb', 'waiters', 'service resource', 'table', 'dynamodbstreams', 'ebs', 'ec2', 'waiters', 'service resource', 'classicaddress', 'dhcpoptions', 'image', 'instance', 'internetgateway', 'keypair', 'keypairinfo', 'networkacl', 'networkinterface', 'networkinterfaceassociation', 'placementgroup', 'route', 'routetable', 'routetableassociation', 'securitygroup', 'snapshot', 'subnet', 'tag', 'volume', 'vpc', 'vpcpeeringconnection', 'vpcaddress', 'ec2instanceconnect', 'ecr', 'waiters', 'ecrpublic', 'ecs', 'waiters', 'efs', 'eks', 'waiters', 'elasticinference', 'elasticache', 'waiters', 'elasticbeanstalk', 'waiters', 'elastictranscoder', 'waiters', 'elasticloadbalancing', 'waiters', 'elasticloadbalancingv2', 'waiters', 'emr', 'waiters', 'emrcontainers', 'elasticsearchservice', 'eventbridge', 'finspace', 'finspacedata', 'firehose', 'fis', 'fms', 'forecastservice', 'forecastqueryservice', 'frauddetector', 'fsx', 'gamelift', 'glacier', 'waiters', 'service resource', 'account', 'archive', 'job', 'multipartupload', 'notification', 'vault', 'globalaccelerator', 'glue', 'greengrass', 'greengrassv2', 'groundstation', 'guardduty', 'health', 'healthlake', 'honeycode', 'iam', 'waiters', 'service resource', 'accesskey', 'accesskeypair', 'accountpasswordpolicy', 'accountsummary', 'assumerolepolicy', 'currentuser', 'group', 'grouppolicy', 'instanceprofile', 'loginprofile', 'mfadevice', 'policy', 'policyversion', 'role', 'rolepolicy', 'samlprovider', 'servercertificate', 'signingcertificate', 'user', 'userpolicy', 'virtualmfadevice', 'identitystore', 'imagebuilder', 'importexport', 'inspector', 'iot', 'iotdataplane', 'iotjobsdataplane', 'iot1clickdevicesservice', 'iot1clickprojects', 'iotanalytics', 'iotdeviceadvisor', 'iotevents', 'ioteventsdata', 'iotfleethub', 'iotsecuretunneling', 'iotsitewise', 'waiters', 'iotthingsgraph', 'iotwireless', 'ivs', 'kafka', 'kendra', 'kinesis', 'waiters', 'kinesisvideoarchivedmedia', 'kinesisvideomedia', 'kinesisvideosignalingchannels', 'kinesisanalytics', 'kinesisanalyticsv2', 'kinesisvideo', 'kms', 'lakeformation', 'lambda', 'waiters', 'lexmodelbuildingservice', 'lexruntimeservice', 'lexmodelsv2', 'lexruntimev2', 'licensemanager', 'lightsail', 'locationservice', 'cloudwatchlogs', 'lookoutequipment', 'lookoutmetrics', 'lookoutforvision', 'machinelearning', 'waiters', 'macie', 'macie2', 'managedblockchain', 'marketplacecatalog', 'marketplaceentitlementservice', 'marketplacecommerceanalytics', 'mediaconnect', 'waiters', 'mediaconvert', 'medialive', 'waiters', 'mediapackage', 'mediapackagevod', 'mediastore', 'mediastoredata', 'mediatailor', 'marketplacemetering', 'migrationhub', 'mgn', 'migrationhubconfig', 'mobile', 'mq', 'mturk', 'mwaa', 'neptune', 'waiters', 'networkfirewall', 'networkmanager', 'nimblestudio', 'opsworks', 'waiters', 'service resource', 'layer', 'stack', 'stacksummary', 'opsworkscm', 'waiters', 'organizations', 'outposts', 'personalize', 'personalizeevents', 'personalizeruntime', 'pi', 'pinpoint', 'pinpointemail', 'pinpointsmsvoice', 'polly', 'pricing', 'proton', 'waiters', 'qldb', 'qldbsession', 'quicksight', 'ram', 'rds', 'waiters', 'rdsdataservice', 'redshift', 'waiters', 'redshiftdataapiservice', 'rekognition', 'waiters', 'resourcegroups', 'resourcegroupstaggingapi', 'robomaker', 'route53', 'waiters', 'route53domains', 'route53resolver', 's3', 'waiters', 'service resource', 'bucket', 'bucketacl', 'bucketcors', 'bucketlifecycle', 'bucketlifecycleconfiguration', 'bucketlogging', 'bucketnotification', 'bucketpolicy', 'bucketrequestpayment', 'buckettagging', 'bucketversioning', 'bucketwebsite', 'multipartupload', 'multipartuploadpart', 'object', 'objectacl', 'objectsummary', 'objectversion', 'examples', 's3control', 's3outposts', 'sagemaker', 'waiters', 'augmentedairuntime', 'sagemakeredgemanager', 'sagemakerfeaturestoreruntime', 'sagemakerruntime', 'savingsplans', 'schemas', 'waiters', 'simpledb', 'secretsmanager', 'securityhub', 'serverlessapplicationrepository', 'servicequotas', 'servicecatalog', 'appregistry', 'servicediscovery', 'ses', 'waiters', 'sesv2', 'shield', 'signer', 'waiters', 'sms', 'pinpointsmsvoice', 'snowball', 'sns', 'service resource', 'platformapplication', 'platformendpoint', 'subscription', 'topic', 'sqs', 'service resource', 'message', 'queue', 'ssm', 'waiters', 'ssmcontacts', 'ssmincidents', 'waiters', 'sso', 'ssoadmin', 'ssooidc', 'sfn', 'storagegateway', 'sts', 'support', 'swf', 'synthetics', 'textract', 'timestreamquery', 'timestreamwrite', 'transcribeservice', 'transfer', 'translate', 'waf', 'wafregional', 'wafv2', 'wellarchitected', 'workdocs', 'worklink', 'workmail', 'workmailmessageflow', 'workspaces', 'xray']

SERVICES = [
    "ec2",
    "accessanalyzer",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "batch",
    "braket",
    "budgets",
    "ce",
    "chime",
    "cloud9",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iotwireless",
    "ivs",
    "kafka",
    "kendra",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migrationhub-config",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53domains",
    "route53resolver",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "xray"
]

def enum_privs(profile_dict, workspace):
    full_perm = {}
    list_of_perms = {}
    read_perm = {
        "List":{},
        "Describe":{}
    }
    read_perm2 = {
        "List": [],
        "Describe": []
    }
    list_perm = []
    desc_perm = []

    region = profile_dict['region']
    access_key_id = profile_dict['access_key_id']
    secret_key = profile_dict['secret_key']

    stscli = boto3.client("sts", region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)

    response = stscli.get_caller_identity()
    del response['ResponseMetadata']
    user = (response['Arn']).split("/")[-1]

    print(
        ("{}: {}".format(
            colored("User", "red", attrs=['bold']),
            colored(user, "blue")
            )
        )
    )
    for key, value in response.items():
        print("\t{}: {}".format(
            colored(key, "red", attrs=['bold']),
            colored(value, "blue")
        ))

    for service in SERVICES:
        print(colored("--------------------------", 'yellow', attrs=['bold']))
        print("{}: {}".format(
            colored("Service", "red", attrs=['bold']),
            colored(service, "blue", attrs=['bold'])
            ))
        print(colored("--------------------------", 'yellow', attrs=['bold']))
        profile = boto3.client(service, region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)
        methods = dir(profile)
        for method in methods:
            if method.split("_")[0] == "list":
                list_perm.append(method)

            elif method.split("_")[0] == "describe":
                desc_perm.append(method)

        if len(list_perm) > 0:
            print(colored("[*] Trying the 'List' functions:", "yellow", attrs=['bold']))
            for lmeth in list_perm:
                try:
                    response = getattr(profile, lmeth)()
                    del response['ResponseMetadata']
                    read_perm['List'][lmeth] = response
                    (read_perm2['List']).append(lmeth)

                    print(colored("[*] '{}' worked! ".format(lmeth),"green"))
                except KeyboardInterrupt:
                    print(colored("[*] Stopping. It might take a while. Please wait.", "green"))
                    now = datetime.now()
                    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                    file = "{}_enum_user_privs".format(dt_string)
                    filename = "./workspaces/{}/{}".format(workspace, file)
                    file = "{}_allowed_functions".format(dt_string)
                    filename2 = "./workspaces/{}/{}".format(workspace, file)

                    full_perm[service] = read_perm
                    list_of_perms[service] = read_perm2

                    with open(filename, 'w') as perm_file:
                        json.dump(full_perm, perm_file, indent=4, default=str)
                        perm_file.close()
                    print(colored("[*] Output of the allowed functions is saved to '{}'".format(filename), "green"))

                    with open(filename2, 'w') as perm_file:
                        json.dump(list_of_perms, perm_file, indent=4, default=str)
                        perm_file.close()
                    print(colored("[*] The list of the allowed functions is saved to '{}'".format(filename2), "green"))
                    return

                except:
                    pass

        if len(desc_perm) > 0:
            print(colored("[*] Trying the 'Describe' functions:", "yellow", attrs=['bold']))
            for dmeth in desc_perm:
                try:
                    response = getattr(profile, dmeth)()
                    del response['ResponseMetadata']
                    read_perm['Describe'][dmeth] = response
                    (read_perm2['List']).append(dmeth)
                    print(colored("[*] '{}' worked! ".format(dmeth),"green"))

                except KeyboardInterrupt:
                    print(colored("[*] Stopping. It might take a while. Please wait.", "green"))
                    now = datetime.now()
                    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
                    file = "{}_enum_user_privs".format(dt_string)
                    filename = "./workspaces/{}/{}".format(workspace, file)
                    file = "{}_allowed_functions".format(dt_string)
                    filename2 = "./workspaces/{}/{}".format(workspace, file)

                    full_perm[service] = read_perm
                    list_of_perms[service] = read_perm2

                    with open(filename, 'w') as perm_file:
                        json.dump(full_perm, perm_file, indent=4, default=str)
                        perm_file.close()
                    print(colored("[*] Output of the allowed functions is saved to '{}'".format(filename), "green"))

                    with open(filename2, 'w') as perm_file:
                        json.dump(list_of_perms, perm_file, indent=4, default=str)
                        perm_file.close()
                    print(colored("[*] The list of the allowed functions is saved to '{}'".format(filename2), "green"))
                    return
                except:
                    pass

        full_perm[service] = read_perm
        list_of_perms[service] = read_perm2
        read_perm2 = {}
        read_perm = {}
        list_perm = []
        desc_perm = []
        print()

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    file = "{}_enum_user_privs_{}".format(dt_string, user)
    filename = "./workspaces/{}/{}".format(workspace, file)
    file = "{}_allowed_functions_{}".format(dt_string, user)
    filename2 = "./workspaces/{}/{}".format(workspace, file)

    with open(filename, 'w') as perm_file:
        json.dump(full_perm, perm_file, indent=4, default=str)
        perm_file.close()
    print(colored("[*] Output of the allowed functions is saved to '{}'".format(filename), "green"))

    with open(filename2, 'w') as perm_file:
        json.dump(list_of_perms, perm_file, indent=4, default=str)
        perm_file.close()
    print(colored("[*] The list of the allowed functions is saved to '{}'".format(filename2), "green"))