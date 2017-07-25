from settings import config
from paramecio.cromosoma.extrafields.colorfield import ColorField
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_colorfield(self):
                
        colorfield=ColorField('color', '')
        
        value=colorfield.check('#ff00ff')
        
        self.assertEqual(16711935, value)

        value=colorfield.check('#ff00fff')
        
        self.assertEqual(0, value)
        

if __name__ == '__main__':
    unittest.main()
