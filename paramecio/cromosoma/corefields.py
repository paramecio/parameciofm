from paramecio.cromosoma.webmodel import PhangoField
from paramecio.cromosoma import coreforms
from paramecio.citoplasma.i18n import I18n

class IntegerField(PhangoField):
    
    """Class that figure an integer sql type field.

    Args:
        name (str): The name of new field
        size (int): The size of the new field in database. By default 11.
        required (bool): Boolean for define if 

    """
    
    def __init__(self, name, size=11, required=False):
        super(IntegerField, self).__init__(name, size, required)
    
    def check(self, value):
        
        """Method for check if value is integer

        Args:
            value (int): The value to check

        """
        
        self.error=False
        self.txt_error=''
        
        try:
        
            value=str(int(value))
        
            if value=="0" and self.required==True:
                self.txt_error="The value is zero"
                self.error=True
        except:
            
            value="0"
            self.txt_error="The value is zero"
            self.error=True
        
        return value
    
    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'INT('+str(self.size)+') NOT NULL DEFAULT "0"'
        
class BigIntegerField(IntegerField):
    
    """Class that figure an big integer sql type field.
    
    Only change the sql type with respect to IntegerField

    """
    
    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'BIGINT('+str(self.size)+') NOT NULL DEFAULT "0"'
    

class FloatField(PhangoField):
    
    """Class that figure an float sql type field.

    Args:
        name (str): The name of new field
        size (int): The size of the new field in database. By default 11.
        required (bool): Boolean for define if 

    """
    
    def __init__(self, name, size=11, required=False):
        super(FloatField, self).__init__(name, size, required)
        
        self.error_default="The value is zero"
    
    def check(self, value):
        
        """Method for check if value is integer

        Args:
            value (float): The value to check

        """
        
        self.error=False
        self.txt_error=''
        
        try:

            value=str(value)

            if value.find(',')!=-1:
                value=value.replace(',', '.')
            
            value=str(float(value))
            
            if value==0 and self.required==True:
                self.txt_error=self.error_default
                self.error=True
        except:
            
            value="0"
            self.txt_error=self.error_default
            self.error=True
        
        return value
    
    def get_type_sql(self):

        return 'FLOAT NOT NULL DEFAULT "0"'

class DoubleField(FloatField):
    
    def get_type_sql(self):

        return 'DOUBLE NOT NULL DEFAULT "0"'

class CharField(PhangoField):
    
    pass

class TextField(PhangoField):
    
    def __init__(self, name, required=False):
        super().__init__(name, 11, required)
        
    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'TEXT NOT NULL'

class HTMLField(TextField):
    
    def __init__(self, name, required=False):
        super().__init__(name, required)

    def check(self, value):
        
        return re.sub('<.*?script?>', '', value)


class ForeignKeyField(IntegerField):
    
    def __init__(self, name, related_table, size=11, required=False, identifier_field='id', named_field="id", select_fields=[]):
        
        super(ForeignKeyField, self).__init__(name, size, required)
        
        self.table_id=related_table.name_field_id
    
        self.table_name=related_table.name
    
        self.related_model=related_table
    
        self.identifier_field=identifier_field
        
        self.named_field=named_field
        
        self.select_fields=select_fields
    
        self.foreignkey=True
        
        self.change_form(coreforms.SelectModelForm, [related_table, self.named_field, self.identifier_field])

    def check(self, value):
        
        value=super().check(value)
        
        if value=='0' or value==0:
            value='NULL'
            
        return value

    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'INT NULL'
        

class BooleanField(IntegerField):
    
    def __init__(self, name, size=1):
        
        required=False
        
        self.yes_text=I18n.lang('common', 'yes', 'Yes')
        self.no_text=I18n.lang('common', 'no', 'No')
        
        super(IntegerField, self).__init__(name, size, required)
    
        self.default_error="Need 0 or 1 value"
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        try:
        
            value=int(value)
            
            if value<0 or value>1:
                self.txt_error=self.default_error
                self.error=True

        except:
            
            self.error=True
            self.txt_error=self.default_error
            value=0

        value=str(value)

        return value
    
    def get_type_sql(self):
        
        """Method for return the sql code for this type

        """

        return 'BOOLEAN NOT NULL DEFAULT "0"'
    
    def show_formatted(self, value):
    
        value=int(value)
        
        if value==0:
            value=self.no_text
        else:
            value=self.yes_text
    
        return str(value)
