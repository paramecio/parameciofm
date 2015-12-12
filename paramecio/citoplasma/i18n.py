#!/usr/bin/python3

from importlib import import_module

def load_lang(*args):
    
    for module in args:
    
        lang_path=module[0]+'.i18n.'+I18n.default_lang+'.'+module[1]
        
        try: 
            i18n_module=import_module(lang_path)
            
            pass
        
        except:
            pass
        
       # here load the language 
        

class I18n:
    
    default_lang='en-US'
    
    dict_i18n=['en-US', 'es-ES']
    
    l={}
    
    @staticmethod
    def lang(module, symbol, text_default):
        
        I18n.l[module]=I18n.l.get(module, {})
        
        I18n.l[module][symbol]=I18n.l[module].get(symbol, text_default)
        
        return I18n.l[module][symbol]


