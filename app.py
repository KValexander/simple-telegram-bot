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

		self.commands = []

		self.storage = Storage()

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

		command = self.deleteCommand(self.chat_id)["command"]
		update_dict = response[-1]

		# Upload chat
		if command == "upload_chat":

			# Upload chat
			if "text" in update_dict["message"]:
				chat = getChat(update_dict["message"]["text"])
				
				if chat["error_code"] != 400:
					self.addChat(update_dict["message"]["text"])

					# Success message
					sendMessage(self.chat_id, "Чат добавлено.\nДобавленные чаты можно посмотреть с помощью команды \"/view_chats\"")
				
				# Error message
				else: sendMessage(self.chat_id, "Чат не найден")

			# Error message
			else: sendMessage(self.chat_id, "Неверный формат")
		
		# Upload message
		elif command == "upload_message":

			# Upload message
			if "text" in update_dict["message"]:
				self.addMessage(update_dict["message"]["text"])

				# Success message
				sendMessage(self.chat_id, "Сообщение добавлено.\nДобавленные сообщения можно посмотреть с помощью команды \"/view_messages\"")

			# Error message
			else: sendMessage(self.chat_id, "Неверный формат")

		# Upload photos
		elif command == "upload_photos":
			
			# Upload photo
			if "photo" in update_dict["message"]:

				text = "Изображение добавлено"
				
				# Upload many photos
				if "media_group_id" in update_dict["message"]:
					
					# Selecting the desired group
					photos = [x for x in [y for y in response if "media_group_id" in y["message"]] if x["message"]["media_group_id"] == update_dict["message"]["media_group_id"]]
					self.addPhoto(photos)
					
					text = "Изображения добавлены"

				# Upload single photo
				else: self.addPhoto(update_dict["message"]["photo"][0]["file_id"])

				# Success message
				sendMessage(self.chat_id, f"{text}.\nДобавленные изображения можно посмотреть с помощью команды \"/view_photos\"")

			# Error message
			else: sendMessage(self.chat_id, "Неверный формат")

	# Data update
	def update(self):
		# Get message text
		text = self.getMessageText()

		# Command initialization
		if text in commands:
			self.commandInit(commands[text])

	# Add command
	def addCommand(self, chat_id, command):
		self.commands.append({
			"chat_id": chat_id,
			"command": command,
		})

	# Delete command
	def deleteCommand(self, chat_id):
		result = []

		for index, command in enumerate(self.commands):
			if command["chat_id"] == chat_id:
				result = self.commands.pop(index)
				break

		return result

	# Command initialization
	def commandInit(self, command):
		print(command)

		# /start
		# Start
		if command == "start":
			sendMessage(self.chat_id, "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")

		# /upload_chat
		# Upload chat
		elif command == "upload_chat":
			self.addCommand(self.chat_id, command)
			sendMessage(self.chat_id, "Введите название чата в формате @name или id (бот должен находится на должности администратора в этом чате)")
		
		# /upload_message
		# Upload message
		elif command == "upload_message":
			self.addCommand(self.chat_id, command)
			sendMessage(self.chat_id, "Введите текст сообщения")

		# /upload_photos
		# Upload photos
		elif command == "upload_photos":
			self.addCommand(self.chat_id, command)
			sendMessage(self.chat_id, "Вставьте изображение (не более 10 за раз для корректного добавления)")

		# /view_chats
		# View chats
		elif command == "view_chats":
			if not self.outChats(self.getChats()):
				sendMessage(self.chat_id, "Чаты отсутствуют")

		# /view_messages
		# View message
		elif command == "view_messages":
			if not self.outMessages(self.getMessages()):
				sendMessage(self.chat_id, "Сообщения отсутствуют")

		# /view_photos
		# View photos
		elif command == "view_photos":
			if not self.outPhotos(self.getPhotos(), self.chat_id):
				sendMessage(self.chat_id, "Изображения отсутствуют")

		# /clear_chats
		# Clear chats
		elif command == "clear_chats":
			self.clearChats()
			sendMessage(self.chat_id, "Список чатов очищен")

		# /clear_messages
		# Clear messages
		elif command == "clear_messages":
			self.clearMessages()
			sendMessage(self.chat_id, "Список сообщений очищен")

		# /clear_photos
		# Clear photos
		elif command == "clear_photos":
			self.clearPhotos()
			sendMessage(self.chat_id, "Список изображений очищен")

	# Get chats
	def getChats(self):
		result = self.storage.getList(self.chat_id, "chats")
		return result

	# Get messages
	def getMessages(self):
		result = self.storage.getList(self.chat_id, "messages")
		return result

	# Get photos
	def getPhotos(self):
		result = self.storage.getList(self.chat_id, "photos")
		return result

	# Clear chats
	def clearChats(self):
		self.storage.clearList(self.chat_id, "chats")

	# Clear messages
	def clearMessages(self):
		self.storage.clearList(self.chat_id, "messages")

	# Clear photos
	def clearPhotos(self):
		self.storage.clearList(self.chat_id, "photos")

	# Add chat
	def addChat(self, chat):
		self.storage.addChat(self.chat_id, chat)

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

	# Out chats
	def outChats(self, array):
		if not len(array): return False

		count = 0
		for chat in array:
			sendMessage(self.chat_id, f"{count}. {chat['chat_id']}")
			count += 1

		sendMessage(self.chat_id, f"Всего чатов: {count}")

		return True

	# Out messages
	def outMessages(self, array):
		if not len(array): return False

		count = 0
		for message in array:
			sendMessage(self.chat_id, f"{count}. {message['text']}")
			count += 1

		sendMessage(self.chat_id, f"Всего сообщений: {count}")

		return True

	# Out photos
	def outPhotos(self, array, chat_id):
		if not len(array): return False

		count = 0
		for photos in array:
			sendMediaGroup(chat_id, json.dumps(photos))
			count += len(photos)

		if chat_id == self.chat_id:
			sendMessage(chat_id, f"Всего изображений: {count}")

		return True