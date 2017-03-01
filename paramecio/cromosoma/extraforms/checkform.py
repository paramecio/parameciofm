#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm

class CheckForm(BaseForm):
    
    def __init__(self, name, value, real_value=1):
        super(CheckForm, self).__init__(name, value)
        
        self.real_value=real_value
    
    def form(self):
        
        arr_value={}
        
        arr_value[self.setform(self.default_value)]=''
        
        arr_value[self.setform(self.real_value)]='checked'
        
        return '<input type="checkbox" class="'+self.css+'" name="'+self.name+'" id="'+self.name_field_id+'" value="'+str(self.real_value)+'" '+arr_value[self.setform(self.default_value)]+'>'
