import sys
from mongoengine import DoesNotExist
from core.database.models import AWSS3Bucket

author = {
    "name": "gl4ssesbo1",
    "twitter": "https://twitter.com/gl4ssesbo1",
    "github": "https://github.com/gl4ssesbo1",
    "blog": "https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
    "SERVICE": {
        "value": "s3",
        "required": "true",
        "description": "The service that will be used to run the module. It cannot be changed."
    },
    "BUCKET-NAME": {
        "value": "",
        "required": "false",
        "description": "A specific bucket or a list of buckets split by comma. If empty, a list of buckets will be looked first."
    }
}

description = "List the objects of a bucket"

calls = [
    's3:ListBucketObjects'
]

aws_command = "aws s3api list-object-versions --bucket <my-bucket> --prefix <prefix>"


def exploit(profile, workspace):
    deleted_files = []
    bucketvar = variables["BUCKET-NAME"]['value']
    buckets = []
    allbuckets = []
    if bucketvar == "":
        bucketrequest = profile.list_buckets()
        if 'Buckets' in bucketrequest and len(bucketrequest['Buckets']) > 0:
            for bucketdict in bucketrequest['Buckets']:
                buckets.append(bucketdict['Name'])
    else:
        buckets = [bucketvar]

    for bucket in buckets:
        return_dict = {
            "Bucket": bucket
        }
        all_objects = []
        try:
            all_versions = profile.list_object_versions(Bucket=bucket)
            for marker in all_versions['DeleteMarkers']:
                deleted_files.append(marker['Key'])

            for version in all_versions['Versions']:
                if version['Key'] in deleted_files:
                    all_objects = {
                        "Owner": version['Owner']['DisplayName'],
                        "Key": version["Key"],
                        "VersionID": version['VersionId'],
                        "LastModified": str(version['LastModified']),
                        "IsLatest": version['IsLatest']
                    }

            return_dict['DeletedFiles'] = all_objects

            allbuckets.append(return_dict)

            database_data = {
                "aws_s3_bucket_name": bucket,
                "aws_s3_bucket_objects": all_objects
            }

            try:
                aws_user = AWSS3Bucket.objects.get(aws_s3_bucket_name=bucket)
                aws_user.modify(**database_data)
                aws_user.save()

            except DoesNotExist:
                AWSS3Bucket(**database_data).save()

            except Exception as e:
                return {"error": "Error from module: {}".format(str(e))}, 500


        except Exception as e:
            allbuckets.append({"Bucket": bucket, "error": f"Error from module: {str(e)}"})

    return {
        "Bucket": allbuckets
    }, 200