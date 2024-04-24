POLICIES = {
    "AWSDirectConnectReadOnlyAccess":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "directconnect:Describe*",
                    "directconnect:List*",
                    "ec2:DescribeVpnGateways",
                    "ec2:DescribeTransitGateways"
                ],
                "Resource": "*"
            }
        ]
    },
    "AmazonGlacierReadOnlyAccess":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "glacier:DescribeJob",
                    "glacier:DescribeVault",
                    "glacier:GetDataRetrievalPolicy",
                    "glacier:GetJobOutput",
                    "glacier:GetVaultAccessPolicy",
                    "glacier:GetVaultLock",
                    "glacier:GetVaultNotifications",
                    "glacier:ListJobs",
                    "glacier:ListMultipartUploads",
                    "glacier:ListParts",
                    "glacier:ListTagsForVault",
                    "glacier:ListVaults"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    },
    "AWSMarketplaceFullAccess":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "aws-marketplace:*",
                    "cloudformation:CreateStack",
                    "cloudformation:DescribeStackResource",
                    "cloudformation:DescribeStackResources",
                    "cloudformation:DescribeStacks",
                    "cloudformation:List*",
                    "ec2:AuthorizeSecurityGroupEgress",
                    "ec2:AuthorizeSecurityGroupIngress",
                    "ec2:CreateSecurityGroup",
                    "ec2:CreateTags",
                    "ec2:DescribeAccountAttributes",
                    "ec2:DescribeAddresses",
                    "ec2:DeleteSecurityGroup",
                    "ec2:DescribeAccountAttributes",
                    "ec2:DescribeImages",
                    "ec2:DescribeInstances",
                    "ec2:DescribeKeyPairs",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeTags",
                    "ec2:DescribeVpcs",
                    "ec2:RunInstances",
                    "ec2:StartInstances",
                    "ec2:StopInstances",
                    "ec2:TerminateInstances"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:CopyImage",
                    "ec2:DeregisterImage",
                    "ec2:DescribeSnapshots",
                    "ec2:DeleteSnapshot",
                    "ec2:CreateImage",
                    "ec2:DescribeInstanceStatus",
                    "ssm:GetAutomationExecution",
                    "ssm:UpdateDocumentDefaultVersion",
                    "ssm:CreateDocument",
                    "ssm:StartAutomationExecution",
                    "ssm:ListDocuments",
                    "ssm:UpdateDocument",
                    "ssm:DescribeDocument",
                    "sns:ListTopics",
                    "sns:GetTopicAttributes",
                    "sns:CreateTopic",
                    "iam:GetRole",
                    "iam:GetInstanceProfile",
                    "iam:ListRoles",
                    "iam:ListInstanceProfiles"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject"
                ],
                "Resource": [
                    "arn:aws:s3:::*image-build*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sns:Publish",
                    "sns:setTopicAttributes"
                ],
                "Resource": "arn:aws:sns:*:*:*image-build*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "iam:PassRole"
                ],
                "Resource": [
                    "*"
                ],
                "Condition": {
                    "StringLike": {
                        "iam:PassedToService": [
                            "ec2.amazonaws.com",
                            "ssm.amazonaws.com"
                        ]
                    }
                }
            }
        ]
    },
    "ClientVPNServiceRolePolicy":{
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeInternetGateways",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeAccountAttributes",
                "ds:AuthorizeApplication",
                "ds:DescribeDirectories",
                "ds:GetDirectoryLimits",
                "ds:UnauthorizeApplication",
                "logs:DescribeLogStreams",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "acm:GetCertificate",
                "acm:DescribeCertificate",
                "iam:GetSAMLProvider",
                "lambda:GetFunctionConfiguration"
            ],
            "Resource": "*"
        }
    },
    "AWSSSODirectoryAdministrator":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSSSODirectoryAdministrator",
                "Effect": "Allow",
                "Action": [
                    "sso-directory:*",
                    "sso:ListDirectoryAssociations"
                ],
                "Resource": "*"
            }
        ]
    },
    
}