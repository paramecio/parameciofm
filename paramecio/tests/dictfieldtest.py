from settings import config
from paramecio.cromosoma import corefields
from paramecio.cromosoma.extrafields.dictfield import DictField
import unittest
import json

class TestFieldMethods(unittest.TestCase):
    
    def test_i18nfield(self):
        
        type_field=corefields.IntegerField('value')
        
        field=DictField('field', type_field)
        
        value={'one': 1, 'two': 2, 'three': 5, 'raw': 'trick\''}
        
        json_encoded=field.check(value)
        
        value_real={'one': '1', 'two': '2', 'three': '5', 'raw': '0'}
        
        value_two=json.loads(json_encoded)
        
        self.assertEqual(value_two, value_real)
        
        # Check charfield dictfield
        
        type_field=corefields.CharField('value')
        
        field=DictField('field', type_field)
        
        value={'one': 'pepito', 'raw': 'trick\''}
        
        json_encoded=field.check(value)
        
        value_two=json.loads(json_encoded)
        
        value_real={'one': 'pepito', 'raw': 'trick\''}
        
        self.assertEqual(value_two, value_real)
        
         # Check charfield dictfield with quot
        
        type_field=corefields.CharField('value')
        
        field=DictField('field', type_field)
        
        value={'one': 'pepito', 'raw': 'trick"'}
        
        json_encoded=field.check(value)
        
        value_two=json.loads(json_encoded)
        
        value_real={'one': 'pepito', 'raw': 'trick&quot;'}
        
        self.assertEqual(value_two, value_real)
        
if __name__ == '__main__':
    unittest.main()
