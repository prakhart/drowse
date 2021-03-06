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













category_dict = {
    "1":"SPORTS BAR",
    "2":"RESTRO BAR",
    "3":"PUBS N BARS",
    "4":"LOUNGE BAR",
    "5":"NIGHT CLUB",
    "6":"COFFEE SHOPS/CAFE",
    "7":"DISCOTHEQUES / DANCE FLOOR",
    "8":"GALA EVENTS",
    }

cuisines_dict = {
    "1":"CONTINENTAL",
    "2":"MEXICAN",
    "3":"PAN ASIAN",
    "4":"ORIENTAL",
    "5":"FAST FOOD",
    "6":"LEBANESE",
    "7":"INDIAN",
    "8":"ITALIAN",
    "9":"FRENCH",
    "10":"JAPANESE",
    "11":"CHINESE",
    "12":"AMERICAN",

    }

ambience_dict = {
    "1":"CASUAL DINING",
    "2":"FINE DINING",
    "3":"PRIVATE DINING AREA",
    "4":"ROOFTOP DINING",
    "5":"POOLSIDE LOUNGE",
    "6":"LIVE MUSIC PERFORMANCE",
    "7":"LOUD DANCE MUSIC",
    "8":"KARAOKE",
    "9":"DANCE FLOOR",
    }



facilities_dict = {
    "1":"FULLY VEGETARIAN",
    "2":"NON-VEGETARIAN",
    "3":"JAIN FOOD",
    "4":"BUFFET",
    "5":"HOME DELIVERY",
    "6":"FULL BAR FACILITY",
    "7":"WI-FI",
    "8":"SMOKING ZONE",
    "9":"FREE PARKING",
    "10":"PAID PARKING",
    "11":"VALET PARKING",
    "12":"SOCIAL EVENTS / PARTIES",
    }




special_offerings_dict = {
    "1":"MICROBREWERIES",
    "2":"CREATIVE COCKTAILS",
    "3":"SHEESHA BAR",
    "4":"SUNDAY BRUNCH",
    "5":"LATE NIGHT SERVING",
    "6":"UNLIMITED DRINKS N BUFFET",
    "7":"LIP SMACKING SEAFOOD",
    "8":"LADIES NIGHT OUT",
    "9":"LIVE SPORTS STREAMING",
    "9":"Special Parties",
    "10":"Authentic Seafood",
    }



cost_for_two_dict = {
    "1":"0-500",
    "2":"500-1000",
    "3":"1000-2000",
    "4":"2000 and above",
    }


payment_modes_dict = {
    "1":"CASH",
    "2":"CREDIT / DEBIT CARD PAYMENT",
    "3":"ONLINE WALLETS ACCEPTED { PAYTM, MOBIKWIK, FREECHARGE }",
    "4":"POPULAR COUPONS LIKE SODEXO, DINERS INTERNATIONAL"
    }

discount_dict = {
  "1" :"10%",
  "2" :"20%",
  "3" :"30%",
  "4" :"40%",
  "5" :"50%",
}

applicable_on_dict = {
  "1" :"All Alcohols",
  "2" :"All Non Alcohols",
  "3" :"Only Beers",
  "4" :"Only IMFL",
  "5" :"Only Cocktails",
}

valid_for_dict = {
  "1" :"1 person / coupon",
  "2" :"2 person / coupon",
  "3" :"3 person / coupon",
  "4" :"4 person / coupon",
}

valid_on_days_dict ={
    "1" : "Monday", 
    "2" : "Tuesday",
    "3" : "Wednesday",
    "4" : "Thursday",
    "5" : "Friday",
    "6" : "Saturday",
    "7" : "Sunday"

}

terms_conditions = {
    "1"  :"The outlet is strict about timings and validity of offers. Please check your availability at the pub within the timings announced in the happy hour section, else the ticket would stand invalid, unless considered otherwise by the outlet.",
    "2"  :"Prior reservation recommended. This offer is only applicable through drowse tickets.",
    "3"  :"Once ticket is booked for a particular happy hour offer, it cannot be clubbed or exchanged with any other active / inactive offer.",
    "4"  :"The choice of hookah / drinks / food is based on availability and sole discretion of the pub management.",
    "5"  :"Sharing and packing of food not allowed. Not applicable only on platters and pitchers.",
    "6"  :"Offer not valid on all special days such as festivals, social events and public occasions, unless specified.",
    "7"  :"All local / national laws regarding legal drinking age stands valid for all drowse customers.",
    }