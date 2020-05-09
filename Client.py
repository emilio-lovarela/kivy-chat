from socket import AF_INET, socket, SOCK_STREAM
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

class SmoothLabel(Label):
    pass

class SmoothLabelMy(Label):
    pass

class Chat_multiple(Popup):

	# Connection variables
	BUFSIZ = 1024
	number_users = StringProperty("1")

	# Connect to server, check if exists in dropbox
	def connect_to_server(self, HOST, PORT):	
		self.client_socket = socket(AF_INET, SOCK_STREAM)
		try:
			self.client_socket.connect((HOST, PORT))
			return  self.client_socket
		except:
			return -1

	# Update chat window
	def receive_from_server(self, msg):
		
		# Separate name from message
		pos = msg.rfind(":")
		if pos == -1:
			name = ""
		else:
			name = msg[0:pos] + "\n"
			msg = msg[pos + 3: ]

		label = SmoothLabel(text=msg)
		label.texture_update()
		max_size = self.insertion_text.size[0] - 128

		# Check render size and update
		if max_size - label.size[0] < 0:
			msg = self.update_text_lines(max_size, msg, True, "recei")
			label = SmoothLabel(text=name + msg)
			label.texture_update()
		else:
			label = SmoothLabel(text=name + msg)
			label.texture_update()

		# Insert label in chat
		self.ids.insert_text.add_widget(label)
		self.scroll_main.scroll_to(label) # Automatic scroll to the bottom

	def send_msg(self, msg):
		"""Handles sending of messages."""
		if msg == "":
			return

		# Auto-update and send the message
		try:
			self.client_socket.send(bytes("m" + msg, "utf8"))
			label = SmoothLabelMy(text=msg)
			label.texture_update()
			max_size = self.insertion_text.size[0] - 128

			# Check render size and update
			if max_size - label.size[0] < 0:
				msg = self.update_text_lines(max_size, msg, True, "send")
				label = SmoothLabelMy(text=msg, padding_x=93)
				label.texture_update()
			else:
				label.padding_x = self.insertion_text.size[0] - label.size[0] - 37

			# Insert label in chat
			self.ids.insert_text.add_widget(label)
			self.scroll_main.scroll_to(label) # Automatic scroll to the bottom
		except:
			print("No internet")

	# Insert jumps between lines if the text is too length
	def update_text_lines(self, max_size, text, mode, type_en):
		if mode == True:
			text_part = text.split(" ")
			space = " "
		else:
			text_part = text
			space = ""

		new_text = ""
		tex_last = []
		msg = ""
		
		count = 0
		for part in text_part:
			if count == 0:
				new_text2 = part
			else:
				new_text2 = new_text2 + space + part

			if type_en == "send":
				label = SmoothLabelMy(text=new_text2)
				label.texture_update()
			else:
				label = SmoothLabel(text=new_text2)
				label.texture_update()

			# Check render size and update
			if max_size - label.size[0] > 0:
				new_text = new_text2
				count += 1
			else:

				count += 1
				tex_last.append(new_text)

				# Divide word too length
				if type_en == "send":
					label = SmoothLabelMy(text=part)
					label.texture_update()
				else:
					label = SmoothLabel(text=part)
					label.texture_update()

				if max_size - label.size[0] < 0 and mode == True:
					if count > 1:
						tex_last.append("\n")

					word = self.update_text_lines(max_size, part, False, type_en)
					tex_last.append(word)
					new_text = ""
					continue

				# Add \n
				new_text = ""
				if count == len(text_part):
					break
				tex_last.append("\n")
				new_text2 = part

		# Reconvert to string
		tex_last.append(new_text)
		for prhase in tex_last:
			msg = msg + prhase

		return msg