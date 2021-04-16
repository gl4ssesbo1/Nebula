# Nebula
Nebula is a Cloud and (hopefully) DevOps Penetration Testing framework. 
It is build with modules for each provider and each functionality. As of April 2021, it only covers AWS, but is currently an ongoing project and hopefully will continue to grow to test GCP, Azure, Kubernetes, Docker, or automation engines like Ansiable, Terraform, Chef, etc.

**Currently covers:**
- S3 Bucket name bruteforce
- IAM, EC2, S3 and Lambda Enumeration
- IAM, EC2, and S3 exploitation
- Custom HTTP User-Agent

**There are currently 50 modules covering:**
- Reconnaissance
- Enumeration
- Exploit
- Cleanup

## Installation
Nebula is coded in python3.8 and tested on python3.8 and 3.9. It uses boto3 library to access AWS. To install, just install python 3.8+ and install libraries required from *requirements.txt*

```
python3.8 -m pip install -r requirements.txt 
```
Then just run *main.py*
```
python3.8 ./main.py
```
## Usage
```
python3.9.exe .\main.py -b
                -------------------------------------------------------------
                50 aws          0 gcp           0 azure         0 office365
                0 docker        0 kubernetes
                -------------------------------------------------------------
                50 modules      2 cleanup               0 detection
                41 enum         6 exploit               0 persistence
                0 listeners     0 lateral movement      0 detection bypass
                0 privesc       1 reconnaissance        0 stager
                -------------------------------------------------------------
()()(AWS) >>>
```
### Listing modules
You can list all the modules or specific module:
```
()()(AWS) >>> show modules
        cleanup/aws_iam_delete_access_key                                     Delete access key of a user by providing
                                                                                it.

        cleanup/aws_iam_delete_login_profile                                  Delete access of a user to the Management
                                                                                Console

        enum/aws_ec2_enum_elastic_ips                                         Lists User data of an Instance provided.
                                                                                Requires Secret Key and Access Key of an IAM that has access
                                                                                to it.

        enum/aws_ec2_enum_images                                              List all ec2 images. Needs credentials of an
                                                                                IAM with DescribeImages right. Output is dumpled on a file.
                                                                                It takes a sh*tload of time, unfortunately. And boy, is it a
                                                                                huge output.

        enum/aws_ec2_enum_instances                                           Describes instances attribues: Instances, VCP,
                                                                                Zones, Images, Security Groups, Snapshots, Subnets, Tags,
                                                                                Volumes. Requires Secret Key and Access Key of an IAM that
                                                                                has access to all or any of the API calls:
                                                                                DescribeAvailabilityZones, DescribeImages,
                                                                                DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups,
                                                                                DescribeSnapshots, DescribeSubnets, DescribeTags,
                                                                                DescribeVolumes, DescribeVpcs
```
