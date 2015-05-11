__author__ = 'Alex Gomes'

import datetime, time, calendar

format_desc_human='%Y-%m-%d/n%H:%M:%S'

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def format_from_timestamp(utc_datetime):
    return str(datetime_from_utc_to_local(utc_datetime).strftime(format_desc_human))

def to_timestamp(utc_date):
    #Sun, 10 May 2015 08:41:24 GMT
    #datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    return calendar.timegm(time.strptime(utc_date, '%a, %d %b %Y %H:%M:%S GMT'))