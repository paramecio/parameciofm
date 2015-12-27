from settings import config
from paramecio.citoplasma import datetime
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_timenow(self):
        
        time=datetime.normalize_time(2012, 12, 21, 00, 24, 21)
        
        self.assertEqual(time, '20121221002421')
        
        value=datetime.format_tztime(time)
        
        self.assertEqual(value, '21/12/2012 00:24:21')
        