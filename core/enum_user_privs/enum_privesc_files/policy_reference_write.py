POLICIES = {
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
    "AmazonDMSRedshiftS3Role":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:CreateBucket",
                    "s3:ListBucket",
                    "s3:DeleteBucket",
                    "s3:GetBucketLocation",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:GetObjectVersion",
                    "s3:GetBucketPolicy",
                    "s3:PutBucketPolicy",
                    "s3:GetBucketAcl",
                    "s3:PutBucketVersioning",
                    "s3:GetBucketVersioning",
                    "s3:PutLifecycleConfiguration",
                    "s3:GetLifecycleConfiguration",
                    "s3:DeleteBucketPolicy"
                ],
                "Resource": "arn:aws:s3:::dms-*"
            }
        ]
    },
    "AWSHealthFullAccess":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "organizations:EnableAWSServiceAccess",
                    "organizations:DisableAWSServiceAccess"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "organizations:ServicePrincipal": "health.amazonaws.com"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "health:*",
                    "organizations:ListAccounts",
                    "organizations:ListParents",
                    "organizations:DescribeAccount",
                    "organizations:ListDelegatedAdministrators"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": "iam:CreateServiceLinkedRole",
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "iam:AWSServiceName": "health.amazonaws.com"
                    }
                }
            }
        ]
    },
    "AlexaForBusinessGatewayExecution":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "a4b:Send*",
                    "a4b:Get*"
                ],
                "Resource": "arn:aws:a4b:*:*:gateway/*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage"
                ],
                "Resource": [
                    "arn:aws:sqs:*:*:dd-*",
                    "arn:aws:sqs:*:*:sd-*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "a4b:List*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:DescribeLogGroups",
                    "logs:PutLogEvents"
                ],
                "Resource": "*"
            }
        ]
    },
    "AmazonRDSFullAccess":{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "rds:*",
                    "application-autoscaling:DeleteScalingPolicy",
                    "application-autoscaling:DeregisterScalableTarget",
                    "application-autoscaling:DescribeScalableTargets",
                    "application-autoscaling:DescribeScalingActivities",
                    "application-autoscaling:DescribeScalingPolicies",
                    "application-autoscaling:PutScalingPolicy",
                    "application-autoscaling:RegisterScalableTarget",
                    "cloudwatch:DescribeAlarms",
                    "cloudwatch:GetMetricStatistics",
                    "cloudwatch:PutMetricAlarm",
                    "cloudwatch:DeleteAlarms",
                    "ec2:DescribeAccountAttributes",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:DescribeCoipPools",
                    "ec2:DescribeInternetGateways",
                    "ec2:DescribeLocalGatewayRouteTables",
                    "ec2:DescribeLocalGatewayRouteTableVpcAssociations",
                    "ec2:DescribeLocalGateways",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeVpcAttribute",
                    "ec2:DescribeVpcs",
                    "ec2:GetCoipPoolUsage",
                    "sns:ListSubscriptions",
                    "sns:ListTopics",
                    "sns:Publish",
                    "logs:DescribeLogStreams",
                    "logs:GetLogEvents",
                    "outposts:GetOutpostInstanceTypes"
                ],
                "Effect": "Allow",
                "Resource": "*"
            },
            {
                "Action": "pi:*",
                "Effect": "Allow",
                "Resource": "arn:aws:pi:*:*:metrics/rds/*"
            },
            {
                "Action": "iam:CreateServiceLinkedRole",
                "Effect": "Allow",
                "Resource": "*",
                "Condition": {
                    "StringLike": {
                        "iam:AWSServiceName": [
                            "rds.amazonaws.com",
                            "rds.application-autoscaling.amazonaws.com"
                        ]
                    }
                }
            }
        ]
    },

}