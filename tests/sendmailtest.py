from settings import config
from paramecio.citoplasma import sendmail
import unittest

class TestFieldMethods(unittest.TestCase):
    
    def test_sendmail(self):
        
        s=sendmail.SendMail()
        
        #self.assertEqual(phrase, 'this---is-a-crap-phrase-o---f-oh-yeah--')
        
        self.assertTrue( s.send(config.portal_email, config.email_test, 'This is a test', 'A message for test a simple email method', content_type='plain', attachments=[]) )
        
        self.assertTrue( s.send(config.portal_email, config.email_test, 'This is a test', 'A message for test a simple email method in <b>html</b>', content_type='html', attachments=[]) )
        
        self.assertTrue( s.send(config.portal_email, config.email_test, 'This is a test', 'A message for test a simple email method in <b>html</b> and attachments', content_type='html', attachments=['tests/images/image.jpg']) )
        
        s.smtp.quit()