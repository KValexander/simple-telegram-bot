# Files
from methods import *

# Class commands
class Commands:
	# Constructor
	def __init__(self, app):
		self.app = app
		self.functions = {"processing": {}, "command": {}}
		for command in commands:
			self.functions["processing"][commands[command]] = "processing_"+commands[command]
			self.functions["command"][commands[command]] = "command_"+commands[command]

	# Processing distribution
	# ==================================================
	def processingDistribution(self, command, response):
		function = self.functions["processing"][command]
		eval(f"self.{function}({response})")

	# Processing Upload chat
	def processing_upload_chat(self, response):
		update_dict = response[-1]

		# Check dict
		if "text" in update_dict["message"]:
			# Check chat
			chat = getChat(update_dict["message"]["text"])

			# Upload chat
			if "error_code" not in chat:
				self.app.addChat(chat["result"])

				# Success message
				sendMessage(self.app.chat_id, "Чат добавлено.\nДобавленные чаты можно посмотреть с помощью команды \"/view_chats\"")
			
			# Error message
			else: sendMessage(self.app.chat_id, "Чат не найден")

		# Error message
		else: sendMessage(self.app.chat_id, "Неверный формат")

	# Processing Upload message
	def processing_upload_message(self, response):
		update_dict = response[-1]
		
		# Check dick
		if "text" in update_dict["message"]:
			# Upload message
			self.app.addMessage(update_dict["message"]["text"])

			# Success message
			sendMessage(self.app.chat_id, "Сообщение добавлено.\nДобавленные сообщения можно посмотреть с помощью команды \"/view_messages\"")

		# Error message
		else: sendMessage(self.app.chat_id, "Неверный формат")

	# Processing Upload photos
	def processing_upload_photos(self, response):
		update_dict = response[-1]
			
		# Check dict
		if "photo" in update_dict["message"]:

			text = "Изображение добавлено"
			
			# Upload many photos
			if "media_group_id" in update_dict["message"]:
				
				# Selecting the desired group
				photos = [x for x in [y for y in response if "media_group_id" in y["message"]] if x["message"]["media_group_id"] == update_dict["message"]["media_group_id"]]
				# Upload photos
				self.app.addPhoto(photos)
				
				text = "Изображения добавлены"

			# Upload single photo
			else: self.app.addPhoto(update_dict["message"]["photo"][0]["file_id"])

			# Success message
			sendMessage(self.app.chat_id, f"{text}.\nДобавленные изображения можно посмотреть с помощью команды \"/view_photos\"")

		# Error message
		else: sendMessage(self.app.chat_id, "Неверный формат")

	# Processing Post time message
	def processing_post_time_message(self, response):
		update_dict = response[-1]
		self.prc_start_timers(update_dict, "message")

	# Processing Post time photo
	def processing_post_time_photo(self, response):
		update_dict = response[-1]
		self.prc_start_timers(update_dict, "photo")

	# Processing start timers
	def prc_start_timers(self, update_dict, entity):
		if "text" in update_dict["message"]:
			time = update_dict["message"]["text"]
			
			if time.isdigit():
				time = int(time)
				
				if time > 3600 or time < 1:
					sendMessage(self.app.chat_id, "Только целые число от 1 до 3600")
					return

				sendMessage(self.app.chat_id, f"Время публикаций через секунд: {time}")
				
				if entity == "photo":
					self.app.startTimerPhoto(self.app.getList("chats"), time)
				else:
					self.app.startTimerMessage(self.app.getList("chats"), time)
			
			else: sendMessage(self.app.chat_id, "Неверный формат")
		else: sendMessage(self.app.chat_id, "Неверный формат")

	# Command distribution
	# ==================================================
	def commandDistribution(self, command):
		print(self.app.chat_id, command)
		function = self.functions["command"][command]
		eval(f"self.{function}()")

	# /start
	# Command Start
	def command_start(self):
		sendMessage(self.app.chat_id, "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")

	# /upload_chat
	# Command Upload chat
	def command_upload_chat(self):
		self.app.addCommand("upload_chat")
		sendMessage(self.app.chat_id, "Введите название чата в формате @name или id (бот должен находится на должности администратора в этом чате)")

	# /upload_message
	# Command Upload message
	def command_upload_message(self):
		self.app.addCommand("upload_message")
		sendMessage(self.app.chat_id, "Введите текст сообщения")

	# /upload_photos
	# Command Upload photos
	def command_upload_photos(self):
		self.app.addCommand("upload_photos")
		sendMessage(self.app.chat_id, "Вставьте изображение (не более 10 за раз для корректного добавления)")

	# /view_chats
	# Command View chats
	def command_view_chats(self):
		if not self.app.outMessages(self.app.getList("chats")):
			sendMessage(self.app.chat_id, "Чаты отсутствуют")

	# /view_messages
	# Command View message
	def command_view_messages(self):
		if not self.app.outMessages(self.app.getList("messages")):
			sendMessage(self.app.chat_id, "Сообщения отсутствуют")

	# /view_photos
	# Command View photos
	def command_view_photos(self):
		if not self.app.outPhotos(self.app.chat_id, self.app.getList("photos")):
			sendMessage(self.app.chat_id, "Изображения отсутствуют")

	# /clear_chats
	# Command Clear chats
	def command_clear_chats(self):
		self.app.clearList("chats")
		sendMessage(self.app.chat_id, "Список чатов очищен")

	# /clear_messages
	# Command Clear messages
	def command_clear_messages(self):
		self.app.clearList("messages")
		sendMessage(self.app.chat_id, "Список сообщений очищен")

	# /clear_photos
	# Command Clear photos
	def command_clear_photos(self):
		self.app.clearList("photos")
		sendMessage(self.app.chat_id, "Список изображений очищен")

	# /post_messages
	# Command Post messages
	def command_post_messages(self):
		self.app.postMessages(self.app.getList("chats"), self.app.getList("messages"))

	# /post_photos
	# Command Post photos
	def command_post_photos(self):
		self.app.postPhotos(self.app.getList("chats"), self.app.getList("photos"))

	# /post_time_message
	# Command Post time message
	def command_post_time_message(self):
		self.app.addCommand("post_time_message")
		sendMessage(self.app.chat_id, "Введите разницу времени публикации в секундах (только целые числа от 1 до 3600)")

	# /post_time_photo
	# Command Post time photo
	def command_post_time_photo(self):
		self.app.addCommand("post_time_photo")
		sendMessage(self.app.chat_id, "Введите разницу времени публикации в секундах (только целые числа от 1 до 3600)")

	# /post_stop
	# Command Post stop
	def command_post_stop(self):
		self.app.stopTimer()
		sendMessage(self.app.chat_id, "Публикация остановлена")
