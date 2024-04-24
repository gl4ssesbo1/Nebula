import sys

import boto3

def enum_privs(profile_dict, workspace):
    region = profile_dict['region']
    access_key_id = profile_dict['access_key_id']
    secret_key = profile_dict['secret_key']

    allowed_privs = []
    message = "Enter list_aws_s3_buckets to get the info dumped."
    database_info = []

    session_token = ""
    if 'session_token' in profile_dict:
        session_token = profile_dict['session_token']

    try:
        if session_token == "":
            s3client = boto3.client("s3", region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key)
        else:
            s3client = boto3.client("s3", region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_key, aws_session_token=session_token)

    except:
        e = str(sys.exc_info())
        return {
            "error": e
        }

    try:
        # List Buckets
        return_buckets = s3client.list_buckets()
        all_buckets = return_buckets['Buckets']
        allowed_privs.append("list_buckets")

        owner = return_buckets['Owner']['DisplayName']
        del return_buckets

        for bucket in all_buckets:
            database_info.append(
                {
                    "aws_s3_bucket_name": bucket['Name'],
                    "aws_s3_bucket_owner": owner,
                    "aws_s3_creation_date": bucket['CreationDate'],
            })

        allow = 0
        for bucket in all_buckets:
            try:
                bucket_objects = s3client.list_objects_v2(Bucket=bucket, MaxKeys=50000)['Contents']


            except:
                allow = 1
                break

        if allow == 0:
            allowed_privs.append("list_objects_v2")

        allow = 0
        for bucket in all_buckets:
            try:
                bucket_objects = s3client.list_object_versions(Bucket=bucket)
            except:
                allow = 1
                break

        if allow == 0:
            allowed_privs.append("list_object_versions")



    except:
        pass