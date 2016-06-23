from paramecio.cromosoma.webmodel import PhangoField
import json

class ArrayField(PhangoField):
    
    def __init__(self, name, field_type, required=False):
        
        super().__init__(name, required)
        
        self.field_type=field_type
    
    def check(self, value):
        
        if type(value).__name__=='str':
            try:
                value=json.loads(value)
            except json.JSONDecodeError:
                
                value=[]
                self.error=True
                self.txt_error='Sorry, the json array is invalid'
                
        elif type(value).__name__!='list':
            
            value=[]
            self.error=True
            self.txt_error='Sorry, the json array is invalid'
        
        if type(self.field_type).__name__!='ArrayField':        
            for k,v in enumerate(value):
                
                value[k]=self.field_type.check(v)
        
        final_value=json.dumps(value)
        
        final_value=super().check(final_value)
        
        return final_value

    def get_type_sql(self):

        return 'TEXT NOT NULL'
    
    def show_formatted(self, value):
        
        return ", ".join(value)
    
    def loads(self, value):
        
        try:
        
            return json.loads(value)
        except:
            
            return False
