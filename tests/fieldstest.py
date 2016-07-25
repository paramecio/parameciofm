from settings import config
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma import corefields
from paramecio.cromosoma.extrafields.emailfield import EmailField
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
        
        self.assertEqual(value, "injection_'")
        
    def test_integerfield(self):
        
        integerfield=corefields.IntegerField('example', 11)
        
        integerfield.required=True
        
        integerfield.check(0)
        
        self.assertTrue(integerfield.error)
        
        integerfield.check('25')
        
        self.assertFalse(integerfield.error)
        
        value=integerfield.check("25'")
        
        self.assertEqual(value, "0")
        
    def test_emailfield(self):
        
        emailfield=EmailField('email')
        
        emailfield.required=True
        
        emailfield.check('exampleweb-t-sys.com')
        
        self.assertTrue(emailfield.error)
        
        emailfield.check('example@web-t-sys.com')
        
        self.assertFalse(emailfield.error)
        
        
