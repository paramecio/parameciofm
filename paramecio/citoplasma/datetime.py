import time
from datetime import date, datetime, tzinfo
import arrow
# from babel.dates import format_date, format_datetime, format_time, get_timezone, UTC
from settings import config
from bottle import hook
from paramecio.citoplasma.sessions import get_session
from os import environ


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
    
def now(utc=False, tz=''):
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
        if tz=='':
            actual=arrow.now().format(sql_format_time)
        else:
            actual=arrow.to(tz).now().format(sql_format_time)
    else:
        actual=arrow.utcnow().format(sql_format_time)
    
    return actual
    
def today(utc=False,tz=''):
    
    return now(utc, tz)[:8]+'000000'
    
# Get actual timestamp

def obtain_timestamp(timeform, local=False, tz=''):
    
    y, m, d, h, mi, s=format_timedata(timeform)
    
    if checkdatetime(y, m, d, h, mi, s):
        
        #timestamp=int(time.mktime((y, m, d, h, mi, s, 0, 0, -1)))       
        
        if local:
            
            #offset=time.altzone
        
            #return timestamp-offset
            
            if tz=='':
                tz=environ.get('TZ', 'utc')
            
            t=arrow.arrow.Arrow(y, m, d, h, mi, s).to(tz)
            
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

# Get a utc timestamp and convert to local

def timestamp_to_datetime_local(timestamp, tz=''):
    
    #time_set=time.localtime(timestamp)
    
    #return time.strftime(sql_format_time, time_set)
    
    t=arrow.get(timestamp)

    if tz=='':
        tz=environ['TZ']    
    
    return t.to(tz).format(sql_format_time)


def format_datetime(format_time, timeform, func_utc_return):
    
    timestamp=obtain_timestamp(timeform)
    
    if timestamp:
    
        t=func_utc_return(timestamp)
        
        return t.format(format_time)
        
    else:
    
        return False
        
# This method parse local time to gmt

def local_to_gmt(timeform, sql_format_time=sql_format_time):
    
    return format_datetime(sql_format_time, timeform, substract_utc)

# time.localtime is useless, you need sum the time offset to the date

def gmt_to_local(timeform, sql_format_time=sql_format_time):
    
    return format_datetime(sql_format_time, timeform, sum_utc)

def format_time(timeform):
    
    return format_datetime(format_time_txt, timeform, sum_utc)

def format_date(timeform):
    
    return format_datetime(format_date_txt, timeform, sum_utc)

def format_fulldate(timeform):
    
    return format_datetime(format_date_txt+' '+format_time_txt, timeform, sum_utc)

def format_local_time(timeform):
    
    return format_datetime(format_time_txt, timeform, no_utc)

def format_local_date(timeform):
    
    return format_datetime(format_date_txt, timeform, no_utc)

def format_local_fulldate(timeform):
    
    return format_datetime(format_date_txt+' '+format_time_txt, timeform, no_utc)

def format_strtime(strtime, timeform):
    
    return format_datetime(strtime, timeform, sum_utc)    

def format_local_strtime(strtime, timeform):
    
    return format_datetime(strtime, timeform, no_utc)    

#Input is utc timestamp, return local arrow object

def sum_utc(timestamp, tz=''):
    
    #offset=time.altzone

    #return time.localtime(timestamp-offset)
    
    t=arrow.get(timestamp)
    
    if tz=='':
        tz=environ['TZ']    
    
    return t.to(tz)

#Input is local timestamp, return utc arrow object

def substract_utc(timestamp, tz=''):
    
    #offset=time.altzone

    #return time.localtime(timestamp+offset)
    
    #t=arrow.get(timestamp).to('UTC')
    
    timeform=timestamp_to_datetime(timestamp)
    
    y, m, d, h, mi, s=format_timedata(timeform)

    if tz=='':
        tz=environ['TZ']    
    
    t=arrow.get(datetime(y, m, d, h, mi, s), tz).to('UTC')
    
    return t

def no_utc(timestamp):
    
    return arrow.get(timestamp)

# def date_to_sql(date_sql):
    
    

class TimeClass:
    
    def __init__(self, timestamp=0, tz=''):
        
        self.utc=False
        
        self.format_time=sql_format_time
        self.format_time_txt=format_time_txt

        self.format_date_txt=format_date_txt

        self.format_date_full=format_date_txt+' '+format_time_txt
        
        self.tz=environ.get('TZ', 'utc')
        
        if tz:
            self.tz=tz
        
        if type(timestamp).__name__=='int':

            if self.utc:

                self.datetime=utcnow()
                
            else:
                self.datetime=timestamp_to_datetime(timestamp)        

        else:
            
            self.datetime=timestamp
        
        y, m, d, h, mi, s=format_timedata(self.datetime)
        
        self.t=arrow.get(datetime(y, m, d, h, mi, s), self.tz)
    
    def add_month(self, num_months):
        
        m=self.t.shift(months=+num_months)
        
        return m.format(self.format_time)

    def substract_month(self, num_months):
        
        m=self.t.shift(months=-num_months)
        
        return m.format(self.format_time)

    def add_day(self, num_days):
        
        m=self.t.shift(days=+num_days)
        
        return m.format(self.format_time)

    def substract_day(self, num_days):
        
        m=self.t.shift(days=-num_days)
        
        return m.format(self.format_time)

    def add_year(self, num_years):
        
        m=self.t.shift(years=+num_years)
        
        return m.format(self.format_time)

    def substract_year(self, num_years):
        
        m=self.t.shift(years=-num_years)
        
        return m.format(self.format_time)
    
    def format(self):
        
        return self.t.format(self.format_date_full)
    
    def local_to_utc(self):
        
        self.t=self.t.to('utc')

    # Only use 

    def utc_to_local(self):
        
        self.t=self.t.to(self.tz)

    def local_to_tz(self, tz):
        
        self.t=self.t.to(tz)

    def now(self, utc=False):        
        
        if not utc:

            actual=arrow.now(self.tz).format(sql_format_time)
        else:
            actual=arrow.utcnow().format(sql_format_time)
        
        return actual
        
    def today(self, utc=False):
        
        if utc:
        
            return arrow.utcnow()[:8]+'000000'
        else:
            return arrow.now(self.tz)[:8]+'000000'            

    def timestamp_to_datetime(self, timestamp):
        
        return arrow.get(timestamp).format(sql_format_time)

    def obtain_timestamp(self, timeform):
        
        y, m, d, h, mi, s=format_timedata(timeform)
        
        if checkdatetime(y, m, d, h, mi, s):
            
            timestamp=arrow.arrow.Arrow(y, m, d, h, mi, s).timestamp                
            
            return timestamp
            
        else:
            return False
            
    def format_strtime(self, strtime, timeform):
    
        #timestamp=self.obtain_timestamp(timeform)
        try:
            y, m, d, h, mi, s=format_timedata(timeform)

            return arrow.get(datetime(y, m, d, h, mi, s), self.tz).format(strtime)
            
        except:
        
            return False
