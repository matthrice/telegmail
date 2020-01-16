from telethon import TelegramClient
from telethon import functions, types
from datetime import datetime, date, timedelta
import pytz
import asyncio

# telegram app configuration
api_id = 1178334
api_hash = 'ced689e6f267cb44dee767bb24e2cb6d'
notes_chanel = 'https://t.me/joinchat/AAAAAEa0c94VxbuxWgS2xw'
client = TelegramClient('telegmail', api_id, api_hash)

# max number of messages returned
MAX_RESULTS = 100

# time constants
today = datetime.combine(date.today(), datetime.max.time())
yesterday = today - timedelta(days=1)
last_week = today - timedelta(days=6)
last_month = today - timedelta(days=29)

# time adjustments
utc = pytz.UTC
telegram_offset = timedelta(hours=7)


async def messages_by_day(channel, day):
    # Get all messages from a channel given a day

    # make day timezone aware and offset
    begin_search_day = utc.localize(day - timedelta(days=1) + telegram_offset)
    end_search_day = utc.localize(day + telegram_offset)

    print("BEGIN SEARCH DAY" + str(begin_search_day))
    print("END SEARCH DAY" + str(end_search_day))

    result = []
    async for msg in client.iter_messages(channel, offset_date=begin_search_day, reverse=True):
        if msg.date > end_search_day:
            return result
        result.append(msg)


async def main():
    # fill cache ?
    dialogs = await client.get_dialogs()
    # get "Notes" channel
    notes_channel = await client.get_entity(notes_chanel)

    msgs_yesterday = await messages_by_day(notes_channel, yesterday - timedelta(days=2))
    print([x.text for x in msgs_yesterday])
    # msgs_yesterday, msgs_last_week, msgs_last_month = await asyncio.gather(
    #     messages_by_day(notes_channel, yesterday),
    #     messages_by_day(notes_channel, last_week),
    #     messages_by_day(notes_channel, last_month)
    # )

with client:
    client.loop.run_until_complete(main())
