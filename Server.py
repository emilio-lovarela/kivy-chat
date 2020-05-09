"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SOCK_DGRAM
from threading import Thread

# Server class
class Server(object):

	# Variables saving clients information
	clients = {}
	user = 1

	# Connection variables
	BUFSIZ = 1024

	def create_server(self, PORT):
		"""Init the server listen"""
		self.SERVER = socket(AF_INET, SOCK_STREAM)
		self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.SERVER.bind(('',PORT))
		self.SERVER.listen(5)
		ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()

	def kill_server(self):
		"""kill server when token changes"""
		self.SERVER.close()
		for client in self.clients.copy():
			client.close()

	def LAN_connection(self):
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(('10.255.255.255', 1))
		HOST = s.getsockname()[0]
		s.close()
		return HOST

	def accept_incoming_connections(self):
		"""Sets up handling for incoming clients."""
		while True:
			try:
				client, client_address = self.SERVER.accept()
				client.send(bytes('n' + str(len(self.clients) + 1), "utf8"))
				Thread(target=self.handle_client, args=(client,)).start()
			except:
				break

	def handle_client(self, client):  # Takes client socket as argument.
		"""Handles a single client connection."""

		indi_user = "User" + str(self.user)
		self.broadcast(bytes("1", "utf8"), client, "a")

		self.clients[client] = indi_user
		self.user += 1

		while True:
			try:
				msg = client.recv(self.BUFSIZ)
				self.broadcast(msg, client, "m" + indi_user + ": ")
			except:
				client.close() # Disconect client
				del self.clients[client]
				self.user -= 1
				self.broadcast(bytes("-1", "utf8"), client, "a")
				break

	def broadcast(self, msg, client, prefix=""):
		"""Broadcasts a message to all the clients."""

		for sock in self.clients:
			if sock != client:
				sock.send(bytes(prefix, "utf8") + msg)