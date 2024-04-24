WELLKNOWN = {
		"Graph": {
			"ClientId": "1b730954-1685-4b74-9bfd-dac224a7b894",
			"RedirectURI": "https://login.microsoftonline.com/common/oauth2/nativeclient",
			"RedirectURI":   "urn:ietf:wg:oauth:2.0:oob",
			"Scope": "https://graph.windows.net//.default",
		},

		#Not at all tested below here
		"Az": {
			"ClientId": "1950a258-227b-4e31-a9cf-717495945fc2",
			"Scope":    "https://management.core.windows.net//.default openid profile offline_access",
		},
		"Teams": {
			"ClientId":    "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
			"RedirectURI": "https://login.microsoftonline.com/common/oauth2/nativeclient",
		},
		"SPO": {
			"ClientId":    "9bc3ab49-b65d-410a-85ad-de819febfddc",
			"RedirectURI": "https://oauth.spops.microsoft.com/",
		},
		"AzureAdmin": {
			"ClientId":    "c44b4083-3bb0-49c1-b47d-974e53cbdf3c",
			"RedirectURI": "https://portal.azure.com/signin/index/?feature.prefetchtokens=true&feature.showservicehealthalerts=true&feature.usemsallogin=true",
		},
		"AzureAD": {
			"ClientId":    "0000000c-0000-0000-c000-000000000000",
			"RedirectURI": "https://account.activedirectory.windowsazure.com/",
			"Scope":       "https://graph.windows.net//user_impersonation",
		},
		"MySignIns": {
			"ClientId":    "19db86c3-b2b9-44cc-b339-36da233a3be2",
			"RedirectURI": "https://mysignins.microsoft.com",
		},
		"AzureADJoin": {
			"ClientId":    "29d9ed98-a469-4536-ade2-f981bc1d605e", #not for resource "https://enrollment.manage.microsoft.com/"
			"RedirectURI": "ms-aadj-redir://auth/drs",
		},
		"AzureAndroidApp": {
			"ClientId":    "0c1307d4-29d6-4389-a11c-5cbe7f65d7fa",
			"RedirectURI": "https://azureapp",
		},
		"OneDriveWeb": {
			"ClientId":    "33be1cef-03fb-444b-8fd3-08ca1b4d803f",
			"RedirectURI": "https://admin.onedrive.com",
		},
		"OneDriveNative": {
			"ClientId":    "ab9b8c07-8f02-4f72-87fa-80105867a763",
			"RedirectURI": "https://login.windows.net/common/oauth2/nativeclient",
		},
		"MSCommerce": {
			"ClientId":    "3d5cffa9-04da-4657-8cab-c7f074657cad",
			"RedirectURI": "http://localhost/m365/commerce",
		},
		"Office": {
			"ClientId":    "d3590ed6-52b3-4102-aeff-aad2292ab01c",
			"RedirectURI": "urn:ietf:wg:oauth:2.0:oob",
			"Scope":       "https://management.core.windows.net//user_impersonation",
		},
	}