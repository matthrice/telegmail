import os
import pytz
import asyncio
import mdmail

from telethon import TelegramClient
from telethon import functions, types
from datetime import datetime, date, timedelta

# telegram app configuration
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
notes_chanel = os.getenv("CHANNEL_URL")
client = TelegramClient(os.getenv("APP_NAME"), api_id, api_hash)

# max number of messages returned
MAX_RESULTS = 100

# time constants
today = datetime.combine(date.today(), datetime.max.time())
yesterday = today - timedelta(days=1)
last_week = today - timedelta(days=7)
last_month = today - timedelta(days=30)

# time adjustments
utc = pytz.UTC
telegram_offset = timedelta(hours=7)

# email setup
from_email = os.getenv("EMAIL_FROM_USER")
to_email = os.getenv("EMAIL_TO_USER")
email_password = os.getenv("EMAIL_PASSWORD")
email_host = os.getenv("EMAIL_HOST")
email_port = int(os.getenv("EMAIL_PORT"))

smtp = {
    "host": email_host,
    "port": email_port,
    "tls": True,
    "ssl": False,
    "user": from_email,
    "password": email_password,
}


async def messages_by_day(channel, day):
    """Get all messages from a channel given a day."""

    # make day timezone aware and offset
    begin_search_day = utc.localize(day - timedelta(days=1) + telegram_offset)
    end_search_day = utc.localize(day + telegram_offset)

    result = []
    async for msg in client.iter_messages(channel, offset_date=begin_search_day, reverse=True):
        if msg.date > end_search_day:
            return result
        result.append(msg)


def format_msg_group(header, date, msgs):
    """Format a message group into markdown."""

    # format date
    date_str = date.strftime("%B %d, %Y (%A)")

    # format messages and join
    msg_str = "\n".join([msg.text.replace("#", "\#") + "\n" for msg in msgs])

    return f"""
### {header}

#### {date_str}

{msg_str}
"""


def format_email(header, snippets):
    """Format entire email from markdown snippets"""

    snippet_str = "\n".join(snippets)

    return f"""
# {header}

{snippet_str}
"""


async def main():
    """Get messages from yesterday, last week, and last month, and send an email."""

    # fill cache ?
    dialogs = await client.get_dialogs()
    # get "Notes" channel
    notes_channel = await client.get_entity(notes_chanel)

    # get messages
    msgs_yesterday, msgs_last_week, msgs_last_month = await asyncio.gather(
        messages_by_day(notes_channel, yesterday),
        messages_by_day(notes_channel, last_week),
        messages_by_day(notes_channel, last_month)
    )

    # format individual markdown snippets
    yesterday_snippet = format_msg_group(
        "Yesterday", yesterday, msgs_yesterday)
    last_week_snippet = format_msg_group(
        "Last Week", last_week, msgs_last_week)
    last_month_snippet = format_msg_group(
        "Last Month", last_month, msgs_last_month)

    # format full markdown
    content = format_email("Telegram Messages", [
                           yesterday_snippet, last_week_snippet, last_month_snippet])

    # send email
    print("Sending email...")
    mdmail.send(content, subject="Telegram Messages",
                from_email=from_email, to_email=to_email, smtp=smtp)


with client:
    client.loop.run_until_complete(main())
