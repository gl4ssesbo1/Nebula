import json
import requests

def list_aws_s3_buckets(apihost, jwt_token):
    try:
        buckets = json.loads(requests.get("{}/api/latest/awsbuckets".format(apihost), headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {"aws_s3_bucket_name": buckets}

    except Exception as e:
        return {'error': f"Error getting buckets: {str(e)}"}

def get_aws_s3_bucket(apihost, bucket, jwt_token):
    try:
        bucket_dict = json.loads(requests.post("{}/api/latest/awsbuckets".format(apihost), json={"aws_s3_bucket_name": bucket}, headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
        return {'aws_s3_bucket_name': bucket_dict['aws_s3_bucket_name']}

    except Exception as e:
        return {'error': f"Error getting buckets: {str(e)}"}

