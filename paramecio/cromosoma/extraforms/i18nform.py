#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.mtemplates import env_theme, PTemplate
import json

env=env_theme(__file__)

t=PTemplate(env)

class I18nForm(BaseForm):
    
    def __init__(self, name, value, form):
        
        super().__init__(name, value)
        
        self.form_child=form
    
    def form(self):
        
        lang_selected=I18n.get_default_lang()
        
        try:
            self.default_value=json.loads(self.default_value)
        except:
            self.default_value={}
        
        if type(self.default_value).__name__!='dict':
            self.default_value={}
        
        for lang in I18n.dict_i18n:
            self.default_value[lang]=self.default_value.get(lang, '')

        return t.load_template('forms/i18nform.phtml', name_form=self.name_field_id, real_name_form=self.name, form=self.form_child, arr_i18n=I18n.dict_i18n, lang_selected=lang_selected, default_value=self.default_value)
