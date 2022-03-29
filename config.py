# Api
api = {
	"api": "https://api.telegram.org/bot",
	"token": "",
}
api["url"] = api["api"] + api["token"]

# Commands
commands = {
	"/start": "start",
	# Chats
	"/upload_chat": "upload_chat",
	"/view_chats": "view_chats",
	"/clear_chats": "clear_chats",
	# Messages
	"/upload_message": "upload_message",
	"/view_messages": "view_messages",
	"/clear_messages": "clear_messages",
	# Photos
	"/upload_photos": "upload_photos",
	"/view_photos": "view_photos",
	"/clear_photos": "clear_photos",
	# Post
	"/post_messages": "post_messages",
	"/post_photos": "post_photos",
	"/post_time_message": "post_time_message",
	"/post_time_photos": "post_time_photos",
	"/post_stop": "post_stop"
}