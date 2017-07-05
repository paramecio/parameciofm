from paramecio.cromosoma.corefields import PhangoField
from paramecio.citoplasma import datetime

class DateField(PhangoField):
    
    def __init__(self, name, size=255, required=False):
        
        super().__init__(name, size, required)
        
        self.utc=True
    
    def check(self, value):
        
        if self.utc:
        
            value=datetime.local_to_gmt(value)
        
        elif not datetime.obtain_timestamp(value, True):

            self.error=True
            self.txt_error='Date format invalid'        
            return ''
        
        if value==False:
            
            self.error=True
            self.txt_error='Date format invalid'
            return ''
        
        return value
    
    def show_formatted(self, value):
        
        return datetime.format_date(value)
