from paramecio.cromosoma.webmodel import WebModel, PhangoField
import json

class DictField(PhangoField):
    
    def __init__(self, name, field_type, required=False):
        
        super().__init__(name, required)
        
        self.field_type=field_type
    
        self.error_default='Sorry, the json dict is invalid'

        self.set_default='NOT NULL'
    
    def check(self, value):
        
        if type(value).__name__=='str':
            try:
                value=json.loads(value)
            except json.JSONDecodeError:
                
                value={}
                self.error=True
                self.txt_error=self.error_default
                
        elif type(value).__name__!='dict':
            
            value={}
            self.error=True
            self.txt_error=self.error_default
            
        for k,v in value.items():
            
            value[k]=self.field_type.check(v)
            
        final_value=json.dumps(value)
        
        #final_value=WebModel.escape_sql(final_value)
        
        return final_value

    def get_type_sql(self):

        return 'TEXT '+self.set_default
    
    def show_formatted(self, value):
        
        return ", ".join(value)
    
