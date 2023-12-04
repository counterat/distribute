from telethon import TelegramClient
from config import api_id, api_hash
client = TelegramClient('session_name', api_id, api_hash)
client =  client.start()
dialogs =  client.get_dialogs()
print(dialogs)
