#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from Client import Chat_multiple
from Server import Server
from threading import Thread
from socket import gethostbyname, getfqdn

Builder.load_file("Client.kv")

class ManageClass(StackLayout):
	
	chat_class = Chat_multiple() # Chat popup class
	server_class = Server() # Server instance

	# Connection socket variables
	PORT = 3300
	HOST = gethostbyname(getfqdn()) # ip adress to connect
	BUFSIZ = 1024

	# Fire popup
	def fire_popup(self):
		self.chat_class.bind(on_dismiss=self.close_popup)
		self.chat_class.open()

	def close_popup(self, _):
		self.chat_but.background_normal = "icons/chat_inactive.png" # Update chat_button state
		self.chat_but.text = ""

	# Create the thread to invoke server creation
	def server_thread(self):
		t = Thread(target=self.background_server_listen)
		t.daemon = True
		t.start()

	# Background checking new messages from server
	def background_server_listen(self):
		self.server_class.create_server(self.PORT) # Host the server

	# Background server listen
	def background_Thread_creation_listen(self):

		# Connect to server if exists
		self.client_socket = self.chat_class.connect_to_server(self.HOST, self.PORT)
		if self.client_socket == -1:
			print("error")
			return

		# Create the thread to invoke function
		t = Thread(target=self.receive_from_server)
		# Set daemon to true so the thread dies when app is closed
		t.daemon = True
		# Start the thread
		t.start()

	# Reciving messages
	def receive_from_server(self):
		"""Handles receiving of messages."""
		while True:
			try:
				msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
				# Classify the message
				if msg[0] == "m":
					self.chat_class.receive_from_server(msg[1:])
					self.chat_but.background_normal = "icons/chat_active.png" # Update chat_button state
					self.chat_but.text = "'"
				elif msg[0] == "n": # Initial number of users
					self.chat_class.number_users = str(int(msg[1:]))
				elif msg[0] == "a": # New or delete user
					self.chat_class.number_users = str(int(self.chat_class.number_users) + int(msg[1:]))
			except:
				break


class ChatApp(App):

    def build(self):
        return ManageClass()

if __name__ == '__main__':
    ChatApp().run()