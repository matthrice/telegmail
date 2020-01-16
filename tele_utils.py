from datetime import datetime, date, timedelta
import pytz

utc = pytz.UTC

today = datetime.combine(date.today(), datetime.max.time())
yesterday = today - timedelta(days=1)
last_week = today - timedelta(days=6)
last_month = today - timedelta(days=29)

telegram_offset = timedelta(hours=7)


def messages_by_day(day):
    # make day timezone aware and offset
    adjusted_day = utc.localize(day)

    print("BEGIN SEARCH DAY" + str(adjusted_day -
                                   timedelta(days=1) + telegram_offset))
    print("END SEARCH DAY" + str(adjusted_day + telegram_offset))


messages_by_day(yesterday)
