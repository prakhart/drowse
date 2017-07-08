import datetime
import time

import pytz


def DATE_TIME():
    return datetime.datetime.now(pytz.timezone('Asia/Calcutta'))

def NEXT_DATE_TIME():
    return DATE_TIME() + datetime.timedelta(days=1)


def FORMATTED_TIME():
    return datetime.datetime.strptime(str(DATE_TIME()).split('.')[0], '%Y-%m-%d %H:%M:%S')

def FORMATTED_TIME_PLUS():
    FORMATTED_TIME_PLUS = datetime.datetime.strptime(str(FORMATTED_TIME()), '%Y-%m-%d %H:%M:%S')
    return  FORMATTED_TIME_PLUS + datetime.timedelta(0, 330 * 60)

def TIME():    
    return FORMATTED_TIME().time()

def DATE():
    return FORMATTED_TIME().date()

def getTime(dateTime):
#    return dateTime
    return datetime.datetime.strftime(datetime.datetime.strptime(str(dateTime), '%Y-%m-%d %H:%M:%S'),"%I:%M %p")


def getDateTime(dateTime):
#    return dateTime
    try:
        return datetime.datetime.strftime(datetime.datetime.strptime(str(dateTime), '%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""
### ---------------------reduce 7 minutes from time--------------
def LATER():
    return FORMATTED_TIME() - datetime.timedelta(0, 7 * 60)

def LATERTIME():
    return LATER().time()

def LATER_15():
    return FORMATTED_TIME() - datetime.timedelta(0, 15 * 60)
def LATER_15_TIME():
    LATER_15().time()
#### -------------------- add 30 minutes
def AFTER():
    return FORMATTED_TIME() + datetime.timedelta(0, 30 * 60)

def AFTERTIME():
    return AFTER().time()


#####-------After add 120 minutes
def AFTER_TWO():
    return FORMATTED_TIME() + datetime.timedelta(0, 120 * 60)

def AFTER_TWO_TIME():
    return AFTER_TWO().time()

def CURRENT_TIME_PLUS_PARAMS(minutes):
    FORMATTED_TIME_PLUS = datetime.datetime.strptime(str(FORMATTED_TIME()), '%Y-%m-%d %H:%M:%S')
    return  FORMATTED_TIME_PLUS + datetime.timedelta(0, minutes * 60)

def CURRENT_TIME_MINUS_PARAMS(minutes):
    FORMATTED_TIME_PLUS = datetime.datetime.strptime(str(FORMATTED_TIME()), '%Y-%m-%d %H:%M:%S')
    return  FORMATTED_TIME_PLUS - datetime.timedelta(0, minutes * 60)


