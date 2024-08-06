import datetime
import json
import re
import sys
import time

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "cloudtrail",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "LOOKUP-ATTRIBUTE": {
        "value": "",
        "required": "false",
        "description": "The Lookup Attribute. Can be one of 'EventId', 'EventName', 'ReadOnly', 'Username', 'ResourceType', 'ResourceName', 'EventSource', 'AccessKeyId'."
    },
    "LOOKUP-ATTRIBUTE-VALUE": {
        "value": "",
        "required": "false",
        "description": "The value of Lookup Attribute"
    },
    "START-TIME": {
        "value": "",
        "required": "false",
        "description": "The start time to lookup logs"
    },
    "END-TIME": {
        "value": "",
        "required": "false",
        "description": "The end time to lookup logs"
    }
}

description = "List all resources on the infrastructure based on the ."

calls = [
    'tag:GetResources'
]

aws_command = "aws cloudtrail lookup-events --region <region> --profile <profile>"

ALLRESOURCETYPES = [
    "aws::apigateway::account",
    "aws::apigateway::apikey",
    "aws::apigateway::clientcertificate",
    "aws::apigateway::domainname",
    "aws::apigateway::restapi",
    "aws::apigateway::stage",
    "aws::apigateway::usageplan",
    "aws::accessanalyzer::analyzer",
    "aws::amplify::app",
    "aws::appmesh::mesh",
    "aws::appstream::appblock",
    "aws::appstream::application",
    "aws::appstream::fleet",
    "aws::appstream::imagebuilder",
    "aws::appstream::stack",
    "aws::appsync::datasource",
    "aws::appsync::graphqlapi",
    "aws::backup::backupplan",
    "aws::backup::backupvault",
    "aws::backup::reportplan",
    "aws::batch::computeenvironment",
    "aws::batch::jobqueue",
    "aws::batch::schedulingpolicy",
    "aws::billingconductor::billinggroup",
    "aws::billingconductor::customlineitem",
    "aws::billingconductor::pricingplan",
    "aws::billingconductor::pricingrule",
    "aws::braket::job",
    "aws::braket::quantumtask",
    "aws::certificatemanager::certificate",
    "aws::acmpca::certificateauthority",
    "aws::cloud9::environment",
    "aws::cloudformation::stack",
    "aws::cloudfront::distribution",
    "aws::cloudfront::streamingdistribution",
    "aws::cloudtrail::channel",
    "aws::cloudtrail::eventdatastore",
    "aws::cloudtrail::trail",
    "aws::cloudwatch::alarm",
    "aws::cloudwatch::dashboard",
    "aws::cloudwatch::insightrule",
    "aws::cloudwatch::metricstream",
    "aws::cloudwatch::servicelevelobjective",
    "aws::logs::destination",
    "aws::logs::loggroup",
    "aws::synthetics::canary",
    "aws::codeartifact::domain",
    "aws::codeartifact::repository",
    "aws::codebuild::project",
    "aws::codecommit::repository",
    "aws::codedeploy::application",
    "aws::codedeploy::deploymentconfig",
    "aws::codegurureviewer::repositoryassociation",
    "aws::codeguruprofiler::profilinggroup",
    "aws::codepipeline::customactiontype",
    "aws::codepipeline::pipeline",
    "aws::codepipeline::webhook",
    "aws::codestarconnections::connection",
    "aws::cognito::identitypool",
    "aws::cognito::userpool",
    "aws::comprehend::documentclassifier",
    "aws::comprehend::entityrecognizer",
    "aws::config::configrule",
    "aws::wisdom::assistant",
    "aws::wisdom::assistantassociation",
    "aws::wisdom::content",
    "aws::wisdom::knowledgebase",
    "aws::wisdom::session",
    "aws::dataexchange::dataset",
    "aws::dataexchange::revision",
    "aws::datapipeline::pipeline",
    "aws::datasync::task",
    "aws::dms::certificate",
    "aws::dms::endpoint",
    "aws::dms::eventsubscription",
    "aws::dms::replicationinstance",
    "aws::dms::replicationsubnetgroup",
    "aws::dms::replicationtask",
    "aws::dynamodb::table",
    "aws::emr::cluster",
    "aws::emrcontainers::jobrun",
    "aws::emrcontainers::virtualcluster",
    "aws::emrserverless::application",
    "aws::emrserverless::jobrun",
    "aws::elasticache::cachecluster",
    "aws::elasticache::parametergroup",
    "aws::elasticache::securitygroup",
    "aws::elasticache::snapshot",
    "aws::elasticache::subnetgroup",
    "aws::elasticache::user",
    "aws::elasticache::usergroup",
    "aws::elasticbeanstalk::application",
    "aws::elasticbeanstalk::applicationversion",
    "aws::elasticbeanstalk::configurationtemplate",
    "aws::elasticbeanstalk::environment",
    "aws::ec2::capacityreservation",
    "aws::ec2::capacityreservationfleet",
    "aws::ec2::carriergateway",
    "aws::ec2::clientvpnendpoint",
    "aws::ec2::coippool",
    "aws::ec2::customergateway",
    "aws::ec2::dhcpoptions",
    "aws::ec2::ec2fleet",
    "aws::ec2::egressonlyinternetgateway",
    "aws::ec2::eip",
    "aws::ec2::exportimagetask",
    "aws::ec2::exportinstancetask",
    "aws::ec2::flowlog",
    "aws::ec2::fpgaimage",
    "aws::ec2::host",
    "aws::ec2::hostreservation",
    "aws::ec2::image",
    "aws::ec2::importimagetask",
    "aws::ec2::importsnapshottask",
    "aws::ec2::instance",
    "aws::ec2::instanceeventwindow",
    "aws::ec2::internetgateway",
    "aws::ec2::ipv4pool",
    "aws::ec2::ipv6pool",
    "aws::ec2::keypair",
    "aws::ec2::launchtemplate",
    "aws::ec2::localgateway",
    "aws::ec2::localgatewayroutetable",
    "aws::ec2::localgatewayroutetablevirtualinterfacegroupassociation",
    "aws::ec2::localgatewayroutetablevpcassociation",
    "aws::ec2::localgatewayvirtualinterface",
    "aws::ec2::localgatewayvirtualinterfacegroup",
    "aws::ec2::natgateway",
    "aws::ec2::networkacl",
    "aws::ec2::networkinsightsaccessscope",
    "aws::ec2::networkinsightsaccessscopeanalysis",
    "aws::ec2::networkinsightsanalysis",
    "aws::ec2::networkinsightspath",
    "aws::ec2::networkinterface",
    "aws::ec2::placementgroup",
    "aws::ec2::prefixlist",
    "aws::ec2::replacerootvolumetask",
    "aws::ec2::reservedinstance",
    "aws::ec2::routetable",
    "aws::ec2::securitygroup",
    "aws::ec2::snapshot",
    "aws::ec2::spotfleet",
    "aws::ec2::spotinstancerequest",
    "aws::ec2::subnet",
    "aws::ec2::subnetcidrreservation",
    "aws::ec2::trafficmirrorfilter",
    "aws::ec2::trafficmirrorsession",
    "aws::ec2::trafficmirrortarget",
    "aws::ec2::transitgateway",
    "aws::ec2::transitgatewayattachment",
    "aws::ec2::transitgatewayconnectpeer",
    "aws::ec2::transitgatewaymulticastdomain",
    "aws::ec2::transitgatewaypolicytable",
    "aws::ec2::transitgatewayroutetable",
    "aws::ec2::transitgatewayroutetableannouncement",
    "aws::ec2::verifiedaccessendpoint",
    "aws::ec2::verifiedaccessgroup",
    "aws::ec2::verifiedaccessinstance",
    "aws::ec2::verifiedaccesstrustprovider",
    "aws::ec2::volume",
    "aws::ec2::vpc",
    "aws::ec2::vpcendpoint",
    "aws::ec2::vpcendpointconnection",
    "aws::ec2::vpcendpointservice",
    "aws::ec2::vpcendpointservicepermissions",
    "aws::ec2::vpcpeeringconnection",
    "aws::ec2::vpnconnection",
    "aws::ec2::vpngateway",
    "aws::ecr::repository",
    "aws::ecs::capacityprovider",
    "aws::ecs::cluster",
    "aws::ecs::containerinstance",
    "aws::ecs::service",
    "aws::ecs::task",
    "aws::ecs::taskdefinition",
    "aws::ecs::taskset",
    "aws::efs::filesystem",
    "aws::elasticinference::elasticinferenceaccelerator",
    "aws::eks::cluster",
    "aws::elasticloadbalancing::loadbalancer",
    "aws::elasticloadbalancingv2::listener",
    "aws::elasticloadbalancingv2::listenerrule",
    "aws::elasticloadbalancingv2::loadbalancer",
    "aws::elasticloadbalancingv2::targetgroup",
    "aws::elasticsearch::domain",
    "aws::events::eventbus",
    "aws::events::rule",
    "aws::eventschemas::discoverer",
    "aws::eventschemas::registry",
    "aws::eventschemas::schema",
    "aws::fsx::filesystem",
    "aws::forecast::dataset",
    "aws::forecast::datasetgroup",
    "aws::forecast::datasetimportjob",
    "aws::forecast::forecast",
    "aws::forecast::forecastexportjob",
    "aws::forecast::predictor",
    "aws::forecast::predictorbacktestexportjob",
    "aws::frauddetector::detector",
    "aws::frauddetector::detectorversion",
    "aws::frauddetector::entitytype",
    "aws::frauddetector::eventtype",
    "aws::frauddetector::externalmodel",
    "aws::frauddetector::label",
    "aws::frauddetector::model",
    "aws::frauddetector::modelversion",
    "aws::frauddetector::outcome",
    "aws::frauddetector::rule",
    "aws::frauddetector::variable",
    "aws::gamelift::alias",
    "aws::gamelift::gamesessionqueue",
    "aws::gamelift::matchmakingconfiguration",
    "aws::gamelift::matchmakingruleset",
    "aws::globalaccelerator::accelerator",
    "aws::glue::crawler",
    "aws::glue::database",
    "aws::glue::job",
    "aws::glue::trigger",
    "aws::glue::workflow",
    "aws::databrew::dataset",
    "aws::databrew::job",
    "aws::databrew::project",
    "aws::databrew::recipe",
    "aws::databrew::schedule",
    "aws::groundstation::config",
    "aws::guardduty::detector",
    "aws::guardduty::filter",
    "aws::guardduty::ipset",
    "aws::guardduty::threatintelset",
    "aws::ivs::channel",
    "aws::ivs::recordingconfiguration",
    "aws::ivs::streamkey",
    "aws::iam::instanceprofile",
    "aws::iam::managedpolicy",
    "aws::iam::openidconnectprovider",
    "aws::iam::role",
    "aws::iam::samlprovider",
    "aws::iam::servercertificate",
    "aws::iam::virtualmfadevice",
    "aws::imagebuilder::component",
    "aws::imagebuilder::containerrecipe",
    "aws::imagebuilder::distributionconfiguration",
    "aws::imagebuilder::image",
    "aws::imagebuilder::imagepipeline",
    "aws::imagebuilder::imagerecipe",
    "aws::imagebuilder::infrastructureconfiguration",
    "aws::inspector::assessmenttemplate",
    "aws::iot::authorizer",
    "aws::iot::custommetric",
    "aws::iot::dimension",
    "aws::iot::jobtemplate",
    "aws::iot::mitigationaction",
    "aws::iot::policy",
    "aws::iot::rolealias",
    "aws::iot::scheduledaudit",
    "aws::iot::securityprofile",
    "aws::iot::topicrule",
    "aws::iotanalytics::channel",
    "aws::iotanalytics::dataset",
    "aws::iotanalytics::datastore",
    "aws::iotanalytics::pipeline",
    "aws::iotevents::detectormodel",
    "aws::iotevents::input",
    "aws::iotfleetwise::campaign",
    "aws::iotfleetwise::decodermanifest",
    "aws::iotfleetwise::fleet",
    "aws::iotfleetwise::modelmanifest",
    "aws::iotfleetwise::signalcatalog",
    "aws::iotfleetwise::vehicle",
    "aws::greengrass::connectordefinition",
    "aws::greengrass::coredefinition",
    "aws::greengrass::devicedefinition",
    "aws::greengrass::functiondefinition",
    "aws::greengrass::group",
    "aws::greengrass::loggerdefinition",
    "aws::greengrass::resourcedefinition",
    "aws::greengrass::subscriptiondefinition",
    "aws::iotsitewise::asset",
    "aws::iotsitewise::assetmodel",
    "aws::iotsitewise::gateway",
    "aws::kms::alias",
    "aws::kms::key",
    "aws::cassandra::keyspace",
    "aws::cassandra::table",
    "aws::kinesis::stream",
    "aws::kinesisanalytics::application",
    "aws::kinesisanalyticsv2::application",
    "aws::kinesisfirehose::deliverystream",
    "aws::lambda::alias",
    "aws::lambda::eventsourcemapping",
    "aws::lambda::function",
    "aws::lambda::layerversion",
    "aws::lambda::version",
    "aws::amazonmq::broker",
    "aws::amazonmq::configuration",
    "aws::macie::classificationjob",
    "aws::macie::customdataidentifier",
    "aws::macie::findingsfilter",
    "aws::macie::member",
    "aws::kafka::cluster",
    "aws::mediaconnect::flow",
    "aws::mediaconnect::flowentitlement",
    "aws::mediaconnect::flowoutput",
    "aws::mediaconnect::flowsource",
    "aws::mediapackage::channel",
    "aws::mediapackage::packagingconfiguration",
    "aws::mediapackage::packaginggroup",
    "aws::networkmanager::corenetwork",
    "aws::networkmanager::device",
    "aws::networkmanager::globalnetwork",
    "aws::networkmanager::link",
    "aws::networkmanager::site",
    "aws::networkmanager::vpcattachment",
    "aws::opensearchservice::domain",
    "aws::opsworks::instance",
    "aws::opsworks::layer",
    "aws::opsworks::stack",
    "aws::organizations::account",
    "aws::organizations::organizationalunit",
    "aws::organizations::policy",
    "aws::organizations::root",
    "aws::pinpoint::app",
    "aws::pinpoint::emailtemplate",
    "aws::pinpoint::pushtemplate",
    "aws::pinpoint::smstemplate",
    "aws::pinpoint::voicetemplate",
    "aws::pinpointsmsvoicev2::pool",
    "aws::qldb::ledger",
    "aws::qldb::stream",
    "aws::redshift::cluster",
    "aws::redshift::clusterparametergroup",
    "aws::redshift::clustersecuritygroup",
    "aws::redshift::clustersubnetgroup",
    "aws::redshift::dbgroup",
    "aws::redshift::dbname",
    "aws::redshift::dbuser",
    "aws::redshift::eventsubscription",
    "aws::redshift::hsmclientcertificate",
    "aws::redshift::hsmconfiguration",
    "aws::redshift::namespace",
    "aws::redshift::snapshot",
    "aws::redshift::snapshotcopygrant",
    "aws::redshift::snapshotschedule",
    "aws::redshift::usagelimit",
    "aws::rds::customdbengineversion",
    "aws::rds::dbcluster",
    "aws::rds::dbclusterendpoint",
    "aws::rds::dbclusterparametergroup",
    "aws::rds::dbclustersnapshot",
    "aws::rds::dbinstance",
    "aws::rds::dbparametergroup",
    "aws::rds::dbproxy",
    "aws::rds::dbproxyendpoint",
    "aws::rds::dbproxytargetgroup",
    "aws::rds::dbsecuritygroup",
    "aws::rds::dbsnapshot",
    "aws::rds::dbsubnetgroup",
    "aws::rds::deployment",
    "aws::rds::eventsubscription",
    "aws::rds::optiongroup",
    "aws::rds::reserveddbinstance",
    "aws::ram::resourceshare",
    "aws::resourcegroups::group",
    "aws::robomaker::deploymentjob",
    "aws::robomaker::fleet",
    "aws::robomaker::robot",
    "aws::robomaker::robotapplication",
    "aws::robomaker::simulationapplication",
    "aws::robomaker::simulationjob",
    "aws::route53::domain",
    "aws::route53::healthcheck",
    "aws::route53::hostedzone",
    "aws::route53resolver::firewalldomainlist",
    "aws::route53resolver::firewallrulegroup",
    "aws::route53resolver::resolverendpoint",
    "aws::route53resolver::resolverqueryloggingconfig",
    "aws::route53resolver::resolverrule",
    "aws::glacier::vault",
    "aws::sagemaker::appimageconfig",
    "aws::sagemaker::coderepository",
    "aws::sagemaker::endpoint",
    "aws::sagemaker::endpointconfig",
    "aws::sagemaker::hyperparametertuningjob",
    "aws::sagemaker::image",
    "aws::sagemaker::labelingjob",
    "aws::sagemaker::model",
    "aws::sagemaker::modelpackagegroup",
    "aws::sagemaker::notebookinstance",
    "aws::sagemaker::pipeline",
    "aws::sagemaker::project",
    "aws::sagemaker::trainingjob",
    "aws::sagemaker::transformjob",
    "aws::sagemaker::workteam",
    "aws::secretsmanager::secret",
    "aws::servicecatalog::cloudformationproduct",
    "aws::servicecatalog::portfolio",
    "aws::servicecatalogappregistry::application",
    "aws::servicecatalogappregistry::attributegroup",
    "aws::servicequotas::quota",
    "aws::ses::configurationset",
    "aws::ses::contactlist",
    "aws::ses::dedicatedippool",
    "aws::ses::identity",
    "aws::sns::topic",
    "aws::sqs::queue",
    "aws::s3::bucket",
    "aws::s3::job",
    "aws::s3::storagelens",
    "aws::stepfunctions::activity",
    "aws::stepfunctions::statemachine",
    "aws::storagegateway::gateway",
    "aws::storagegateway::volume",
    "aws::ssm::association",
    "aws::ssm::automationexecution",
    "aws::ssm::document",
    "aws::ssm::maintenancewindow",
    "aws::ssm::managedinstance",
    "aws::ssm::opsitem",
    "aws::ssm::opsmetadata",
    "aws::ssm::parameter",
    "aws::ssm::patchbaseline",
    "aws::systemsmanagersap::application",
    "aws::systemsmanagersap::database",
    "aws::timestream::scheduledquery",
    "aws::transfer::certificate",
    "aws::transfer::connector",
    "aws::transfer::workflow",
    "aws::waf::rule",
    "aws::waf::webacl",
    "aws::workspaces::workspace",
    "aws::xray::group",
    "aws::xray::samplingrule"
]

