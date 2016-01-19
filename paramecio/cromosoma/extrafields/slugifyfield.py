#!/usr/bin/python3

from paramecio.cromosoma.corefields import CharField
from paramecio.citoplasma.slugify import slugify

class SlugifyField(CharField):
    
    def check(value):
        
        value=slugify(value)
        
        if value=='':
            
            self.error=True
            
            return ''
    
        return value
    

