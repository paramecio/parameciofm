from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time, get_timezone, UTC
from settings import config

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

if hasattr(config, 'timezone'):
    timezone=config.timezone
else:
    timezone='UTC'
    
tzutc=get_timezone('UTC')

tz = get_timezone(timezone)

# In utc

def timenow():
    
    t=datetime.utcnow()
    
    return format_datetime(t, "yyyyLLddHHmmss", tzutc)

#In utc

def normalize_time(year, month, day, hour, minute, second):
    
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

def format_tztime(time):
    
    #try:
        
    year, month, day, hour, minute, second=obtain_fields_time(time)
    
    t=datetime(year, month, day, hour, minute, second)
    
    return format_datetime(t, locale="es_ES", tzinfo=tz)
        
    #except:
        
    #    return timenow()
       