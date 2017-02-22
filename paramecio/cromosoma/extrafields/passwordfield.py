from paramecio.cromosoma.corefields import PhangoField
from paramecio.cromosoma.coreforms import PasswordForm
from hmac import compare_digest as compare_hash
import crypt

class PasswordField(PhangoField):
    
    def __init__(self, name, size=1024, required=False):
        
        super(PasswordField, self).__init__(name, size, required)    
        self.protected=True
        self.name_form=PasswordForm
        self.default_value=''
    
    def check(self, value):
        
        self.txt_error=''
        self.error=False
        
        value.strip()
        
        if value=='':
            
            if self.model!=None:
            
                if self.model.updated==True:
                    self.required=False
                    self.check_blank=True
                    return ""
                else:
                    
                    self.txt_error="The field is empty"
                    self.error=True
                    
            else:
                self.txt_error="The field is empty"
                self.error=True
            
        else:
            
            #if crypt.METHOD_SHA512 in crypt.methods:
            
            #salt=crypt.mksalt(crypt.METHOD_SHA512)
            value=crypt.crypt(value)

            """
            else:
                
                self.txt_error="You need the SHA512 method"
                self.error=True
                return ""
            """
        
        return value
    
    @staticmethod
    def verify( password, h):
        #return bcrypt_sha256.verify(password, h)
        return compare_hash(h, crypt.crypt(password, h))

# Old function bcrypt

"""
try:

    from passlib.hash import bcrypt
    from passlib.hash import bcrypt_sha256

    class PasswordField(PhangoField):
        
        def __init__(self, name, size=1024, required=False):
            
            super(PasswordField, self).__init__(name, size, required)    
            self.protected=True
            self.name_form=PasswordForm
            self.default_value=''
        
        def check(self, value):
            
            self.txt_error=''
            self.error=False
            
            value.strip()
            
            if value=='':
                
                if self.model!=None:
                
                    if self.model.updated==True:
                        self.required=False
                        self.check_blank=True
                        return ""
                    else:
                        
                        self.txt_error="The field is empty"
                        self.error=True
                        
                else:
                    self.txt_error="The field is empty"
                    self.error=True
                
            else:
                
                #if crypt.METHOD_SHA512 in crypt.methods:
                
                #value = bcrypt_sha256.encrypt(value)
                value = bcrypt_sha256.hash(value)
            
            return value
        
        @staticmethod
        def verify( password, h):
            
            return bcrypt_sha256.verify(password, h)
    
except:
"""   
