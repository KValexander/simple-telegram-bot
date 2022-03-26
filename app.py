# Libraries
import json
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

		self.current_command = None

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
				self.current_command = None

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
		print(command)

		# /start
		# Start app
		if command == "start":
			sendMessage(self.chat_id, "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")

		# /upload
		# Image upload
		elif command == "upload":
			self.current_command = command
			sendMessage(self.chat_id, "Вставьте изображение (не более 10 за раз для корректного добавления)")

		# /view
		# Image view
		elif command == "view":
			if not self.outPhotos(self.storage.getPhotos(self.chat_id), self.chat_id):
				sendMessage(self.chat_id, "Добавленные изображения отсутствуют")
		
		# /add_chat
		# Add chat to post
		elif command == "add_chat":
			pass

	# Add photo
	def addPhoto(self, file_id):
		pass

	# Out photos
	def outPhotos(self, array, chat_id):
		count = len(array)
		
		if not count: return False

		for photos in array:
			sendMediaGroup(chat_id, json.dumps(photos))

		if chat_id == self.chat_id:
			sendMessage(chat_id, f"Всего изображений: {count}")