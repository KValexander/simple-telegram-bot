# Libraies
import os.path
import json

# Class Storage
class Storage:
	# Constructor
	def __init__(self):
		self.directory = "storage"
		self.template = {
			"chats": [],
			"messages": [],
			"photos": []
		}

	# Create storage
	def createStorage(self, chat_id):
		file = open(f"{self.directory}/{chat_id}.json", "w+")
		file.write(json.dumps(self.template))
		file.close()

	# Check storage
	def checkStorage(self, chat_id):
		filename = f"{self.directory}/{chat_id}.json"
		if not os.path.exists(filename):
			self.createStorage(chat_id)
		return filename

	# Update storage
	def updateStorage(self, chat_id, storage):
		filename = self.checkStorage(chat_id)
		file = open(filename, "w+")
		file.write(json.dumps(storage))
		file.close()

	# Get object
	def getStorage(self, chat_id):
		storage, filename = {}, self.checkStorage(chat_id)
		file = open(filename, "r")
		storage = json.loads(file.readline())
		return storage

	# Get list
	def getList(self, chat_id, key):
		storage = self.getStorage(chat_id)
		return storage[key]

	# Clear list
	def clearList(self, chat_id, key):
		storage = self.getStorage(chat_id)
		storage[key].clear()
		self.updateStorage(chat_id, storage)

	# Add chat
	def addChat(self, chat_id, chat):
		storage = self.getStorage(chat_id)
		storage["chats"].append({"chat_id": chat})
		self.updateStorage(chat_id, storage)

	# Add message
	def addMessage(self, chat_id, text):
		storage = self.getStorage(chat_id)
		storage["messages"].append({"text": text})
		self.updateStorage(chat_id, storage)

	# Add photo
	def addPhoto(self, chat_id, file_id):
		storage = self.getStorage(chat_id)

		if not len(storage["photos"]):
			storage["photos"].append([])

		# Adding many images
		if type(file_id) == list:
			for fid in file_id:
				storage["photos"] = self.processPhoto(fid, storage["photos"])
		
		# Adding single image
		else: storage["photos"] = self.processPhoto(file_id, storage["photos"])

		# Update storage
		self.updateStorage(chat_id, storage)

	# Process photo
	def processPhoto(self, file_id, array):
		index = len(array) - 1

		if len(array[index]) >= 10:
			array.append([])
			index += 1

		array[index].append({
			"type": "photo",
			"media": file_id
		})

		return array
