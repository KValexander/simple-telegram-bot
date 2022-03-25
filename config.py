# Api
api = {
	"api": "https://api.telegram.org/bot",
	"token": "5192104143:AAEFIYiHa9cjIAN4pU9zSePdk34qKYp6lF0",
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