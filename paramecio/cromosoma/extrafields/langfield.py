#!/usr/bin/env python3

from paramecio.cromosoma.corefields import CharField
from paramecio.cromosoma import coreforms
from paramecio.citoplasma.i18n import I18n

class LangField(CharField):
    
    def __init__(self, name, size=255, required=False):
    
        super(CharField, self).__init__(name, size, required)
        
        select_lang={}

        for lang in I18n.dict_i18n:
            select_lang[lang]=lang

        self.change_form(coreforms.SelectForm, [select_lang])
        self.default_value=I18n.default_lang
        
    def check(self, value):
        
        if value not in I18n.dict_i18n:
            
            value=I18n.default_lang

        return value
