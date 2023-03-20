from datetime import datetime, timedelta
import pytz
import calendar

tz_IL = pytz.timezone('Israel')


def find_day(time):
    day = datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d').weekday()
    return calendar.day_name[day]


def get_current_time():
    now = datetime.now(tz_IL)
    return now
