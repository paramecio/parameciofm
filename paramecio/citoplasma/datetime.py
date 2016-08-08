import time
from datetime import date, datetime, tzinfo
import arrow
# from babel.dates import format_date, format_datetime, format_time, get_timezone, UTC
from settings import config
from bottle import hook
from paramecio.citoplasma.sessions import get_session
from os import environ

#t=datetime.utcnow()

#format_date(t, locale='es_ES')

#format_time(t, locale='es_ES')

#  eastern = get_timezone('Europe/Madrid')

# format_time(t, locale='es_ES', tzdata=eastern)
# 20141112030455

# format_datetime(t, "yyyyLLddhhmmss")

# format_datetime(t, "yyyyLLddhhmmss", tzinfo=eastern

#  class datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

# Is saved in format_datetime utc with utcnow if the field is clear.

# format_datetime(t, locale="es_ES", tzinfo=eastern)

# Next convert to 

# Change 

#os.environ['TZ'] = 'America/New_York'

#time.tzset()

#>>> time.timezone
#-3600

#>>> int(time.time())
#1451356872

#>>> time.mktime((2015, 12, 29, 12, 25, 36, 0, 1, 0))
#1451384736.0

# strftime

#time.gmtime()
#time.struct_time(tm_year=2015, tm_mon=12, tm_mday=30, tm_hour=2, tm_min=6, tm_sec=56, tm_wday=2, tm_yday=364, tm_isdst=0)

sql_format_time='YYYYMMDDHHmmss'

format_date_txt="YYYY/MM/DD"

format_time_txt="HH:mm:ss"

timezone='Europe/Madrid'

if hasattr(config, 'format_date'):
    format_date_txt=config.format_date

if hasattr(config, 'format_time'):
    format_time_txt=config.format_time

if hasattr(config, 'timezone'):
    timezone=config.timezone    

#@hook('before_request')

def set_timezone():
    
    environ['TZ']=environ.get('TZ', timezone)
    
    if environ['TZ']!=timezone:
        environ['TZ']=timezone
        time.tzset()

def set_timezone_session():
    
    s=get_session()
    
    timezone_local=timezone
    
    if s!=None:
        if 'timezone' in s:
            timezone_local=s['timezone']
        #timezone_local=s.get('timezone', timezone)
    
    environ['TZ']=environ.get('TZ', timezone_local)
    
    if environ['TZ']!=timezone_local:
        environ['TZ']=timezone_local
        time.tzset()
    
    #request.environ['TIMEZONE'] = request.environ['PATH_INFO'].rstrip('/')

def format_timedata(time):
    
    year=0
    month=0
    day=0
    hour=0
    minute=0
    second=0
    ampm=''
    
    try:
    
        year=int(time[:4])
        
        month=int(time[4:6])
        
        day=int(time[6:8])
        
        hour=int(time[8:10])
        
        minute=int(time[10:12])
        
        second=int(time[12:14])
    
        ampm=int(time[14:16])

    except:
        pass
    
    if ampm=='PM' or ampm=='pm':
        
        if hour>0:
            hour+=12

    return (year, month, day, hour, minute, second)

def checkdatetime(y, m, d, h, mi, s):
    
    try:
        #test=datetime.strptime(str(y)+'-'+str(m)+'-'+str(d)+' '+str(h)+'-'+str(mi)+'-'+str(s), '%Y-%m-%d %H-%M-%S')
        test=arrow.arrow.Arrow(y, m, d, h, mi, s)
        return True
    except:
        return False
    
# Get the localtime
    
def now(utc=False):
    """
    actual=datetime.today()
    
    # Get localtime
    
    final_date=actual.strftime(sql_format_time)
    #Go to gmt
    
    if utc:
    
        final_date=local_to_gmt(final_date)
        
    return final_date
    """
    
    if not utc:
    
        actual=arrow.now().format(sql_format_time)
    else:
        actual=arrow.utcnow().format(sql_format_time)
    
    
# Get actual timestamp

def obtain_timestamp(timeform, local=False):
    
    y, m, d, h, mi, s=format_timedata(timeform)
    
    if checkdatetime(y, m, d, h, mi, s):
        
        #timestamp=int(time.mktime((y, m, d, h, mi, s, 0, 0, -1)))       
        
        if local:
            
            #offset=time.altzone
        
            #return timestamp-offset
            
            t=arrow.arrow.Arrow(y, m, d, h, mi, s).to(environ['TZ'])
            
            timestamp=t.timestamp
            
        else:
            timestamp=arrow.arrow.Arrow(y, m, d, h, mi, s).timestamp
         
        return timestamp
        
        #return mktime($h, $mi, $s, $m, $d, $y);
    else:
        return False

# timestamp is gmt time, convert in normal time

