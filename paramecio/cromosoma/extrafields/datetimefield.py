from paramecio.cromosoma.corefields import PhangoField
from paramecio.citoplasma import datetime
from paramecio.cromosoma.extraforms.dateform import DateForm

class DateTimeField(PhangoField):
    
    def __init__(self, name, size=255, required=False):
        
        super().__init__(name, size, required)
        
        self.name_form=DateForm
        
        self.utc=False
        
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
        else:
            
            """
            format_date_txt="YYYY/MM/DD"

            format_time_txt="HH:mm:ss"
            """
            
            value=datetime.format_local_strtime('YYYY-MM-DD HH:mm:ss', value)
        
        return value
    
    def show_formatted(self, value):
        
        # Convert to paramecio value
        value=str(value)
        value=value.replace('-', '').replace(':', '').replace(' ', '')
        
        return datetime.format_date(value)

    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'DATETIME NOT NULL'
