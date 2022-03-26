# Libraies
import os
import json

# Class Storage
class Storage:
	# Constructor
	def __init__(self):
		self.directory = "storage"

	# Create storage
	def createStorage(self, chat_id):
		storage = open(f"{self.directory}/{chat_id}.json", "w+")
		storage.write(json.dumps({"chats": [], "photos": []}))
		storage.close()

	# Check storage
	def checkStorage(self, chat_id):
		filename = f"{self.directory}/{chat_id}.json"
		if not os.path.exists(filename):
			self.createStorage(chat_id)
		return filename

	# Get object
	def getObject(self, chat_id):
		obj, filename = {}, self.checkStorage(chat_id)

		storage = open(filename, "r")
		obj = json.loads(storage.readline())

		return obj

	# Get photos
	def getPhotos(self, chat_id):
		obj = self.getObject(chat_id)

		return obj["photos"]

