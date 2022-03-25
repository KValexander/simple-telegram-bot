# Api
api = {
	"api": "https://api.telegram.org/bot",
	"token": "",
}
api["url"] = api["api"] + api["token"]

# Commands
commands = {
	"/start": "start",
}

# TG api commands
tg_commands = {
	"getUpdates": "/getUpdates?",
	"sendMessage": "/sendMessage?",
	"sendPhoto": "/sendPhoto?",
	"sendMediaGroup": "/sendMediaGroup?",
	"getFile": "/getFile?",
}