# Nebula
<img src="./img/logo.png" alt="logo" width="200"/>

Nebula is a Cloud and (hopefully) DevOps Penetration Testing framework. 
It is build with modules for each provider and each functionality. As of April 2021, it only covers AWS, but is currently an ongoing project and hopefully will continue to grow to test GCP, Azure, Kubernetes, Docker, or automation engines like Ansible, Terraform, Chef, etc.

**Currently covers:**
- S3 Bucket name bruteforce
- IAM, EC2, S3, STS and Lambda Enumeration
- IAM, EC2, STS, and S3 exploitation
- SSM Enumeration + Exploitation
- Custom HTTP User-Agent
- Enumerate Read Privileges (working on write privs)
- Reverse Shell
- No creds Reconnaisance

**There are currently 67 modules covering:**
- Reconnaissance
- Enumeration
- Exploit
- Cleanup
- Reverse Shell

## Installation

### Docker
#### From Dockerhub
Clone the Nebula Repo from Github and pull Nebula Docker image:

``` 
git clone https://github.com/gl4ssesbo1/Nebula
docker pull gl4ssesbo1/nebula:latest
```
and then run main.py through:

```
cd Nebula
docker run -v $(pwd):/app -ti gl4ssesbo1/nebula:latest main.py
```
Remember to not forget -v option, because it allows files to be saved on the system even after removing the docker image.

#### Using DockerFile
Clone the Nebula Repo from Github and build Docker image locally:

``` 
git clone https://github.com/gl4ssesbo1/Nebula
docker build -t nebula .
```
then run main.py through:

```
docker run -v Nebula:/app -ti nebula main.py
```

Remember to not forget -v option, because it allows files to be saved on the system even after removing the docker image.

#### Adding port mapping
If you want to run a shell, also add the -p option:
```
cd Nebula
docker run -p <host port>:<container port> -v $(pwd):/app -ti gl4ssesbo1/nebula:latest main.py
```

### Installed on System
Nebula is coded in python3.8 and tested on python3.8 and 3.9. It uses boto3 library to access AWS. To install, just install python 3.8+ and install libraries required from *requirements.txt*

```
python3.8 -m pip install -r requirements.txt 
```

Then install session-manager-plugin. This is needed for SSM modules:
```
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
dpkg -i session-manager-plugin.deb
```
On windows devices, since less is not installed, I got one from **https://github.com/jftuga/less-Windows**
The prebuilt binary is saved on directory less_binary. Just add that directory to the PATH environment variable and it will be ok.

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
### Help
Running *help* command, will give you a list of the commands that can be used:
```
()()(AWS) >>> help

    Help Command:               Description:
    -------------               ------------

    help                        Show help for all the commands
    help credentials            Show help for credentials
    help module                 Show help for modules
    help workspace              Show help for credentials
    help user-agent             Show help for credentials
    help shell                  Show help for shell connections


    Module Commands             Description
    ---------------             -----------

    show modules                List all the modules
    show enum                   List all Enumeration modules
    show exploit                List all Exploit modules
    show persistence            List all Persistence modules
    show privesc                List all Privilege Escalation modules
    show reconnaissance         List all Reconnaissance modules
    show listener               List all Reconnaissance modules
    show cleanup                List all Enumeration modules
    show detection              List all Exploit modules
    show detectionbypass        List all Persistence modules
    show lateralmovement        List all Privilege Escalation modules
    show stager                 List all Reconnaissance modules

    use module <module>         Use a module.
    options                     Show options of a module you have selected.
    run                         Run a module you have selected. Eg: 'run <module name>'
    search                      Search for a module via pattern. Eg: 'search s3'
    back                        Unselect a module
    set <option>                Set option of a module. Need to have the module used first.
    unset <option>              Unset option of a module. Need to have the module used first.


    User-Agent commands         Description
    -------------------         -----------

    set user-agent windows      Set a windows client user agent
    set user-agent linux        Set a linux client user agent
    set user-agent custom       Set a custom client user agent
    show user-agent             Show the current user-agent
    unset user-agent            Use the user agent that boto3 produces


    Workspace Commands          Description
    ------------------          -----------

    create workspace <wp>       Create a workspace
    use workspace <wp>          Use one of the workspaces
    remove workspace <wp>       Remove a workspace


    Shell commands              Description
    -------------------         -----------

    shell check_env             Check the environment you are in, get data and meta-data
    shell exit                  Kill a connection
    shell <command>             Run a command on a system. You don't need " on the command, just shell <command1> <command2>
```
### Enum Privs
When you have a set of credentials, you can enter *getuid* to get the user or *enum_user_privs* to check the Read permission of a set of credentials.
#### GetUID
```
(test)()(AWS) >>> getuid
------------------------------------------------
UserId: A******************Q
------------------------------------------------
        UserID: A******************Q
        Arn: arn:aws:iam::012345678912:user/user_user
        Account: 012345678912
[*] Output is saved to './workspaces/test/12_07_2021_02_22_54_getuid_dev_brian'
```

