import json
import sys

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
    },
    "BUCKET-NAMES": {
        "value": "",
        "required": "true",
        "description": "A specific bucket or a list of buckets split by comma."
    }
}

description = "List the objects of a bucket"

calls = [
    's3:ListBucketObjects'
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

        if 'DeleteMarkers' in all_versions:
            for marker in all_versions['DeleteMarkers']:
                deleted_files.append(marker['Key'])

            for version in all_versions['Versions']:
                if version['Key'] in deleted_files:
                    all_objects.append({
                        "Owner": version['Owner']['DisplayName'],
                        "Key": version["Key"],
                        "VersionID": version['VersionId'],
                        "LastModified": str(version['LastModified']),
                        "IsLatest": version['IsLatest']
                    })

            return_dict['DeletedFiles'] = all_objects

            database_data = {
                "digitalocean_s3_space_name": bucket,
                "digitalocean_s3_deleted_objects": all_objects,
            }

            try:
                do_user = DigitalOceanSpace.objects.get(digitalocean_s3_space_name=bucket)
                do_user.modify(**database_data)
                do_user.save()

            except DoesNotExist:
                DigitalOceanSpace(**database_data).save()

            except:
                e = sys.exc_info()
                return {"error": "Error from module: {}".format(str(e))}, 500

            return {
                       "Bucket": return_dict
                   }, 200
        else:
            return {"Bucket": {"Bucket": bucket, "Message": "No deleted files in space"}}
    except:
        e = sys.exc_info()
        return {"error": "Error from module: {}".format(str(e))}, 500
