
from telethon import TelegramClient

api_id = 263724                  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "3a8ae22a8e6981038a370c7149d51fc2"              # API Hash (оттуда же)
phone_number = "+79523870268"    # Номер телефона аккаунта, с которого будет выполняться код


# Необходимо предварительно авторизоваться, чтобы был создан файл second_account,
# содержащий данные об аутентификации клиента.
client = TelegramClient('session_name', api_id, api_hash)
client.connect()

# print(client.get_me().stringify())

username = 'shaitan1985' # канал @telegram


for message in client.get_messages(username, limit=10):
    print(message.id)
    # client.download_media(message)
    break



# import hashlib
# file = '001.jpg'
# with open(file, 'rb') as f:
#     m = hashlib.md5()
#     while True:
#         data = f.read(8192)  # размер блока чтения 8 мб
#         if not data:
#             break
#         m.update(data)
#     print(m.hexdigest())
# file = '002.jpg'
# with open(file, 'rb') as f:
#     m = hashlib.md5()
#     while True:
#         data = f.read(8192)  # размер блока чтения 8 мб
#         if not data:
#             break
#         m.update(data)
#     print(m.hexdigest())