If the creds do not have the below privs on himself,
```
STS:GetUserIdentity
IAM:GetUser
IAM:ListAttachedUserPolicies
IAM:GetPolicy (for all policies)
```
you will get an error:
```
[*] An error occurred (AccessDenied) when calling the GetUser operation: User: arn:aws:iam::012345678912:user/user_user is not authorized to perform: iam:GetUser on resource: user user_user
```
#### Enum_User_Privs
This command checks List and Describe Privileges on a set of credentials.
```
(test)()(AWS) >>> enum_user_privs
User: user_user
        UserID: A******************Q
        Arn: arn:aws:iam::012345678912:user/user_user
        Account: 012345678912
--------------------------
Service: ec2
--------------------------
[*] Trying the 'Describe' functions:
[*] 'describe_account_attributes' worked!
[*] 'describe_addresses' worked!
[*] 'describe_aggregate_id_format' worked!
[*] 'describe_availability_zones' worked!
[*] 'describe_bundle_tasks' worked!
[*] 'describe_capacity_reservations' worked!
[*] 'describe_client_vpn_endpoints' worked!
[*] 'describe_coip_pools' worked!
[*] 'describe_customer_gateways' worked!
[*] 'describe_dhcp_options' worked!
[*] 'describe_egress_only_internet_gateways' worked!
^C[*] Stopping. It might take a while. Please wait.
[*] Output of the allowed functions is saved to './workspaces/test/12_07_2021_02_24_09_enum_user_privs'
[*] The list of the allowed functions is saved to './workspaces/test/12_07_2021_02_24_09_allowed_functions'
```

### Modules
#### Listing modules
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

And like that you can use:
```
     show module
     show enum
     show exploit
     show persistence
     show privesc
     show reconnaissance
     show listener
     show cleanup
     show detection
     show detectionbypass
     show lateralmovement
     show stager
```
#### Searching for modules
Use **search** command to search modules with a specific word:
```
()()(AWS) >>> search instance
        enum/aws_ec2_enum_instances                                           Describes instances attribues: Instances, VCP,
                                                                                Zones, Images, Security Groups, Snapshots, Subnets, Tags,
                                                                                Volumes. Requires Secret Key and Access Key of an IAM that
                                                                                has access to all or any of the API calls:
                                                                                DescribeAvailabilityZones, DescribeImages,
                                                                                DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups,
                                                                                DescribeSnapshots, DescribeSubnets, DescribeTags,
                                                                                DescribeVolumes, DescribeVpcs

        enum/aws_iam_list_instance_profiles                                   List all the instance profiles.

        exploit/aws_ec2_create_instance_with_user_data                        You must provide policies in JSON format in
                                                                                IAM. However, for AWS CloudFormation templates formatted in
                                                                                YAML, you can provide the policy in JSON or YAML format. AWS
                                                                                CloudFormation always converts a YAML policy to JSON format
                                                                                before submitting it to IAM.

()()(AWS) >>>
```

