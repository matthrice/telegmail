from telethon import TelegramClient
from telethon import functions, types
from datetime import datetime, date, timedelta
import pytz
import asyncio


api_id = 1178334
api_hash = 'ced689e6f267cb44dee767bb24e2cb6d'
client = TelegramClient('telegmail', api_id, api_hash)

MAX_RESULTS = 100

utc = pytz.UTC

today = datetime.combine(date.today(), datetime.max.time())
yesterday = today - timedelta(days=1)
last_week = today - timedelta(days=6)
last_month = today - timedelta(days=29)

telegram_offset = timedelta(hours=7)


async def messages_by_day(channel, day):
    # make day timezone aware and offset
    begin_search_day = utc.localize(day - timedelta(days=1) + telegram_offset)
    end_search_day = utc.localize(day + telegram_offset)

    print("BEGIN SEARCH DAY" + str(begin_search_day))
    print("END SEARCH DAY" + str(end_search_day))

    result = []
    async for msg in client.iter_messages(channel, offset_date=begin_search_day, reverse=True):
        if msg.date > end_search_day:
            return result
        print(msg.date)
        print(msg.id)
        print(msg.text)
        result.append(msg)


async def main():

    dialogs = await client.get_dialogs()

    notes_channel = await client.get_entity('https://t.me/joinchat/AAAAAEa0c94VxbuxWgS2xw')

    msgs_yesterday = await messages_by_day(notes_channel, yesterday - timedelta(days=4))

    # msgs_yesterday, msgs_last_week, msgs_last_month = await asyncio.gather(
    #     messages_by_day(notes_channel, yesterday),
    #     messages_by_day(notes_channel, last_week),
    #     messages_by_day(notes_channel, last_month)
    # )

with client:
    client.loop.run_until_complete(main())
