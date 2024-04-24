import json
import sys
import botocore

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
        "value": "SPACE",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    }
}

description = "Enumerate all Space using Space API"
aws_command = ""


def exploit(profile):
    return_dict = []
    #try:
    all_buckets = profile.list_buckets()['Buckets']
    for bucket in all_buckets:
        try:
            bucketCORS = profile.get_bucket_cors(Bucket=bucket["Name"])
            del (bucketCORS['ResponseMetadata'])
            bucket["CORS"] = bucketCORS
        except botocore.exceptions.ClientError:
            bucket["CORS"] = None

        try:
            bucketEnc = profile.get_bucket_encryption(Bucket=bucket["Name"])
            del (bucketEnc['ResponseMetadata'])
            bucket["Encryption"] = bucketEnc
        except botocore.exceptions.ClientError:
            bucket["Encryption"] = None

        try:
            bucketLifeCycle = profile.get_bucket_lifecycle(Bucket=bucket["Name"])
            del (bucketLifeCycle["ResponseMetadata"])
            bucket["Lifecycle"] = bucketLifeCycle
        except botocore.exceptions.ClientError:
            bucket["Lifecycle"] = None

        try:
            bucketLifeCycleConfig = profile.get_bucket_lifecycle_configuration(Bucket=bucket["Name"])
            del (bucketLifeCycleConfig["ResponseMetadata"])
            bucket["LifecycleConfiguration"] = bucketLifeCycleConfig
        except botocore.exceptions.ClientError:
            bucket["LifecycleConfiguration"] = None

        try:
            bucketLocation = profile.get_bucket_location(Bucket=bucket["Name"])
            del (bucketLocation["ResponseMetadata"])
            bucket["BucketLocation"] = bucketLocation['LocationConstraint']
        except botocore.exceptions.ClientError:
            bucket["BucketLocation"] = None

        try:
            bucketLogging = profile.get_bucket_logging(Bucket=bucket["Name"])
            del (bucketLogging["ResponseMetadata"])
            bucket["Logging"] = bucketLogging
        except botocore.exceptions.ClientError:
            bucket["Logging"] = None

        try:
            bucketNotification = profile.get_bucket_notification(Bucket=bucket["Name"])
            del (bucketNotification["ResponseMetadata"])
            bucket["Notification"] = bucketNotification
        except botocore.exceptions.ClientError:
            bucket["Notification"] = None

        try:
            bucketNotificationConfiguration = profile.list_bucket_metrics_configurations(Bucket=bucket["Name"])
            del (bucketNotificationConfiguration["ResponseMetadata"])
            bucket["NotificationConfiguration"] = bucketNotificationConfiguration
        except botocore.exceptions.ClientError:
            bucket["NotificationConfiguration"] = None

        try:
            bucketOwnership = profile.get_bucket_ownership_controls(Bucket=bucket["Name"])
            del (bucketOwnership["ResponseMetadata"])
            bucket["Ownership"] = bucketOwnership['OwnershipControls']
        except botocore.exceptions.ClientError:
            bucket["Ownership"] = None

        try:
            bucketPolicy = profile.get_bucket_policy(Bucket=bucket["Name"])
            del (bucketPolicy["ResponseMetadata"])
            bucket["Policy"] = bucketPolicy
        except botocore.exceptions.ClientError:
            bucket["Policy"] = None

        try:
            bucketPolicyStatus = profile.get_bucket_policy_status(Bucket=bucket["Name"])
            del (bucketPolicyStatus["ResponseMetadata"])
            bucket["PolicyStatus"] = bucketPolicyStatus
        except botocore.exceptions.ClientError:
            bucket["PolicyStatus"] = None

        try:
            bucketReplication = profile.get_bucket_replication(Bucket=bucket["Name"])
            del (bucketReplication["ResponseMetadata"])
            bucket["Replication"] = bucketReplication
        except botocore.exceptions.ClientError:
            bucket["Replication"] = None

        try:
            bucketTagging = profile.get_bucket_tagging(Bucket=bucket["Name"])
            del (bucketTagging["ResponseMetadata"])
            bucket["Tagging"] = bucketTagging
        except botocore.exceptions.ClientError:
            bucket["Tagging"] = None

        try:
            bucketVersioning = profile.get_bucket_versioning(Bucket=bucket["Name"])
            del (bucketVersioning["ResponseMetadata"])
            bucket["Versioning"] = bucketVersioning
        except botocore.exceptions.ClientError:
            bucket["Versioning"] = None

        try:
            bucketWebsite = profile.get_bucket_website(Bucket=bucket["Name"])
            del (bucketWebsite["ResponseMetadata"])
            bucket["Website"] = bucketWebsite
        except botocore.exceptions.ClientError:
            bucket["Website"] = None

        try:
            bucketObjectLockConfig = profile.get_object_lock_configuration(Bucket=bucket["Name"])
            del (bucketObjectLockConfig["ResponseMetadata"])
            bucket["BucketObjectLockConfig"] = bucketObjectLockConfig
        except botocore.exceptions.ClientError:
            bucket["BucketObjectLockConfig"] = None

        try:
            bucketPublicAccessBlock = profile.get_public_access_block(Bucket=bucket["Name"])
            del (bucketPublicAccessBlock["ResponseMetadata"])
            bucket["PublicAccessBlock"] = bucketPublicAccessBlock
        except botocore.exceptions.ClientError:
            bucket["PublicAccessBlock"] = None

        try:
            bucketObjects = profile.list_objects_v2(Bucket=bucket["Name"], MaxKeys=2)
            if bucketObjects['IsTruncated']:
                bucketObjects = profile.list_objects_v2(Bucket=bucket["Name"],
                                                        ContinuationToken=bucketObjects['NextContinuationToken'])
            del (bucketObjects["ResponseMetadata"])

            for bucketObject in bucketObjects['Contents']:
                try:
                    bucketObjectACL = profile.get_object_acl(Bucket=bucket["Name"], Key=bucketObject['Key'])
                    del (bucketObjectACL["ResponseMetadata"])
                    bucketObject['ObjectACL'] = bucketObjectACL
                except botocore.exceptions.ClientError:
                    bucketObject['ObjectACL'] = None

                try:
                    bucketObjectLegalHold = profile.get_object_legal_hold(Bucket=bucket["Name"],
                                                                          Key=bucketObject['Key'])
                    del (bucketObjectLegalHold["ResponseMetadata"])
                    bucketObject['ObjectLegalHold'] = bucketObjectLegalHold['LegalHold']['Status']
                except botocore.exceptions.ClientError:
                    bucketObject['ObjectLegalHold'] = None

                try:
                    bucketObjectRetention = profile.get_object_retention(Bucket=bucket["Name"],
                                                                         Key=bucketObject['Key'])
                    del (bucketObjectRetention["ResponseMetadata"])
                    bucketObject['Retention'] = bucketObjectRetention['Retention']
                except botocore.exceptions.ClientError:
                    bucketObject['Retention'] = None

                try:
                    bucketObjectTagging = profile.get_object_tagging(Bucket=bucket["Name"], Key=bucketObject['Key'])
                    del (bucketObjectTagging["ResponseMetadata"])
                    bucketObject['Tags'] = bucketObjectTagging['TagSet']
                except botocore.exceptions.ClientError:
                    bucketObject['Tags'] = None

            bucket["Objects"] = bucketObjects

        except botocore.exceptions.ClientError:
            bucket["Objects"] = None

        try:
            bucketObjectVersions = profile.list_object_versions(Bucket=bucket["Name"])
            bucket['DeletedFiles'] = []
            deleted_files = []
            if 'DeleteMarkers' in bucketObjectVersions:
                for marker in bucketObjectVersions['DeleteMarkers']:
                    deleted_files.append(marker['Key'])

                for version in bucketObjectVersions['Versions']:
                    if version['Key'] in deleted_files:
                        all_objects = {
                            "Owner": version['Owner']['DisplayName'],
                            "Key": version["Key"],
                            "VersionID": version['VersionId'],
                            "LastModified": str(version['LastModified']),
                            "IsLatest": version['IsLatest']
                        }

                        bucket['DeletedFiles'].append(all_objects)
        except botocore.exceptions.ClientError:
            bucket["DeletedFiles"] = None

        database_data = {
            "digitalocean_s3_space_name": bucket['Name'],
            "digitalocean_s3_space_owner": bucket['Ownership'],
            "digitalocean_s3_creation_date": bucket['CreationDate'],
            "digitalocean_s3_space_objects": bucket['Objects'],
            "digitalocean_s3_deleted_objects": bucket['DeletedFiles'],
            "digitalocean_s3_space_policy_status": bucket['PolicyStatus'],
            "digitalocean_s3_space_policy": bucket['Policy'],
            "digitalocean_s3_space_acl": bucket['ACL'],
            "digitalocean_s3_is_website": False,
            "digitalocean_s3_cors": bucket['CORS']
        }

        #if bucket['Website'] is not None:
        #    database_data["digitalocean_s3_is_website"]: True

        print(database_data)

        try:
            do_user = DigitalOceanSpace.objects.get(digitalocean_s3_space_name=bucket['Name'])
            do_user.modify(**database_data)
            do_user.save()

        except DoesNotExist:
            DigitalOceanSpace(**database_data).save()

        except:
            pass
            #e = sys.exc_info()
            #return {"error": "Error from module: {}".format(str(e))}, 500
        return_dict.append(bucket)

    return {
        "Name": return_dict
    }, 200
    #except:
    #    e = sys.exc_info()
    #    return {"error": "Error from module: {}".format(str(e))}, 500
