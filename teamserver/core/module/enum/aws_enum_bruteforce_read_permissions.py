import sys

import boto3
import json

from core.module.enum.__bruteforce_calls.bruteforce_calls import BRUTEFORCE_CALLS

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "None",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"SERVICE": {
		"value": "",
		"required": "false",
        "description":"The service to enumerate. Can be any of: 'accessanalyzer', 'account', 'acm', 'acm-pca', 'amp', 'amplify', 'amplifybackend', 'amplifyuibuilder', 'apigateway', 'apigatewaymanagementapi', 'apigatewayv2', 'appconfig', 'appconfigdata', 'appfabric', 'appflow', 'appintegrations', 'application-autoscaling', 'application-insights', 'applicationcostprofiler', 'appmesh', 'apprunner', 'appstream', 'appsync', 'arc-zonal-shift', 'athena', 'auditmanager', 'autoscaling', 'autoscaling-plans', 'b2bi', 'backup', 'backup-gateway', 'batch', 'bcm-data-exports', 'bedrock', 'bedrock-agent', 'bedrock-agent-runtime', 'bedrock-runtime', 'billingconductor', 'braket', 'budgets', 'ce', 'chime', 'chime-sdk-identity', 'chime-sdk-media-pipelines', 'chime-sdk-meetings', 'chime-sdk-messaging', 'chime-sdk-voice', 'cleanrooms', 'cleanroomsml', 'cloud9', 'cloudcontrol', 'clouddirectory', 'cloudformation', 'cloudfront', 'cloudfront-keyvaluestore', 'cloudhsm', 'cloudhsmv2', 'cloudsearch', 'cloudsearchdomain', 'cloudtrail', 'cloudtrail-data', 'cloudwatch', 'codeartifact', 'codebuild', 'codecatalyst', 'codecommit', 'codedeploy', 'codeguru-reviewer', 'codeguru-security', 'codeguruprofiler', 'codepipeline', 'codestar', 'codestar-connections', 'codestar-notifications', 'cognito-identity', 'cognito-idp', 'cognito-sync', 'comprehend', 'comprehendmedical', 'compute-optimizer', 'config', 'connect', 'connect-contact-lens', 'connectcampaigns', 'connectcases', 'connectparticipant', 'controltower', 'cost-optimization-hub', 'cur', 'customer-profiles', 'databrew', 'dataexchange', 'datapipeline', 'datasync', 'datazone', 'dax', 'detective', 'devicefarm', 'devops-guru', 'directconnect', 'discovery', 'dlm', 'dms', 'docdb', 'docdb-elastic', 'drs', 'ds', 'dynamodb', 'dynamodbstreams', 'ebs', 'ec2', 'ec2-instance-connect', 'ecr', 'ecr-public', 'ecs', 'efs', 'eks', 'eks-auth', 'elastic-inference', 'elasticache', 'elasticbeanstalk', 'elastictranscoder', 'elb', 'elbv2', 'emr', 'emr-containers', 'emr-serverless', 'entityresolution', 'es', 'events', 'evidently', 'finspace', 'finspace-data', 'firehose', 'fis', 'fms', 'forecast', 'forecastquery', 'frauddetector', 'freetier', 'fsx', 'gamelift', 'glacier', 'globalaccelerator', 'glue', 'grafana', 'greengrass', 'greengrassv2', 'groundstation', 'guardduty', 'health', 'healthlake', 'iam', 'identitystore', 'imagebuilder', 'importexport', 'inspector', 'inspector-scan', 'inspector2', 'internetmonitor', 'iot', 'iot-data', 'iot-jobs-data', 'iot1click-devices', 'iot1click-projects', 'iotanalytics', 'iotdeviceadvisor', 'iotevents', 'iotevents-data', 'iotfleethub', 'iotfleetwise', 'iotsecuretunneling', 'iotsitewise', 'iotthingsgraph', 'iottwinmaker', 'iotwireless', 'ivs', 'ivs-realtime', 'ivschat', 'kafka', 'kafkaconnect', 'kendra', 'kendra-ranking', 'keyspaces', 'kinesis', 'kinesis-video-archived-media', 'kinesis-video-media', 'kinesis-video-signaling', 'kinesis-video-webrtc-storage', 'kinesisanalytics', 'kinesisanalyticsv2', 'kinesisvideo', 'kms', 'lakeformation', 'lambda', 'launch-wizard', 'lex-models', 'lex-runtime', 'lexv2-models', 'lexv2-runtime', 'license-manager', 'license-manager-linux-subscriptions', 'license-manager-user-subscriptions', 'lightsail', 'location', 'logs', 'lookoutequipment', 'lookoutmetrics', 'lookoutvision', 'm2', 'machinelearning', 'macie2', 'managedblockchain', 'managedblockchain-query', 'marketplace-agreement', 'marketplace-catalog', 'marketplace-deployment', 'marketplace-entitlement', 'marketplacecommerceanalytics', 'mediaconnect', 'mediaconvert', 'medialive', 'mediapackage', 'mediapackage-vod', 'mediapackagev2', 'mediastore', 'mediastore-data', 'mediatailor', 'medical-imaging', 'memorydb', 'meteringmarketplace', 'mgh', 'mgn', 'migration-hub-refactor-spaces', 'migrationhub-config', 'migrationhuborchestrator', 'migrationhubstrategy', 'mq', 'mturk', 'mwaa', 'neptune', 'neptune-graph', 'neptunedata', 'network-firewall', 'networkmanager', 'networkmonitor', 'nimble', 'oam', 'omics', 'opensearch', 'opensearchserverless', 'opsworks', 'opsworkscm', 'organizations', 'osis', 'outposts', 'panorama', 'payment-cryptography', 'payment-cryptography-data', 'pca-connector-ad', 'personalize', 'personalize-events', 'personalize-runtime', 'pi', 'pinpoint', 'pinpoint-email', 'pinpoint-sms-voice', 'pinpoint-sms-voice-v2', 'pipes', 'polly', 'pricing', 'privatenetworks', 'proton', 'qbusiness', 'qconnect', 'qldb', 'qldb-session', 'quicksight', 'ram', 'rbin', 'rds', 'rds-data', 'redshift', 'redshift-data', 'redshift-serverless', 'rekognition', 'repostspace', 'resiliencehub', 'resource-explorer-2', 'resource-groups', 'resourcegroupstaggingapi', 'robomaker', 'rolesanywhere', 'route53', 'route53-recovery-cluster', 'route53-recovery-control-config', 'route53-recovery-readiness', 'route53domains', 'route53resolver', 'rum', 's3', 's3control', 's3outposts', 'sagemaker', 'sagemaker-a2i-runtime', 'sagemaker-edge', 'sagemaker-featurestore-runtime', 'sagemaker-geospatial', 'sagemaker-metrics', 'sagemaker-runtime', 'savingsplans', 'scheduler', 'schemas', 'sdb', 'secretsmanager', 'securityhub', 'securitylake', 'serverlessrepo', 'service-quotas', 'servicecatalog', 'servicecatalog-appregistry', 'servicediscovery', 'ses', 'sesv2', 'shield', 'signer', 'simspaceweaver', 'sms', 'sms-voice', 'snow-device-management', 'snowball', 'sns', 'sqs', 'ssm', 'ssm-contacts', 'ssm-incidents', 'ssm-sap', 'sso', 'sso-admin', 'sso-oidc', 'stepfunctions', 'storagegateway', 'sts', 'supplychain', 'support', 'support-app', 'swf', 'synthetics', 'textract', 'timestream-query', 'timestream-write', 'tnb', 'transcribe', 'transfer', 'translate', 'trustedadvisor', 'verifiedpermissions', 'voice-id', 'vpc-lattice', 'waf', 'waf-regional', 'wafv2', 'wellarchitected', 'wisdom', 'workdocs', 'worklink', 'workmail', 'workmailmessageflow', 'workspaces', 'workspaces-thin-client', 'workspaces-web', 'xray'"
	}
}
description = "Bruteforce all list_*, get_* and describe_* calls for each service dynamically."

# The aws command is the command used for describe-launch-templates. You can change to yours. Please set region and profile as {}
aws_command = "None"

# The exploit function is like the main() of the module. This is called 
# from the module

colors = [
    "not-used",
    "red",
    "blue",
    "yellow",
    "green",
    "magenta",
    "cyan",
    "white"
]

output = ""

def exploit(profile):
    try:
        response = profile.describe_report_definitions()

        if response['NextToken']:
            response.extend(profile.describe_report_definitions(NextToken=response['NextToken']))

        return {"ReportName": response['ReportDefinitions']}

    except Exception as e:
        return {"error": str(e)}

    