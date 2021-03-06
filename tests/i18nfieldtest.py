from settings import config
from paramecio.cromosoma.extrafields.i18nfield import I18nField
from paramecio.citoplasma.httputils import GetPostFiles
from paramecio.citoplasma.i18n import I18n
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_i18nfield(self):
        """
        field=I18nField('i18n')
        
        value=field.check({})
        
        self.assertTrue(field.error)
        
        value=field.check({'i18n_es-ES': 'Mi text', 'i18n_en-US': 'My Text'})
        
        self.assertFalse(field.error)
        
        GetPostFiles.post={'i18n_es-ES': 'Mi text', 'i18n_en-US': 'My Text'}
        
        value=field.check('')
        
        self.assertFalse(field.error)
        
        I18n.default_lang='en-US'
        
        forms=GetPostFiles()
        
        forms.post={'i18n_es-ES': 'My Text'}
        
        value=field.check('')
        
        self.assertTrue(field.error)
        """
        
        # Need fixes
        
        pass

if __name__ == '__main__':
    unittest.main()
