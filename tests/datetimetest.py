from settings import config
from paramecio.citoplasma import datetime
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_timenow(self):
        
        time='20121023401223'
        
        time_set=datetime.format_timedata(time)
        
        self.assertFalse(datetime.checkdatetime(time_set[0], time_set[1], time_set[2], time_set[3], time_set[4], time_set[5]))
        
        time='20121126231248'
        
        time_set=datetime.format_timedata(time)
        
        self.assertTrue(datetime.checkdatetime(time_set[0], time_set[1], time_set[2], time_set[3], time_set[4], time_set[5]))
        
        timestamp=datetime.obtain_timestamp(time)
        
        self.assertTrue(timestamp)
        
        datetime.timezone='Europe/Madrid'
        
        datetime.set_timezone()
        
        # Check conversions to gmt time
        
        gmtstamp=datetime.local_to_gmt(time)
        
        self.assertEqual(gmtstamp, '20121126221248')
        
        time_from_utc=datetime.format_time(time)
        
        self.assertEqual(time_from_utc, '00:12:48')
        
        date_from_utc=datetime.format_date(time)
        
        self.assertEqual(date_from_utc, '2012/11/27')
        
        time_summer='20120826231248'
        
        gmtstamp=datetime.local_to_gmt(time_summer)
        
        self.assertEqual(gmtstamp, '20120826211248')
        
        #today=datetime.now()
        
        #print(today)
        
        """
        tz=datetime.obtain_timezone('Europe/Madrid')
        
        time=datetime.normalize_time(2012, 12, 21, 23, 24, 21)
        
        self.assertEqual(time, '20121221232421')

        value=datetime.format_tztime(time)
        
        self.assertEqual(value, '23:24:21')
        
        value=datetime.format_tzdate(time)
        
        self.assertEqual(value, '2012/12/21')
        
        value=datetime.format_tzdate(time, tz)
        
        self.assertEqual(value, '2012/12/22')
        
        value=datetime.format_tztime(time, tz)
        
        self.assertEqual(value, '00:24:21')
        
        print(datetime.local_to_utc('20121221232421', tz))
        """

class TestClassMethods(unittest.TestCase):
    
    def test_timenow(self):

        datetime.timezone='Europe/Madrid'

        datetime.set_timezone()

        d=datetime.TimeClass('20121126231248')

        self.assertEqual('2012/11/26 23:12:48', d.format())
        
        d.local_to_utc()
        
        self.assertEqual('2012/11/26 22:12:48', d.format())
        
        d.utc_to_local()

        self.assertEqual('20130126231248', d.add_month(2))

        self.assertEqual('20120926231248', d.substract_month(2))

        self.assertEqual('20121203231248', d.add_day(7))
        self.assertEqual('20121119231248', d.substract_day(7))
        #self.assertEqual('20121203231248', d.substract_day(7))

if __name__ == '__main__':
    unittest.main()
