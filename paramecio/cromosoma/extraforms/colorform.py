#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.mtemplates import standard_t

class ColorForm(BaseForm):
    
    def __init__(self, name, value):
        
        super().__init__(name, value)
        
        self.t=standard_t
    
    def form(self):
        

        return self.t.load_template('forms/colorform.phtml', name_form=self.name_field_id, default_value=self.default_value, form=self)
