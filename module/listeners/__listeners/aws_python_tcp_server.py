import os
import socket
import sys
from termcolor import colored
import random
import string
from threading import Thread
from queue import Queue
import json
import signal

global s
id = 0

sockets = {}
particles = {}
th = []

NR_OF_THREADS = 2
JOB_NUMBER = [1, 2]

threads = {}

q = Queue()

def socket_create():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def socket_bind():
    global s, sockets, id, q
    s.bind((HOST, PORT))
    print(colored("[*] Binding to {}:{}".format(HOST,PORT), 'green'))
    s.listen(10000)
    sockets[id] = {}
    sockets[id]['queue'] = q
    sockets[id]['socket'] = s
    sockets[id]['addr'] = (str(s).split(",")[4]).split("'")[1] + ":" + (str(s).split(",")[5]).split(")")[0]
    sockets[id]['type'] = ((str(s).split(",")[2])).split(".")[1]
    sockets[id]['module'] = 'aws_python_tcp_listener'
    id += 1
    print(colored("[*] Socket created {}:{}\n".format(HOST, PORT), 'green'))

def socket_accept():
    while True:
        global s, particles, WORKSPACE
        conn, addr = s.accept()
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(8))

        while os.path.exists("../../../workspaces/{}".format(name)):
            letters = string.ascii_lowercase
            name = ''.join(random.choice(letters) for i in range(8))

        #os.makedirs("../../../workspaces/{}".format(name))
        os.makedirs("./workspaces/{}/{}".format(WORKSPACE, name))

        conn.send(str.encode(''))
        info = conn.recv(2048).decode().strip("\n")

        s.setblocking(True)

        #conn.send(str.encode(''))
        #system = conn.recv(2048).decode()

        #conn.send(str.encode(''))
        #hostname = conn.recv(2048).decode()

        particle_info = json.loads(info)

        user = particle_info['USER']
        system = particle_info['SYSTEM']
        hostname = particle_info['HOSTNAME']
        ipss = particle_info['LAN_IP']

        '''
        conn.send(str.encode(''))
        ip = conn.recv(2048).decode()
        print(ip)
        '''

        print("{} '{}' {}: {} {} {}".format(
            colored("[*] Session", "green"),
            colored(name, "blue"),
            colored("established from", "green"),
            colored(addr, "blue"),
            colored("with user", "green"),
            colored(user, "blue")
        ))

        particles[name] = {
            "socket": conn,
            "module":"aws_python_tcp_listener",
            "IP": addr[0],
            "Port": addr[1],
            "LAN_IP":addr[0],
            "User": user,
            "OS":system,
            "Hostname":hostname
        }

#def register_signal_handler():
#    signal.signal(signal.SIGINT, quit_gracefully)
#    signal.signal(signal.SIGTERM, quit_gracefully)
#    return

def quit_gracefully(signal=None, frame=None):
    print('\nQuitting gracefully')
    for key,value in particles.items():
        try:
            conn = value['socket']
            conn.shutdown(2)
            conn.close()
        except Exception as e:
            print('Could not close connection %s' % str(e))
            # continue
    for key,value in sockets.items():
        sock = value['socket']
        if not sock == None:
            sock.close()
    sys.exit(0)

def recvall(conn, n):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def work():
    global sockets, WORKSPACE, s
    while True:
        x = q.get()
        try:
            if x == 1:
                try:
                    socket_create()
                    socket_bind()
                    socket_accept()
                except KeyboardInterrupt:
                    command = input(
                        colored("Are you sure you want to exit? [y/N] ", "red")
                    )
                    if command == "Y" or command == "y":
                        if sockets:
                            for key, value in sockets.items():
                                s = value['socket']
                                s.shutdown(2)
                                s.close()

                            print("All socket closed!")
                        exit()
                        sys.exit()
                    socket_create()
                    socket_bind()
                    socket_accept()

            if x == 2:
                sys.path.insert(0, "../../../")
                imported_module = __import__("main")
                workspace = WORKSPACE
                particle = ''
                terminal = colored('AWS', 'yellow')
                try:
                    imported_module.main(workspace, particle, terminal, particles, sockets)
                except KeyboardInterrupt:
                    command = input(
                        colored("Are you sure you want to exit? [y/N] ", "red")
                    )
                    if command == "Y" or command == "y":
                        if sockets:
                            for key, value in sockets.items():
                                s = value['socket']
                                s.shutdown(2)
                                s.close()

                            print("All socket closed!")
                        exit()
                        sys.exit()

                    imported_module.main(workspace, particle, terminal, particles, sockets)

            q.task_done()
        except:
            e = sys.exc_info()[1]
            print(colored("[*] {}".format(e), "red"))
            s.close()
            for i in q.queue:
                q.task_done()
            q.join()
            print(colored("[*] Socket Closed","yellow"))
            break
    print("broke")

def create_threads():
    #register_signal_handler()
    for _ in range(NR_OF_THREADS):
        thread = Thread(target=work, args=())
        thread.daemon = True
        th.append(thread)
        thread.start()
    return

def create_jobs():
    for x in JOB_NUMBER:
        q.put(x)
    q.join()

def main(host, port, workspace):
    global HOST
    global PORT
    global s
    global id
    global WORKSPACE

    WORKSPACE = workspace
    HOST = host
    PORT = port

    create_threads()
    create_jobs()