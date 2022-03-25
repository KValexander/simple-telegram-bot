# Libraries
import requests

# Files
from config import *

# Get updates
def getUpdates(offset=""):
	get = api["url"] + tg_commands["getUpdates"] + offset
	response = requests.get(get).json()
	return response

# Send message
def sendMessage(chat_id, text):
	message = f"chat_id={chat_id}&text={text}";
	get = api["url"] + tg_commands["sendMessage"] + message
	return requests.get(get)

# Send photo
def sendPhoto(chat_id, file_id):
	message = f"chat_id={chat_id}&photo={file_id}"
	get = api["url"] + tg_commands["sendPhoto"] + message
	return requests.get(get)

# Send media group
def sendMediaGroup(chat_id, media):
	message = f"chat_id={chat_id}&media={media}"
	get = api["url"] + tg_commands["sendMediaGroup"] + message
	return requests.get(get)

# Get file
def getFile(file_id):
	message = f"file_id={file_id}"
	get = api["url"] + tg_commands["getFile"] + message
	return requests.get(get)