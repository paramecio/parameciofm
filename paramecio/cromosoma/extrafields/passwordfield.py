from paramecio.cromosoma.corefields import PhangoField
from paramecio.cromosoma.coreforms import PasswordForm
from passlib.hash import bcrypt

class PasswordField(PhangoField):
    
    def __init__(self, name, size=255, required=False):
        
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
            value = bcrypt.encrypt(value)
            
        
        return value
    
    @staticmethod
    def verify( password, h):
        
        return bcrypt.verify(password, h)
    
    
