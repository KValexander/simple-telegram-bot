# Libraries
import threading

# Files
from methods import *

# Classes
from storage import Storage

# Class App
class App:
	# Constructor
	def __init__(self):
		self.chat_id = 0
		self.update_id = 0
		self.update_limit = 30

		self.current_command = ""

		self.storage = Storage()

	# Get data
	def getData(self, filtration=False):
		offset = f"offset={self.update_id - self.update_limit}"
		response = getUpdates(offset)
		if filtration:
			response = [x for x in response["result"] if "message" in x]
		return response

	# Get message
	def getMessageText(self):
		# Get data
		data = self.getData(True)
		if len(data) == 0: return False

		# Get update object
		upd_obj = data[-1]
		self.chat_id = upd_obj["message"]["chat"]["id"]

		# Check update_id
		if self.update_id == 0:
			self.update_id = upd_obj["update_id"]

		if upd_obj["update_id"] != self.update_id:

			# Command processing
			if self.current_command:
				self.commandProcessing(data)

			# Return message text
			if "text" in upd_obj["message"]:
				self.update_id = upd_obj["update_id"]
				return upd_obj["message"]["text"]
	
	# Command processing
	def commandProcessing(self):
		pass

	# Data update
	def update(self):
		# Get message text
		text = self.getMessageText()

		# Command initialization
		if text in commands:
			self.commandInit(commands[text])

	# Command initialization
	def commandInit(self, command):

		# /start
		if command == "start":
			sendMessage(self.chat_id, "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")