#### Using Modules
To use a module, just type *use* and the name of the module. The 3 brackets will have the name of the module.
```
(work1)()(enum/aws_ec2_enum_instances) >>> use module enum/aws_iam_get_group
(work1)()(enum/aws_ec2_enum_instances) >>>
```

#### Options
Using *options*, we can list the information on the module:
```
(work1)()(enum/aws_ec2_enum_instances) >>> options
Desctiption:
-----------------------------
        Describes instances attribues: Instances, VCP, Zones, Images, Security Groups, Snapshots, Subnets, Tags, Volumes. Requires Secret Key and Access Key of an IAM that has access to all or any of the API calls: DescribeAvailabilityZones, DescribeImages, DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups, DescribeSnapshots, DescribeSubnets, DescribeTags, DescribeVolumes, DescribeVpcs

Author:
-----------------------------
        name:   gl4ssesbo1
        twitter:        https://twitter.com/gl4ssesbo1
        github: https://github.com/gl4ssesbo1
        blog:   https://www.pepperclipp.com/

AWSCLI Command:
-----------------------------
        aws ec2 describe-instances --region {} --profile {}

Needs Credentials: True
-----------------------------

Options:
-----------------------------
        SERVICE:        ec2
                Required: true
                Description: The service that will be used to run the module. It cannot be changed.

        INSTANCE-ID:
                Required: false
                Description: The ID of the instance you want to enumerate. If not supplied, all instances will be enumerated.

(work1)()(enum/aws_ec2_enum_instances) >>>
```
To set options, use *set* and the name of the option:
```
(work1)()(enum/aws_ec2_enum_instances) >>> set INSTANCE-ID 1234
(work1)()(enum/aws_ec2_enum_instances) >>> options
Desctiption:
-----------------------------
        Describes instances attribues: Instances, VCP, Zones, Images, Security Groups, Snapshots, Subnets, Tags, Volumes. Requires Secret Key and Access Key of an IAM that has access to all or any of the API calls: DescribeAvailabilityZones, DescribeImages, DescribeInstances, DescribeKeyPairs, DescribeSecurityGroups, DescribeSnapshots, DescribeSubnets, DescribeTags, DescribeVolumes, DescribeVpcs

Author:
-----------------------------
        name:   gl4ssesbo1
        twitter:        https://twitter.com/gl4ssesbo1
        github: https://github.com/gl4ssesbo1
        blog:   https://www.pepperclipp.com/

Needs Credentials: True
-----------------------------

AWSCLI Command:
-----------------------------
        aws ec2 describe-instances --region {} --profile {}

Options:
-----------------------------
        SERVICE:        ec2
                Required: true
                Description: The service that will be used to run the module. It cannot be changed.

        INSTANCE-ID:    1234
                Required: false
                Description: The ID of the instance you want to enumerate. If not supplied, all instances will be enumerated.

(work1)()(enum/aws_ec2_enum_instances) >>>
```
Also unsetting them, using **unset**.
```
(work1)()(enum/aws_ec2_enum_instances) >>> unset INSTANCE-ID
(work1)()(enum/aws_ec2_enum_instances) >>>
```
#### Running the module
To run the module, if it requires credentials, you will need to have imported a set of credentials with the permission required to run it. This is shown on a module's options as:
```
Needs Credentials: True
-----------------------------
```
To run it, just enter **run**. Depending on the output, it will either show a pagainated view, or just print it. The pagination, uses less binary, which for Windows uses the binary from **https://github.com/jftuga/less-Windows**. A copy of the exe is on less_binary directory.
The output is also saved on files on the workspace directory:
```
(work1)()(enum/aws_ec2_enum_instances) >>> run
[*] Content dumped on file './workspaces/work1/16_04_2021_18_16_48_ec2_enum_instances'.
```

