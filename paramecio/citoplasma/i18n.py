#!/usr/bin/python3

from importlib import import_module

def load_lang(*args):
    
    for module in args:
    
        lang_path=module+'.i18n'
        
        try: 
            i18n_module=import_module(module)
        
            return True
        
        except:
            return False
        
       # here load the language 
        

class I18n:
    
    l={}
    
    @staticmethod
    def lang(module, symbol, text_default):
        
        I18n.l[module]=I18n.l.get(module, {})
        
        I18n.l[module][symbol]=I18n.l[module].get(symbol, text_default)
        
        return I18n.l[module][symbol]


