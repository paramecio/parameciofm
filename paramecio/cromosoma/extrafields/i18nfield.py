#!/usr/bin/python3 

import json
from paramecio.cromosoma.webmodel import PhangoField
from paramecio.cromosoma.coreforms import TextForm
from paramecio.cromosoma.extraforms.i18nform import I18nForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.httputils import GetPostFiles

class I18nField(PhangoField):
    
    def __init__(self, name):
        
        super().__init__(name)
        
        self.name_form=I18nForm
        self.parameters=[TextForm(name, '')]
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        final_value={}
        
        func_get=self.obtain_lang_from_post
        
        if type(value).__name__=='dict':
            func_get=self.obtain_lang_value
            
        for lang in I18n.dict_i18n:
            final_value[lang]=func_get(lang, value)

        final_value[I18n.default_lang]=final_value.get(I18n.default_lang, '')
        
        if final_value[I18n.default_lang]=='':
            
            self.error=True
            self.txt_error='Sorry, You need default language '+I18n.default_lang
            return json.dumps(final_value)
        
        return json.dumps(final_value)
    

    def obtain_lang_value(self, lang, value):
        
        return value.get(self.name+'_'+lang, '')
    
    def obtain_lang_from_post(self, lang, value):
        
        return GetPostFiles.post.get(self.name+'_'+lang, '')
    
    