AWS_SERVICES = ['accessanalyzer', 'acm', 'acm-pca', 'alexaforbusiness', 'amp', 'amplify', 'amplifybackend', 'apigateway', 'apigatewaymanagementapi', 'apigatewayv2', 'appconfig', 'appflow', 'appintegrations', 'application-autoscaling', 'application-insights', 'applicationcostprofiler', 'appmesh', 'apprunner', 'appstream', 'appsync', 'athena', 'auditmanager', 'autoscaling', 'autoscaling-plans', 'backup', 'batch', 'braket', 'budgets', 'ce', 'chime', 'cloud9', 'clouddirectory', 'cloudformation', 'cloudfront', 'cloudhsm', 'cloudhsmv2', 'cloudsearch', 'cloudsearchdomain', 'cloudtrail', 'cloudwatch', 'codeartifact', 'codebuild', 'codecommit', 'codedeploy', 'codeguru-reviewer', 'codeguruprofiler', 'codepipeline', 'codestar', 'codestar-connections', 'codestar-notifications', 'cognito-identity', 'cognito-idp', 'cognito-sync', 'comprehend', 'comprehendmedical', 'compute-optimizer', 'config', 'connect', 'connect-contact-lens', 'connectparticipant', 'cur', 'customer-profiles', 'databrew', 'dataexchange', 'datapipeline', 'datasync', 'dax', 'detective', 'devicefarm', 'devops-guru', 'directconnect', 'discovery', 'dlm', 'dms', 'docdb', 'ds', 'dynamodb', 'dynamodbstreams', 'ebs', 'ec2', 'ec2-instance-connect', 'ecr', 'ecr-public', 'ecs', 'efs', 'eks', 'elastic-inference', 'elasticache', 'elasticbeanstalk', 'elastictranscoder', 'elb', 'elbv2', 'emr', 'emr-containers', 'es', 'events', 'finspace', 'finspace-data', 'firehose', 'fis', 'fms', 'forecast', 'forecastquery', 'frauddetector', 'fsx', 'gamelift', 'glacier', 'globalaccelerator', 'glue', 'greengrass', 'greengrassv2', 'groundstation', 'guardduty', 'health', 'healthlake', 'honeycode', 'iam', 'identitystore', 'imagebuilder', 'importexport', 'inspector', 'iot', 'iot-data', 'iot-jobs-data', 'iot1click-devices', 'iot1click-projects', 'iotanalytics', 'iotdeviceadvisor', 'iotevents', 'iotevents-data', 'iotfleethub', 'iotsecuretunneling', 'iotsitewise', 'iotthingsgraph', 'iotwireless', 'ivs', 'kafka', 'kendra', 'kinesis', 'kinesis-video-archived-media', 'kinesis-video-media', 'kinesis-video-signaling', 'kinesisanalytics', 'kinesisanalyticsv2', 'kinesisvideo', 'kms', 'lakeformation', 'lambda', 'lex-models', 'lex-runtime', 'lexv2-models', 'lexv2-runtime', 'license-manager', 'lightsail', 'location', 'logs', 'lookoutequipment', 'lookoutmetrics', 'lookoutvision', 'machinelearning', 'macie', 'macie2', 'managedblockchain', 'marketplace-catalog', 'marketplace-entitlement', 'marketplacecommerceanalytics', 'mediaconnect', 'mediaconvert', 'medialive', 'mediapackage', 'mediapackage-vod', 'mediastore', 'mediastore-data', 'mediatailor', 'meteringmarketplace', 'mgh', 'mgn', 'migrationhub-config', 'mobile', 'mq', 'mturk', 'mwaa', 'neptune', 'network-firewall', 'networkmanager', 'nimble', 'opsworks', 'opsworkscm', 'organizations', 'outposts', 'personalize', 'personalize-events', 'personalize-runtime', 'pi', 'pinpoint', 'pinpoint-email', 'pinpoint-sms-voice', 'polly', 'pricing', 'proton', 'qldb', 'qldb-session', 'quicksight', 'ram', 'rds', 'rds-data', 'redshift', 'redshift-data', 'rekognition', 'resource-groups', 'resourcegroupstaggingapi', 'robomaker', 'route53', 'route53domains', 'route53resolver', 's3', 's3control', 's3outposts', 'sagemaker', 'sagemaker-a2i-runtime', 'sagemaker-edge', 'sagemaker-featurestore-runtime', 'sagemaker-runtime', 'savingsplans', 'schemas', 'sdb', 'secretsmanager', 'securityhub', 'serverlessrepo', 'service-quotas', 'servicecatalog', 'servicecatalog-appregistry', 'servicediscovery', 'ses', 'sesv2', 'shield', 'signer', 'sms', 'sms-voice', 'snowball', 'sns', 'sqs', 'ssm', 'ssm-contacts', 'ssm-incidents', 'sso', 'sso-admin', 'sso-oidc', 'stepfunctions', 'storagegateway', 'sts', 'support', 'swf', 'synthetics', 'textract', 'timestream-query', 'timestream-write', 'transcribe', 'transfer', 'translate', 'waf', 'waf-regional', 'wafv2', 'wellarchitected', 'workdocs', 'worklink', 'workmail', 'workmailmessageflow', 'workspaces', 'xray']
def filterResourcesByServiceAccountAndRegion(resource):
    service = resource.split(":")[2]
    region = resource.split(":")[3]
    accountID = resource.split(":")[4]
    resourceType = resource.split(":")[5].split("/")[0]

    return [
        service,
        region,
        accountID,
        resourceType
    ]