def timestamp_to_datetime(timestamp):
    
    #time_set=substract_utc(timestamp)
        
    #return time.strftime(sql_format_time, time_set)
    
    return arrow.get(timestamp).format(sql_format_time)


def timestamp_to_datetime_local(timestamp):
    
    #time_set=time.localtime(timestamp)
    
    #return time.strftime(sql_format_time, time_set)
    
    t=arrow.get(timestamp)
    
    return t.to(environ['TZ']).format(sql_format_time)


def format_datetime(format_time, timeform, func_utc_return):
    
    timestamp=obtain_timestamp(timeform)
    
    if timestamp:
    
        #offset=time.timezone
        
        #timestamp=func_utc_return(timestamp, offset)
        
        # Return utc
        
        #time_set=func_utc_return(timestamp)
        
        #return time.strftime(format_time, time_set)
        
        t=func_utc_return(timestamp)
        
        return t.format(format_time)
        
    else:
    
        return False
        
# This method parse local time to gmt

def local_to_gmt(timeform):
    
    return format_datetime(sql_format_time, timeform, substract_utc)

# time.localtime is useless, you need sum the time offset to the date

def gmt_to_local(timeform):
    
    return format_datetime(sql_format_time, timeform, sum_utc)

def format_time(timeform):
    
    return format_datetime(format_time_txt, timeform, sum_utc)

def format_date(timeform):
    
    return format_datetime(format_date_txt, timeform, sum_utc)

def format_fulldate(timeform):
    
    return format_datetime(format_date_txt+' '+format_time_txt, timeform, sum_utc)

#Input is utc timestamp, return local arrow object

def sum_utc(timestamp):
    
    #offset=time.altzone

    #return time.localtime(timestamp-offset)
    
    t=arrow.get(timestamp)
    
    return t.to(environ['TZ'])

#Input is local timestamp, return utc arrow object

def substract_utc(timestamp):
    
    #offset=time.altzone

    #return time.localtime(timestamp+offset)
    
    #t=arrow.get(timestamp).to('UTC')
    
    timeform=timestamp_to_datetime(timestamp)
    
    y, m, d, h, mi, s=format_timedata(timeform)
    
    t=arrow.get(datetime(y, m, d, h, mi, s), environ['TZ']).to('UTC')
    
    return t


"""
if hasattr(config, 'timezone'):
    timezone=config.timezone
    
tzutc=get_timezone('UTC')

tz=get_timezone(timezone)

# In utc

def timenow():
    
    t=datetime.utcnow()
    
    return format_datetime(t, "yyyyLLddHHmmss", tzutc)

def timegmt(time, tzc=None):
    
    if tzc==None:
        tzc=tz
    
    year, month, day, hour, minute, second=obtain_fields_time(time)
    
    t=datetime(year, month, day, hour, minute, second)
    
    return format_datetime(t, "yyyyLLddHHmmss", tzutc)

#In utc

def normalize_time(year, month, day, hour, minute, second, tz=None):
    
    try:
    
        t=datetime(year, month, day, hour, minute, second)
        
        return format_datetime(t, "yyyyLLddHHmmss", tzutc)

    except ValueError:
        
        return timenow()

def obtain_fields_time(time):
    
    #year, month, day, hour, minute, second=time
    
    year=int(time[:4])
    
    month=int(time[4:6])
    
    day=int(time[6:8])
    
    hour=int(time[8:10])
    
    minute=int(time[10:12])
    
    second=int(time[12:14])
    
    return year, month, day, hour, minute, second        
    
# In the format of tzinfo

def format_tztime(time, tzc=None):
    
    if tzc==None:
        tzc=tz
    
    year, month, day, hour, minute, second=obtain_fields_time(time)
    
    t=datetime(year, month, day, hour, minute, second)
    
    return format_datetime(t, format_time, tzinfo=tzc)

def format_tzdate(time, tzc=None):
    
    if tzc==None:
        tzc=tz
    
    year, month, day, hour, minute, second=obtain_fields_time(time)
    
    t=datetime(year, month, day, hour, minute, second)
    
    return format_datetime(t, format_date, tzinfo=tzc)

def local_to_utc(date, tzc=None):
    
    if tzc==None:
        tzc=tz
    
    year, month, day, hour, minute, second=obtain_fields_time(date)
    
    t=datetime(year, month, day, hour, minute, second, tzinfo=get_timezone('Europe/Madrid'))
    print(t)
    #timestamp=int(time.mktime((year, month, day, hour, minute, second, 0, 1, 0)))
    
    #timezone_sum=time.timezone
    
    #timestamp-=timezone_sum
    
    print(format_datetime(t, "yyyyLLddHHmmss", tzinfo=tzutc))

    #    return timenow()
def obtain_timezone(timezone):
    
    return get_timezone(timezone)


"""
