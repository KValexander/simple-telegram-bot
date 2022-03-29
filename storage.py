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
	def clearList(self, chat_id, key, n=0):
		storage = self.getStorage(chat_id)
		count = len(storage[key]) if key != "photos" else self.countPhotos(storage[key])
		if not n or n >= count: storage[key].clear()
		else:
			if key == "photos": storage[key] = self.delPhotos(storage[key], count)
			else: del storage[key][:n]
		self.updateStorage(chat_id, storage)

	# Count photos
	def countPhotos(self, array):
		count = 0
		for photo in array:
			count += len(photo)
		return count

	# Delete photos
	def delPhotos(self, array, count):
		# Why doesn't it work correctly?
		for i in range(count):
			del array[0][0]
			if not len(array[0]):
				del array[0]
		return array

	# Add chat
	def addChat(self, chat_id, result):
		storage = self.getStorage(chat_id)
		storage["chats"].append(result)
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