### Credentials
####Inputing Credentials
Nebula can use both AccessKeyID + SecretKey combination and AccessKeyID + SecretKey+SessionKey combination to authenticate into the infratructure.
To insert a set of credentials, use:
```
()()(AWS) >>> set credentials test1
Profile Name: test1
Access Key ID: A*********2
Secret Key ID: a****************************7
Region: us-west-3

Do you also have a session token?[y/N]
[*] Credentials set. Use 'show credentials' to check them.
[*] Currect credential profile set to 'test1'.Use 'show current-creds' to check them.
```
And you will get some inputs allowing you to set them. Session token can be added when entering credentials, by inputing **y** when asked **Do you also have a session token?[y/N]**.

####Using Credentials
To use another credential, just enter:
```
()()(AWS) >>> use credentials test1
[*] Currect credential profile set to 'test1'.Use 'show current-creds' to check them.
```
####Current Credentials
When you enter the credentials, they are automatically made the current credentials, meaning the ones you will authenticate with. To check the current credentials, use:
```
()()(AWS) >>> show current-creds
{
    "profile": "test1",
    "access_key_id": "A*********2",
    "secret_key": "a****************************7",
    "region": "us-west-3"
}
```
####Removing Credentials
In case you don't want your credentials, you can can remove them using:
```
()()(AWS) >>> remove credentials test1
You are about to remove credential 'test1'. Are you sure? [y/N] y
```
####Dumping and importing credentials
In case you want your credentials saved on the machine, you can use:
```
()()(AWS) >>> dump credentials
[*] Credentials dumped on file './credentials/16_04_2021_17_37_59'.
```
And they will be saved on a file containing the time and date of the dump on directory *credentials* on Nebula directory.
To import them, just enter:
```
()()(AWS) >>> import credentials 16_04_2021_17_37_59
()()(AWS) >>> show credentials
[
    {
        "profile": "test1",
        "access_key_id": "A*********2",
        "secret_key": "a****************************7",
        "region": "us-west-3"
    }
]
```
### Workspaces
Nebula uses workspaces to save the output from every command. The output is saved as json data (except for s3_name_fuzzer which saves it as XML) on a folder created on directory *workspaces*.
#### Create Workspaces
To create one, enter:
```
()()(AWS) >>> create workspace work1
[*] Workspace 'work1' created.
[*] Current workspace set at 'work1'.
(work1)()(AWS) >>> ls ./workspaces


    Directory: C:\Users\***\Desktop\Nebula\workspaces


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         4/16/2021   5:42 PM                work1
-a----         4/16/2021   4:40 PM              0 __init__.py
```
When created, the first brackets will contain the name of the workspace you are working at.
If you want to use an existing workspace, just type:
```
()()(AWS) >>> use workspace work1
(work1)()(AWS) >>>
```
Workspaces are required to be used, so even if you are not using any at the moment, while running a module, it will ask you to create one with random name or to just create one with a custom name yourself.
```
()()(enum/aws_ec2_enum_instances) >>> run
A workspace is not configured. Workstation 'qxryiuct' will be created. Are you sure? [y/N] n
[*] Create a workstation first using 'create workstation <workstation name>'.
()()(enum/aws_ec2_enum_instances) >>>
```
#### List workspaces
To get a list of workspaces, use:
```
(work1)()(enum/aws_ec2_enum_instances) >>> show workspaces
-----------------------------------
Workspaces:
-----------------------------------
        work1

(work1)()(enum/aws_ec2_enum_instances) >>>
```
#### Remove Workspaces
To remove a workspace, enter:
```
()()(AWS) >>> remove workspace work1
[*] Are you sure you want to delete the workspace? [y/N] y
()()(AWS) >>> show workspaces
-----------------------------------
Workspaces:
-----------------------------------

()()(AWS) >>>
```
### Reverse Shell
To create a Reverse Shell, you need to create a stager and run a listener. To use this feature, you need to have Nebula run as root (to open ports).
#### Stager
To generate a stager, use modules on *stagers*:
```
()()(AWS) >>> use module stager/aws_python_tcp
()()(stager/aws_python_tcp) >>> options
Desctiption:
-----------------------------
        The TCP Reverse Shell that is used by listeners/aws_python_tcp_listener

Author:
-----------------------------
        name:   gl4ssesbo1
        twitter:        https://twitter.com/gl4ssesbo1
        github: https://github.com/gl4ssesbo1
        blog:   https://www.pepperclipp.com/

Needs Credentials: False
-----------------------------

AWSCLI Command:
-----------------------------
        None

Options:
-----------------------------
        SERVICE:        none
                Required: true
                Description: The service that will be used to run the module. It cannot be changed.

        HOST:
                Required: true
                Description: The Host/IP of the C2 Server.

        PORT:
                Required: true
                Description: The C2 Server Port.

        FORMAT:
                Required: true
                Description: The format of the stager. Currently only allows 'py' for Python and 'elf' for ELF Binary.

        CALLBACK-TIME:  None
                Required: true
                Description: The time in seconds between callbacks from Stager. The Stager calls back even if the server crashes or is stoped in a loop.

        OUTPUT-FILE-NAME:
                Required: true
                Description: The name of the stager output file.
```
The options to fill are:
   - **HOST**: The IP or domain of the C2 Server
   - **Port**: The C2 Server Port
   - **Format**: Currently only supports python raw file and elf binary
   - **Callback-Time**: The time in seconds for which the sessions should call back. It calls back even if a current session is up, and even if the server crushes or is closed, so that you don't loose access to the machine.
   - **Output File Name**: The name of the output file.

