from settings import config
from paramecio.cromosoma import corefields
from paramecio.cromosoma.extrafields.arrayfield import ArrayField
import unittest
import json

class TestFieldMethods(unittest.TestCase):
    
    def test_i18nfield(self):
        
        type_field=corefields.IntegerField('value')
        
        field=ArrayField('field', type_field)
        
        value=[1,2,5,'trick\'']
        
        json_encoded=field.check(value)
        
        self.assertEqual(json_encoded, '["1", "2", "5", "0"]')
        
        type_field=corefields.CharField('value')
        
        field=ArrayField('field', type_field)
        
        value=['trick', 'mytuquito', 25]
        
        json_encoded=field.check(value)
        
        self.assertEqual(json_encoded, '["trick", "mytuquito", "25"]')
        
        
