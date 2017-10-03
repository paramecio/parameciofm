from paramecio.cromosoma.corefields import CharField
import re

mail_pattern=re.compile("\w[\w\.-]*@\w[\w\.-]+\.\w+")

class EmailField(CharField):
    
    def __init__(self, name, size=1024, required=False):
        
        super().__init__(name, size, required)
        
        self.error_default='Error: No valid format'        
    
    def check(self, value):
        
        value=super().check(value)
        
        self.error=False
        self.txt_error=''
        
        if not mail_pattern.match(value):
            
            self.error=True
            value=""
            self.txt_error=self.error_default
            
        return value
