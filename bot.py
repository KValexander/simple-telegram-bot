# Libraries
import requests
import json
import time
import sys

# Api
api = {
    "url": "",
    "api":  "https://api.telegram.org/bot",
    "token": "",
    "channel": "",
    "user_id": 0,
    "chat_id": 0,
    "update_id": 0,
    "update_limit": 30,
    "current_command": None,
    "photos": [],
}
# Url
api["url"] = api["api"] + api["token"]

# Commands
commands = {
    "getUpdates": "/getUpdates?",
    "sendMessage": "/sendMessage?",
    "sendPhoto": "/sendPhoto?",
    "sendMediaGroup": "/sendMediaGroup?",
    "getFile": "/getFile?",
}

# Get updates
def getUpdates():
    # Update limit
    offset = f"offset={api['update_id'] - api['update_limit']}"
    get = api["url"] + commands["getUpdates"] + offset

    # get = api["url"] + commands["getUpdates"]
    response = requests.get(get).json()
    api["user_id"] = response["result"][-1]["message"]["from"]["id"]
    api["chat_id"] = response["result"][-1]["message"]["chat"]["id"]
    return response

# Get command
def getCommand():
    # Get data
    response = getUpdates()
    response = [x for x in response["result"] if "message" in x]

    # Getting the last object
    update_obj = response[-1]

    # Command processing
    if api["current_command"]:
        commandProcessing(update_obj, response)

    # Check update_id
    if api["update_id"] == 0:
        api["update_id"] = update_obj["update_id"]

    # Command return
    if update_obj["update_id"] != api["update_id"]:
        if "text" in update_obj["message"]:
            api["update_id"] = update_obj["update_id"]
            return update_obj["message"]["text"]

    return False

# Command processing
def commandProcessing(update_obj, response):
    # Upload files
    if api["current_command"] == "upload":
        # Upload image
        if "photo" in update_obj["message"]:
            api["current_command"] = None
            text = "Изображение добавлено"
            # Upload many images
            if "media_group_id" in update_obj["message"]:
                photos = [x for x in response if "media_group_id" in x["message"]]
                photos = [x for x in photos if x["message"]["media_group_id"] == update_obj["message"]["media_group_id"]]
                for photo in photos:
                    addPhoto(photo["message"]["photo"][0]["file_id"])
                text = "Изображения добавлены"
            # Upload single image
            else: addPhoto(update_obj["message"]["photo"][0]["file_id"])
            
            # Success message
            sendMessage(api["chat_id"], f"{text}.\nДобавленные изображения можно посмотреть с помощью команды \"/view\"")

# Add photo
def addPhoto(file_id):
    index = len(api["photos"]) - 1

    if index < 0:
        api["photos"].append([])
        index = 0

    if len(api["photos"][index]) >= 10:
        api["photos"].append([])
        index += 1

    api["photos"][index].append({
        "type": "photo",
        "media": file_id
    })

# Out photos
def outPhotos(array):
    if len(array) == 0: return False

    count = 0
    for photos in api["photos"]:
        sendMediaGroup(api["chat_id"], json.dumps(photos.copy()))
        count += len(photos)

    sendMessage(api["chat_id"], f"Всего изображений: {count}")

    return True

# Send message
def sendMessage(chat_id, text):
    message = f"chat_id={chat_id}&text={text}";
    get = api["url"] + commands["sendMessage"] + message
    return requests.get(get)

# Send photo
def sendPhoto(chat_id, file_id):
    message = f"chat_id={chat_id}&photo={file_id}"
    get = api["url"] + commands["sendPhoto"] + message
    return requests.get(get)

# Send media group
def sendMediaGroup(chat_id, media):
    message = f"chat_id={chat_id}&media={media}"
    get = api["url"] + commands["sendMediaGroup"] + message
    return requests.get(get)

# Get file
def getFile(file_id):
    message = f"file_id={file_id}"
    get = api["url"] + commands["getFile"] + message
    return requests.get(get)

# Loop
while True:
    command = getCommand()

    if command:

        print(command)

        # Start
        if command == "/start":
            sendMessage(api["chat_id"], "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")
        
        # Upload image
        elif command == "/upload":
            api["current_command"] = "upload"
            sendMessage(api["chat_id"], "Вставьте изображение (не более 10 за раз для корректного добавления)")

        # View images
        elif command == "/view":
            if not outPhotos(api["photos"]):
                sendMessage(api["chat_id"], f"Добавленные изображения отсутствуют")

        # Delete images
        elif command == "/clear":
            api["photos"].clear()
            sendMessage(api["chat_id"], f"Список добавленных изображений очищен")

    time.sleep(1)