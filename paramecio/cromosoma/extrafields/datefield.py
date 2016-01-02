from paramecio.cromosoma.corefields import CharField
from paramecio.citoplasma import datetime

class DateField(CharField):
    
    def check(self, value):
        
        value=datetime.local_to_gmt(value)
        
        if value==False:
            
            self.error=True
            self.error='Date format invalid'
            return ''
        
        return value
    
    def show_formatted(self, value):
        
        return datetime.format_date(value)