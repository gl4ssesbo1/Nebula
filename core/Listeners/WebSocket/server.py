from websocket_server import WebsocketServer
from termcolor import colored

# Called for every client connecting (after handshake)
def new_client(client, server):
	print(colored("[*] New client connected from {} and was given the id {}".format(client['address'], client['id']), "green"))
	#server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print(colored("[*] Client(%d) disconnected" % client['id'], "yellow"))


# Called when a client sends a message
def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'

	return message

def start_websocket_listener(port, cert, key):
	print(colored("[*] Listener started on port: {}".format(str(port)), "green"))
	server = WebsocketServer(port=port)
	if cert is not None and key is not None:
		server.cert = cert
		server.key = key

	server.set_fn_new_client(new_client)
	server.set_fn_client_left(client_left)
	server.set_fn_message_received(message_received)
	server.run_forever()

