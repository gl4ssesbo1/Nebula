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
	},
	"DETECTOR-TIME": {
		"value": "FIFTEEN_MINUTES",
		"required": "true",
        "description":"The time to configure. Can either be FIFTEEN_MINUTES, ONE_HOUR, or SIX_HOURS"
	}
}
description = "Revert the detection time back to the original."

aws_command = "aws guardduty update-detector --detector-id <detector-id>  --no-enable  --region <region> --profile <profile>"

calls = [
	"guardduty:UpdateDetector"
]

def exploit(profile, workspace):
	detectorID = variables['DETECTOR-ID']['value']
	detectorTime = variables['DETECTOR-TIME']['value']

	try:
		profile.update_detector(
			DetectorId=detectorID,
			FindingPublishingFrequency=detectorTime

		)
		status = f"Detector {detectorID} detection time was set to {detectorTime}"
	except:
		status = f"Detector {detectorID} was not changed with error code: {str(sys.exc_info()[1])}."

	return {
		"Detector": {
			"Detector": detectorID,
			"Time": detectorTime,
			"Status": status
		}
	}


