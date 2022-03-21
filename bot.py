import requests
import time
import sys

api = {
    "url": "",
    "api":  "https://api.telegram.org/bot",
    "token": "",
    "user_id": 0,
    "chat_id": 0,
    "update_id": 0,
    "update_obj": {},
    "current_command": "none",
}
api["url"] = api["api"] + api["token"]

commands = {
    "getUpdates": "/getUpdates",
    "sendMessage": "/sendMessage?",
}

def getUpdates():
    get = api["url"] + commands["getUpdates"]
    response = requests.get(get).json()
    api["user_id"] = response["result"][-1]["message"]["from"]["id"]
    api["chat_id"] = response["result"][-1]["message"]["chat"]["id"]
    return response

def getCommand():
    response = getUpdates()

    api["update_obj"] = response["result"][-1]

    if "photo" in api["update_obj"]["message"]:
        if api["current_command"] == "upload": 
            pass
        return False

    if api["update_id"] == 0:
        api["update_id"] = api["update_obj"]["update_id"]
        return False

    if api["update_obj"]["update_id"] != api["update_id"]:
        api["update_id"] = api["update_obj"]["update_id"]
        return api["update_obj"]["message"]["text"]

    return False

def sendMessage(chat_id, text):
    message = f"chat_id={chat_id}&text={text}";
    get = api["url"] + commands["sendMessage"] + message
    requests.get(get)

while True:
    command = getCommand()
    if command:
        print(command)
        if command == "/start":
            sendMessage(api["chat_id"], "Добро пожаловать. Выберите интересующее вас действие, введя в поле ввода \"/\"")
    time.sleep(1)
