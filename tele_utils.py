from datetime import datetime, date, timedelta
import pytz
import smtplib
import os
from email.message import EmailMessage

utc = pytz.UTC

today = datetime.combine(date.today(), datetime.max.time())
yesterday = today - timedelta(days=1)
last_week = today - timedelta(days=6)
last_month = today - timedelta(days=29)

telegram_offset = timedelta(hours=7)


def messages_by_day(day):
    # make day timezone aware and offset
    adjusted_day = utc.localize(day)

    return f"""
{"BEGIN SEARCH DAY" + str(adjusted_day -
                                   timedelta(days=1) + telegram_offset)}
{"END SEARCH DAY" + str(adjusted_day + telegram_offset)}

{adjusted_day.strftime("%B %d, %Y (%A)")}
"""


def send_content(content):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

        message = 'Subject: Telegram Messages\n\n{}'.format("content")
        server.sendmail(os.getenv("EMAIL_USER"),
                        "mattrice.tx@gmail.com", message)
        server.quit()
        print("Success! email sent")
    except:
        print("Email failed to send")


content = messages_by_day(yesterday)
send_content(content)
