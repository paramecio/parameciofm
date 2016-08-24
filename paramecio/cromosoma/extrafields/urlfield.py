from paramecio.cromosoma.corefields import CharField
import re

check_url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

class UrlField(CharField):
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        if not check_url.match(value):
            
            self.error=True
            value=""
            self.txt_error='No valid URL format'
            
        return value
        
check_domain=re.compile('^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$')

class DomainField(CharField):
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        if not check_domain.match(value):
            
            self.error=True
            value=""
            self.txt_error='No valid domain format'
            
        return value
