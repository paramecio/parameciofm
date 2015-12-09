from settings import config
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma import corefields
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_phangofield(self):
        
        field=corefields.PhangoField('example', 255)
        
        field.required=True
        
        field.check('')
        
        self.assertTrue(field.error)
        
        field.check('content')
        
        self.assertFalse(field.error)
        
        value=field.check("injection_'")
        
        self.assertEqual(value, "injection_\\'")
        
        