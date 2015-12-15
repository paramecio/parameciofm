from paramecio.cromosoma.webmodel import PhangoField
from paramecio.cromosoma import coreforms
from paramecio.citoplasma.i18n import I18n

class IntegerField(PhangoField):
    
    def __init__(self, name, size=11, required=False):
        super(IntegerField, self).__init__(name, size, required)
    
    def check(self, value):
        
        self.error=None
        self.txt_error=''
        
        try:
        
            value=str(int(value))
        
            if value==0 and self.required==True:
                self.txt_error="The value is zero"
                self.error=True
        except:
            
            self.error=True

        return value
    
    def get_type_sql(self):

        return 'INT('+str(self.size)+') NOT NULL DEFAULT "0"'

class CharField(PhangoField):
    
    pass

class TextField(PhangoField):
    
    def __init__(self, name, required=False):
        super().__init__(name, 11, required)
    
    def get_type_sql(self):

        return 'TEXT NOT NULL DEFAULT ""'

class ForeignKeyField(IntegerField):
    
    def __init__(self, name, related_table, size=11, required=False, identifier_field='id', named_field="id", select_fields=[]):
    
        self.table_id=related_table.name_field_id
    
        self.table_name=related_table.name
    
        self.identifier_field=identifier_field
        
        self.named_field=named_field
        
        self.select_fields=select_fields
        
        super(ForeignKeyField, self).__init__(name, size, required)
    
        self.foreignkey=True

class BooleanField(IntegerField):
    
    def __init__(self, name, size=1):
        
        required=False
        
        self.yes=I18n.lang('common', 'yes', 'Yes')
        self.no=I18n.lang('common', 'no', 'No')
        
        super(IntegerField, self).__init__(name, size, required)
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        try:
        
            value=int(value)
            
            if value<0 or value>1:
                self.txt_error="Need 0 or 1 value"
                self.error=True

        except:
            
            self.error=True
            value=0

        value=str(value)

        return value
    
    def get_type_sql(self):

        return 'BOOLEAN NOT NULL DEFAULT "0"'
    
    def show_formatted(self, value):
    
        value=int(value)
        
        if value==0:
            value=self.yes_text
        else:
            value=self.no_text
    
        return value
