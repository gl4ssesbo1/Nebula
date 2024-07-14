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
		"value": "guardduty",
		"required": "true",
        "description":"The service that will be used to run the module. It cannot be changed."
	},
	"DETECTOR-ID": {
		"value": "",
		"required": "true",
        "description":"The ID of the GuardDuty Detector to Disable"
	}
}
description = "Enables a GD Detector on a specific region."

aws_command = "aws guardduty update-detector --detector-id <detector-id>  --enable  --region <region> --profile <profile>"

calls = [
	"guardduty:UpdateDetector"
]

def exploit(profile, workspace):
	detectorID = variables['DETECTOR-ID']['value']

	try:
		profile.update_detector(
			DetectorId=detectorID,
			Enable=True
		)
		status = f"Detector {detectorID} was enabled"
	except Exception as e:
		status = f"Detector {detectorID} was not enabled with error code: {str(e)}."

	return {
		"Detector": {
			"Detector": detectorID,
			"Status": status
		}
	}

