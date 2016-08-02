from settings import config
from paramecio.citoplasma import slugify
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_slugify(self):
        
        phrase=slugify.slugify('this!()is a crap phrase o}çÇf oh yeah¡\'')
        
        self.assertEqual(phrase, 'this---is-a-crap-phrase-o---f-oh-yeah--')
        

if __name__ == '__main__':
    unittest.main()
