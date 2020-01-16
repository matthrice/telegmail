from telethon import TelegramClient

api_id = 1178334
api_hash = 'ced689e6f267cb44dee767bb24e2cb6d'
client = TelegramClient('telegmail', api_id, api_hash)
notes_id = '-1001186231262'


async def main():
    me = await client.get_me()

    dialogs = await client.get_dialogs()

    notes_channel = await client.get_entity('https://t.me/joinchat/AAAAAEa0c94VxbuxWgS2xw')

    count = 0
    async for message in client.iter_messages(notes_channel):
        print(message.id, message.text)
        count += 1
        if count > 10:
            break

with client:
    client.loop.run_until_complete(main())
