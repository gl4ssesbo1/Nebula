import sys
import operator
import socketio
from termcolor import colored

from core.database.models import WebsocketListener
from core.database.models import WebsocketParticle

server_io = socketio.AsyncServer(async_mode='asgi')

# Triggered when a client connects to our socket.
@server_io.event
def connect(sid, socket):
    #print(colored("[*] New client connected from {} and was given the id {}".format(client['address'], client['id']), "green"))
    print(colored("[*] New client connected and was given the id {}".format(sid), "green"))
    #print(sid, 'connected')


# Triggered when a client disconnects from our socket
@server_io.event
def disconnect(sid):
    print(colored("[*] Client with ID {} disconnected".format(sid), "red"))


@server_io.event
def get_task_output(sid, listener_name, listener_task_id, task_output):
    try:
        listener_object = WebsocketListener.objects.get(listener_name=listener_name).json()
        listener_tasks = listener_object['listener_tasks']
        if len(listener_tasks) == 0:
            pass
        else:
            for task in listener_tasks:
                if task["listener_task_id"] == listener_task_id:
                    task['listener_task_output'] = task_output

            listener_object['listener_tasks'] = listener_tasks
            try:
                WebsocketListener.objects.get(listener_name=listener_name).update(**listener_object)
                server_io.emit("ok", {"task": "ok"}, to=sid)
            except Exception as e:
                print("[*] {}".format(sys.exc_info()))
                server_io.emit("error", {"task": "notok"}, to=sid)

    except Exception as e:
        print("[*] {}".format(sys.exc_info()))

@server_io.event
def get_task(sid, listener_name):
    tasks_to_send = []
    try:
        listener_tasks = WebsocketListener.objects.get(listener_name=listener_name).json()['listener_tasks']
        if len(listener_tasks) == 0:
            pass
        else:
            for task in listener_tasks:
                if task["listener_task_status"] == "Pending":
                    tasks_to_send.append(task)

            tasks_to_send.sort(key=operator.itemgetter('listener_task_id'))
            server_io.emit("task", tasks_to_send[0], to=sid)

    except Exception as e:
        print("[*] {}".format(sys.exc_info()))




