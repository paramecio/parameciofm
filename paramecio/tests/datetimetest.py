from settings import config
from paramecio.citoplasma import datetime
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_timenow(self):
        
        time='20121023401223'
        
        time_set=datetime.format_timedata(time)
        
        self.assertFalse(datetime.checkdatetime(time_set[0], time_set[1], time_set[2], time_set[3], time_set[4], time_set[5]))
        
        time='20121026231248'
        
        time_set=datetime.format_timedata(time)
        
        self.assertTrue(datetime.checkdatetime(time_set[0], time_set[1], time_set[2], time_set[3], time_set[4], time_set[5]))
        
        timestamp=datetime.obtain_timestamp(time)
        
        self.assertTrue(timestamp)
        
        datetime.timezone='Europe/Madrid'
        
        datetime.set_timezone()
        
        gmtstamp=datetime.local_to_gmt(time)
        
        self.assertEqual(gmtstamp, '20121026221248')
        
        time_from_utc=datetime.format_time(time)
        
        self.assertEqual(time_from_utc, '00:12:48')
        
        date_from_utc=datetime.format_date(time)
        
        self.assertEqual(date_from_utc, '2012/10/27')
        
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

if __name__ == '__main__':
    unittest.main()
