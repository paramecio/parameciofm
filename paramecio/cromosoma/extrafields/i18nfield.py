#!/usr/bin/env python3 

import json
from paramecio.cromosoma.webmodel import PhangoField
from paramecio.cromosoma.coreforms import BaseForm
from paramecio.cromosoma.extraforms.i18nform import I18nForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.httputils import GetPostFiles
import json

class I18nField(PhangoField):
    
    def __init__(self, name):
        
        super().__init__(name)
        
        self.name_form=I18nForm
        self.extra_parameters=[BaseForm(name, '')]
    
    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        arr_values={}

        try:
            arr_values=json.loads(value)
            
            if not arr_values:
                arr_values={}
            
        except:
            arr_values={}
        
        arr_real_values={}

        for lang in I18n.dict_i18n:
            arr_real_values[lang]=arr_values.get(lang, value)
        
        arr_values=arr_real_values
        
        if arr_values[I18n.default_lang]=='':
            self.error=True
            self.txt_error='Sorry, You need default language '+I18n.default_lang
            return json.dumps(arr_values)
        
        return json.dumps(arr_values)

    def get_type_sql(self):

        return 'TEXT NOT NULL DEFAULT ""'

    def obtain_lang_value(self, lang, value):
        
        return value.get(self.name+'_'+lang, '')
    
    def obtain_lang_from_post(self, lang, value):
        
        #getpost=GetPostFiles()
        
        #getpost.obtain_post()
        
        return "" #GetPostFiles.post.get(self.name+'_'+lang, '')
    
    
