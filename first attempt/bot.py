# Libraries
import requests
import json
import time
import threading

# Api
api = {
    "url": "",
    "api":  "https://api.telegram.org/bot",
    "token": "5192104143:AAEWVTkhk1cnZWBUP013Qn7sSa5OExb6H1o",
    "publication_chat_id": -1001739776156,
    "user_id": 0,
    "chat_id": 0,
    "update_id": 0,
    "update_limit": 30,
    "current_command": None,
    "timer": None,
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
    return response

# Get command
def getCommand():
    # Get data
    response = getUpdates()
    response = [x for x in response["result"] if "message" in x]

    # Getting the last object
    update_obj = response[-1]
    api["user_id"] = update_obj["message"]["from"]["id"]
    api["chat_id"] = update_obj["message"]["chat"]["id"]

    # Check update_id
    if api["update_id"] == 0:
        api["update_id"] = update_obj["update_id"]

    # Getting only the next message
    if update_obj["update_id"] != api["update_id"]:

        # Command processing
        if api["current_command"] and api["chat_id"] == update_obj[":
            commandProcessing(update_obj, response)

        # Command return
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

    # Publish images after a certain time
    elif api["current_command"] == "publication":
        if "text" in update_obj["message"]:
            api["current_command"] = None
            time = update_obj["message"]["text"]
            if time.isdigit():
                time = int(time)
                sendMessage(api["chat_id"], f"Добавленные изображения будут публиковаться раз в {time} секунд")
                api["timer"] = threading.Timer(time, publicationTime, (api["publication_chat_id"], api["photos"], time,))
                api["timer"].start()
            else: sendMessage(api["chat_id"], "Неверный формат")

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
def outPhotos(chat_id, array):
    if len(array) == 0: return False

    count = 0
    for photos in api["photos"]:
        sendMediaGroup(chat_id, json.dumps(photos.copy()))
        count += len(photos)

    if api["chat_id"] == chat_id:
        sendMessage(chat_id, f"Всего изображений: {count}")

    return True

# Publication by time
def publicationTime(chat_id, array, time):
    if len(array) == 0:
        sendMessage(api["chat_id"], "Изображения отсутствуют, публикация остановлена")
        return

    photo = array[0].pop(0)
    sendPhoto(chat_id, photo["media"])

    if len(array[0]) == 0:
        array.pop(0)

    api["timer"] = threading.Timer(time, publicationTime, (chat_id, array, time,))
    api["timer"].start()

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
        
        # Upload images
        elif command == "/upload":
            api["current_command"] = "upload"
            sendMessage(api["chat_id"], "Вставьте изображение (не более 10 за раз для корректного добавления)")

        # View images
        elif command == "/view":
            if not outPhotos(api["chat_id"], api["photos"]):
                sendMessage(api["chat_id"], "Добавленные изображения отсутствуют")

        # Delete images
        elif command == "/clear":
            api["photos"].clear()
            sendMessage(api["chat_id"], "Список добавленных изображений очищен")

        # Publish images
        elif command == "/publish":
            outPhotos(api["publication_chat_id"], api["photos"])
            api["photos"].clear()
            sendMessage(api["chat_id"], "Добавленные изображения были опубликованы и удалены из списка")

        # Publish images after a certain time
        elif command == "/publication_time":
            api["current_command"] = "publication"
            sendMessage(api["chat_id"], "Введите через какое количество секунд будут выкладываться изображения (только целые числа)")

        # Stop publishing
        elif command == "/stop_publication":
            if api["timer"] != None:
                api["timer"].cancel()
                sendMessage(api["chat_id"], "Публикация остановлена")
            else: sendMessage(api["chat_id"], "Публикация не запущена")

    time.sleep(1)