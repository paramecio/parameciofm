#!/usr/bin/python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.mtemplates import standard_t

class I18nForm(BaseForm):
    
    def __init__(self, name, value, form):
        
        super().__init__(name, value)
        
        self.form_child=form
    
    def form(self):
        print(self.name)
        return standard_t.load_template('forms/i18nform.phtml', name_form=self.name, form=self.form_child, arr_i18n=I18n.dict_i18n, lang_selected=I18n.default_lang)