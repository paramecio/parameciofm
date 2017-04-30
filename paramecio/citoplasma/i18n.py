#!/usr/bin/env python3

from importlib import import_module
from paramecio.citoplasma.sessions import get_session

yes_session=False

i18n_module={}

def load_lang(*args):
    
    for module in args:
        
        lang_path=module[0]+'.i18n.'+module[1]
        
        try:
            
            i18n_module[lang_path]=import_module(lang_path)
            
            pass
        
        except:
            pass
        
       # here load the language 
        

class I18n:
    
    default_lang='en-US'
    
    dict_i18n=['en-US', 'es-ES']
    
    l={}
    
    #@staticmethod 
    #def set_lang(code_lang):
    #    if default_lang
        
    
    @staticmethod
    def get_default_lang():
        
        lang=I18n.default_lang
        
        s=get_session()

        lang=s.get('lang', lang)
            
        return lang
    
    @staticmethod
    def lang(module, symbol, text_default):
        
        lang=I18n.get_default_lang()
        
        I18n.l[lang]=I18n.l.get(lang, {})
        
        I18n.l[lang][module]=I18n.l[lang].get(module, {})
        
        I18n.l[lang][module][symbol]=I18n.l[lang][module].get(symbol, text_default)
        
        return I18n.l[lang][module][symbol]


