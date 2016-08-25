#!/usr/bin/env python3

#from paramecio.cromosoma.webmodel import PhangoField
from paramecio.cromosoma.corefields import IntegerField
from paramecio.cromosoma.coreforms import SelectModelForm
from paramecio.citoplasma.httputils import GetPostFiles

class ParentField(IntegerField):
    
    def __init__(self, name, size=11, required=False, field_name='name'):
        
        super().__init__(name, size, required)
        
        #self.foreignkey=True
        self.indexed=True
        self.field_name=field_name

    def post_register(self):
        
        if self.model!=None:
            self.change_form(SelectModelForm, [self.model, self.field_name, self.model.name_field_id, self.name])
    
    def check(self, value):
        
        value=super().check(value)
        
        if self.model!=None:
            if self.model.updated==True:
                if self.model.name_field_id in self.model.post:
                    GetPostFiles.obtain_get()
                    
                    model_id=GetPostFiles.get.get(self.model.name_field_id, '0')
                    
                    if model_id==value:
                        self.error=True
                        self.txt_error='A field cannot be its own father'
                        value=0
                        return value
                        
                
        return value
