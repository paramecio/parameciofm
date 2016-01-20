#!/usr/bin/python3

from paramecio.cromosoma.corefields import CharField
from paramecio.citoplasma.slugify import slugify
from paramecio.cromosoma.coreforms import HiddenForm

class SlugifyField(CharField):
    
    def __init__(self, name, size=255, field_related=None, required=False):
        
        super(SlugifyField, self).__init__(name, size, required)
        
        self.name_form=HiddenForm
        
        self.field_related=field_related
    
    def check(self, value):
        
        value=slugify(value)
        
        if value=='':
            
            if self.model!=None and self.field_related!=None:
                
                self.model.post[self.field_related]=self.model.post.get(self.field_related, '')
                
                value=slugify(self.model.post[self.field_related])
                
                if value=='':
            
                    self.error=True
                    self.error_txt='Value is empty'
                    
                    return ''
        return value
    

