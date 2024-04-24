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
    "BUCKET-NAMES": {
        "value": "",
        "required": "true",
        "description": "A specific bucket or a list of buckets split by comma."
    }
}

description = "Check all the versions of the objects of a bucket or a list of buckets and find deleted files. Then, you can use exploit/aws_s3_get_object to download the files. The module is based of the RedBoto script: aws_s3_list_deleted_files.py"

calls = [
    's3:ListObjectVersions'
]

aws_command = "aws s3api list-object-versions --bucket <my-bucket> --prefix <prefix>"


def exploit(profile):
    deleted_files = []
    bucket = variables["BUCKET-NAMES"]['value']
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

        except:
            e = sys.exc_info()
            return {"error": "Error from module: {}".format(str(e))}, 500

        return {
                   "Bucket": return_dict
               }, 200
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500
