# Libraries
import time
import json
import threading

# Files
from methods import *

# Classes
from storage import Storage
from commands import Commands

# Class App
class App:
	# Constructor
	def __init__(self):
		self.chat_id = 0
		self.update_id = 0
		self.update_limit = 30

		self.commands = []
		self.timers = []

		self.storage = Storage()
		self.cmd = Commands(self)

	# Get response
	def getResponse(self, filtration=False):
		offset = f"offset={self.update_id - self.update_limit}"
		response = getUpdates(offset)
		if filtration:
			response = [x for x in response["result"] if "message" in x]
		return response

	# Get message text
	def getMessageText(self):
		# Get data
		response = self.getResponse(True)
		if len(response) == 0: return False

		# Get update object
		update_dict = response[-1]
		self.chat_id = update_dict["message"]["chat"]["id"]

		# Check update_id
		if self.update_id == 0:
			self.update_id = update_dict["update_id"]

		# Catching a message
		if update_dict["update_id"] != self.update_id:
			
			# Command processing
			if len(self.commands):
				self.commandProcessing(response)

			# Return message text
			if "text" in update_dict["message"]:
				self.update_id = update_dict["update_id"]
				return update_dict["message"]["text"]
	
	# Command processing
	def commandProcessing(self, response):
		# Get command for current chat
		command = [x for x in self.commands if x["chat_id"] == self.chat_id]
		if not len(command): return

		# Processing distribution
		command = self.deleteCommand()["command"]
		self.cmd.processingDistribution(command, response)

	# Data update
	def update(self):
		# Get message text
		text = self.getMessageText()

		# Command initialization
		if text in commands:
			self.cmd.commandDistribution(commands[text])

	# Add command
	def addCommand(self, command):
		self.commands.append({
			"chat_id": self.chat_id,
			"command": command,
		})

	# Delete command
	def deleteCommand(self):
		result = []

		for index, command in enumerate(self.commands):
			if command["chat_id"] == self.chat_id:
				result = self.commands.pop(index)
				break

		return result

	# Get list
	def getList(self, key):
		result = self.storage.getList(self.chat_id, key)
		return result

	# Clear list
	def clearList(self, key, n=0):
		self.storage.clearList(self.chat_id, key, n)

	# Add chat
	def addChat(self, result):
		self.storage.addChat(self.chat_id, result)

	# Add message
	def addMessage(self, text):
		self.storage.addMessage(self.chat_id, text)

	# Add photo
	def addPhoto(self, file_id):
		photos = [] if type(file_id) == list else file_id

		# Add many photos
		if type(file_id) == list:
			for photo in file_id:
				photos.append(photo["message"]["photo"][0]["file_id"])

		self.storage.addPhoto(self.chat_id, photos)

	# Out messages
	def outMessages(self, array):
		if not len(array): return False
		select = "message" if "text" in array[0] else "chat"

		count = 1
		for message in array:
			text = f"{count}) {message['text']}" if select == "message" else f"{count}) {message['title']} ({message['id']})"
			sendMessage(self.chat_id, text)
			count += 1

		text = "Всего сообщений" if select == "message" else "Всего чатов"
		sendMessage(self.chat_id, f"{text}: {count - 1}")

		return True

	# Out photos
	def outPhotos(self, chat_id, array):
		if not len(array): return False

		count = 0
		for photos in array:
			sendMediaGroup(chat_id, json.dumps(photos.copy()))
			count += len(photos)

		if chat_id == self.chat_id:
			sendMessage(chat_id, f"Всего изображений: {count}")

		return True

	# Post messages
	def postMessages(self, chats, array):
		if not len(chats) or not len(array): return False
		
		for chat in chats:
			for message in array:
				sendMessage(chat["id"], message["text"])

		self.clearList("messages")

		return True

	# Post photos
	def postPhotos(self, chats, array, n=20):
		if not len(chats) or not len(array): return False

		for chat in chats:
			self.outPhotos(chat["id"], array)

		self.clearList("photos", n)

		return True

	# Add timer
	def addTimer(self, timer):
		self.timers.append({
			"chat_id": self.chat_id,
			"timer": timer
		})

	# Get timer
	def getTimer(self):
		for timer in self.timers:
			if timer["chat_id"] == self.chat_id:
				return timer

	# Delete timer
	def deleteTimer(self):
		for index, timer in enumerate(self.timers):
			if timer["chat_id"] == self.chat_id:
				del self.timers[index]
				return

	# Start timer message
	def startTimerMessage(self, chats, time=3):
		timer = threading.Timer(time, self.postTimeMessage, (chats, time,))
		self.addTimer(timer)
		timer.start()

	# Start timer photo
	def startTimerPhoto(self, chats, time=3):
		timer = threading.Timer(time, self.postTimePhoto, (chats, time,))
		self.addTimer(timer)
		timer.start()

	# Post time message
	def postTimeMessage(self, chats, time=3):
		message = self.storage.popList(self.chat_id, "messages")

		if not message:
			self.deleteTimer()
			sendMessage(self.chat_id, "Сообщения опубликованы")
			return
		
		for chat in chats:
			sendMessage(chat["id"], message["text"])

		timer = self.getTimer()
		timer["timer"] = threading.Timer(time, self.postTimeMessage, (chats, time,))
		timer["timer"].start()

	# Post time photo
	def postTimePhoto(self, chats, time=3):
		photo = self.storage.popList(self.chat_id, "photos")

		if not photo:
			self.deleteTimer()
			sendMessage(self.chat_id, "Изображения опубликованы")
			return

		for chat in chats:
			sendPhoto(chat["id"], photo["media"])

		timer = self.getTimer()
		timer["timer"] = threading.Timer(time, self.postTimePhoto, (chats, time,))
		timer["timer"].start()

	# Stop timer
	def stopTimer(self):
		timer = self.getTimer()
		timer["timer"].cancel()

		self.deleteTimer()

