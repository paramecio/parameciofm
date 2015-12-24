from paramecio.cromosoma.corefields import CharField
import re

mail_pattern=re.compile("\w[\w\.-]*@\w[\w\.-]+\.\w+")

class EmailField(CharField):
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        if not mail_pattern.match(value):
            
            self.error=True
            value=""
            self.txt_error='No valid format'
            
        return value