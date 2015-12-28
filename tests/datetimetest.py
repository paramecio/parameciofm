from settings import config
from paramecio.citoplasma import datetime
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_timenow(self):
        
        time=datetime.normalize_time(2012, 12, 21, 23, 24, 21)
        
        self.assertEqual(time, '20121221232421')
        
        value=datetime.format_tztime(time)
        
        self.assertEqual(value, '23:24:21')
        
        value=datetime.format_tzdate(time)
        
        self.assertEqual(value, '2012/12/21')
        
        tz=datetime.obtain_timezone('Europe/Madrid')
        
        value=datetime.format_tzdate(time, tz)
        
        self.assertEqual(value, '2012/12/22')
        
        value=datetime.format_tztime(time, tz)
        
        self.assertEqual(value, '00:24:21')
        
        