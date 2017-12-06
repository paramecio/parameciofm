from paramecio.cromosoma.corefields import PhangoField
from paramecio.citoplasma import datetime
from paramecio.cromosoma.extraforms.dateform import DateForm

class DateField(PhangoField):
    
    def __init__(self, name, size=255, required=False):
        
        super().__init__(name, size, required)
        
        self.name_form=DateForm
        
        self.utc=True
        
        self.error_default='Error: Date format invalid'        
    
    def check(self, value):
        
        if self.utc:
        
            value=datetime.local_to_gmt(value)
        
        elif not datetime.obtain_timestamp(value, False):

            self.error=True
            self.txt_error=self.error_default
            return ''
        
        if value==False:
            
            self.error=True
            self.txt_error=self.error_default
            return ''
        
        return value
    
    def show_formatted(self, value):
        
        return datetime.format_date(value)