Running the module will generate a stager saved on **./workspaces/workspacename/stagername**

#### Listener
The listener is simple. Just configure Host (by default set to 0.0.0.0) and Port and it creates the server. To run the listener, you need to have Nebula run as root.
```
()()(stager/aws_python_tcp) >>> use module listeners/aws_python_tcp_listener
()()(listeners/aws_python_tcp_listener) >>> options
Desctiption:
-----------------------------
        TCP Listener for Reverse Shell stagers/aws_python_tcp

Author:
-----------------------------
        name:   gl4ssesbo1
        twitter:        https://twitter.com/gl4ssesbo1
        github: https://github.com/gl4ssesbo1
        blog:   https://www.pepperclipp.com/

Needs Credentials: False
-----------------------------

AWSCLI Command:
-----------------------------
        None

Options:
-----------------------------
        SERVICE:        none
                Required: true
                Description: The service that will be used to run the module. It cannot be changed.

        HOST:   0.0.0.0
                Required: true
                Description: The Host/IP of the C2 Server.

        PORT:
                Required: true
                Description: The C2 Server Port.
```

### User Agents
User agents can be set as linux ones, windows ones or custom. To show them, just use *show*.
```
()()(AWS) >>> set user-agent linux
User Agent: Boto3/1.9.89 Python/3.8.1 Linux/4.1.2-34-generic was set
()()(AWS) >>> show user-agent
[*] User Agent is: Boto3/1.9.89 Python/3.8.1 Linux/4.1.2-34-generic
()()(AWS) >>> set user-agent windows
User Agent: Boto3/1.7.48 Python/3.9.1 Windows/7 Botocore/1.10.48 was set
()()(AWS) >>> show user-agent
[*] User Agent is: Boto3/1.7.48 Python/3.9.1 Windows/7 Botocore/1.10.48
()()(AWS) >>> set user-agent custom
Enter the User-Agent you want: sth
User Agent: sth was set
()()(AWS) >>> show user-agent
[*] User Agent is: sth
()()(AWS) >>>
```
To unset a user agent, enter:
```
()()(AWS) >>> unset user-agent
[*] User Agent set to empty.
```
Which will have the system's user agent.
