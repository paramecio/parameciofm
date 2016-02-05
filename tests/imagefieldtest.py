from bottle import FileUpload
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma.extrafields.imagefield import ImageField
from paramecio.citoplasma.httputils import GetPostFiles
from settings import config
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_imagefield(self):
        
        f=open('tests/images/image.jpg', 'rb')
        
        GetPostFiles.files={}
        
        GetPostFiles.files['image_file']=FileUpload(f, 'image_file', 'image.jpg')
        
        field=ImageField('image', 'tests/images/uploads', module=None, size=255, required=False)
        
        field.yes_thumbnail=True
        
        field.check('')
        
        print(field.txt_error)
        
        self.assertFalse(field.error)
        
        pass


"""from settings import config
from bottle import FileUpload
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma.imagefield import ImageField
from paramecio.citoplasma.httputils import GetPostFiles
import unittest

class TestImageFieldMethods(unittest.TestCase):
    
    def test_image(self):
        #name, save_folder, module=None, size=255, required=False)
        
        #FileUpload(fileobj, name, filename
        x=0
        pass
        
        GetPostFiles.files=
        
        field=ImageField(, 'test/image', module=None, size=255, required=False)
        
        field.required=True
        
        field.check('')
        
        self.assertTrue(field.error)
        
        field.check('content')
        
        self.assertFalse(field.error)
        
        value=field.check("injection_'")
        
        self.assertEqual(value, "injection_\\'")"""
        
   