def exploit(profile, workspace):
    lookup_attribute = variables['LOOKUP-ATTRIBUTE']['value']
    lookup_value = variables['LOOKUP-ATTRIBUTE-VALUE']['value']
    start_time = variables['START-TIME']['value']
    end_time = variables['END-TIME']['value']

    args = {}

    if start_time != "":
        args['StartTime'] = datetime.datetime.strptime(start_time, "%Y-%m-%d")

    if end_time != "":
        args['EndTime'] = datetime.datetime.strptime(end_time, "%Y-%m-%d")

    if (lookup_attribute == "" and lookup_value != "") or \
        (lookup_attribute != "" and lookup_value == ""):
        return {"error": "Put either both LOOKUP-ATTRIBUTE and LOOKUP-ATTRIBUTE-VALUE or neither of them."}

    elif (lookup_attribute != "" and lookup_value != ""):
        try:
            args["LookupAttributes"] = [{
                    'AttributeKey': lookup_attribute,
                    'AttributeValue': lookup_value
                }]
            response = profile.lookup_events(
                **args
            )
            resources = response["Events"]
            while response['NextToken'] != "":
                try:
                    response = profile.lookup_events(
                        LookupAttributes=[{
                            'AttributeKey': lookup_attribute,
                            'AttributeValue': lookup_value
                        }],
                        NextToken = response['NextToken']
                    )
                    resources.extend(response["Events"])
                except:
                    break
        except Exception as e:
            return {"error": "Error from module: {}".format(str(e))}, 500

    else:
        try:
            response = profile.lookup_events(**args)
            resources = response["Events"]
            while response['NextToken'] != "":
                try:
                    #print(response['NextToken'])
                    #print('yes')
                    response = profile.lookup_events(NextToken=response['NextToken'])
                    resources.extend(response["Events"])
                except:
                    break
        except Exception as e:
            return {"error": "Error from module: {}".format(str(e))}, 500

    accounts = []
    ips = []
    arns = []

    try:
        returnList = {
            "Resources": {}
        }

        for event in resources:
            for eventResources in event['Resources']:
                rType = eventResources['ResourceType']
                rValue = eventResources['ResourceName']
                #for rType, rValue in eventResources.items():
                if rType in returnList['Resources']:
                    if not rValue in returnList['Resources'][rType]:
                        returnList['Resources'][rType].append(rValue)
                else:
                    returnList['Resources'][rType] = [rValue]

            eventdata = json.loads(event["CloudTrailEvent"])

            try:
                if "arn" in eventdata['userIdentity']:
                    arns.append(eventdata['userIdentity']['arn'])

                accounts.append(eventdata['userIdentity']['accountId'])
                ips.append(eventdata['sourceIPAddress'])
            except:
                pass

            try:
                eventdata = json.loads(event["CloudTrailEvent"])

                if "arn" in eventdata['userIdentity']:
                    arn = eventdata['userIdentity']['arn']
                    arns.append(eventdata['userIdentity']['arn'])

                    if arn.split(":")[5].split("/")[0] in ["user", "federated-user"]:
                        if 'AWS::IAM::User' not in returnList['Resources']:
                            returnList['Resources']['AWS::IAM::User'] = []
                        if not arn in returnList['Resources']['AWS::IAM::User']:
                            returnList['Resources']['AWS::IAM::User'].append(arn)

                    else:
                        if 'AWS::IAM::Role' not in returnList['Resources']:
                            returnList['Resources']['AWS::IAM::Role'] = []

                        if not arn in returnList['Resources']['AWS::IAM::Role']:
                            returnList['Resources']['AWS::IAM::Role'].append(arn)

                '''        
                if eventdata['responseElements'] is not None:
                    for responseKey, responseValue in eventdata['responseElements'].items():
                        print(responseValue)
                        if re.match(
                            "arn:aws:\w+:::\w+",
                            responseValue
                        ):
                            arns.append(responseValue)

                if eventdata['requestParameters'] is not None:
                    for resourceKey, resourceValue in eventdata['requestParameters'].items():
                        if re.match(
                            "arn:aws:\w+::\d+:\w+",
                            resourceValue
                        ):
                            arns.append(resourceValue)
                '''
                #for arn in list(set(arns)):
                #    arns.append(arn)
                '''
                    resourceInfo = filterResourcesByServiceAccountAndRegion(arn)
                    if resourceInfo[2] == "":
                        resourceInfo[2] = "AWS"
                    
                    else:
                        if resourceInfo[2] in returnList:
                            if resourceInfo[1] in returnList[resourceInfo[2]]:
                                if resourceInfo[0] in returnList[resourceInfo[2]][resourceInfo[1]]:
                                    returnList[resourceInfo[2]][resourceInfo[1]][resourceInfo[0]].append(arn)

                                else:
                                    returnList[resourceInfo[2]][resourceInfo[1]][resourceInfo[0]] = [arn]
                            

                        else:
                            returnList[resourceInfo[2]] = {
                                resourceInfo[1]: resourceInfo[0]
                            }
                '''
            
            
            except Exception as e:
                print(str(e))

        #returnList['ARNs'] = list(set(arns))
        returnList['Resources']['IPs'] = list(set(ips))
        #returnList['Accounts'] = list(set(accounts))
    except Exception as e:
        return {"error": "Error from module: {}".format(str(e))}, 500

    return returnList, 200
