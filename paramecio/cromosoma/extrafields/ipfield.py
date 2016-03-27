from paramecio.cromosoma.corefields import CharField
import ipaddress

class IpField(CharField):
    
    def check(self, value):
        
        try:
        
            value=str(ipaddress.ip_address(value))
        
        except:
            
            self.error=True
            self.txt_error='No Valid IP'
            value=""

            
        return value
