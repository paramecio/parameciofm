#!/usr/bin/python3

from collections import OrderedDict

def get_language(s):
    
    s['lang']=s.get('lang', None)
        
    lang_selected=None
    
    if s['lang']!=None:
        lang_selected=s['lang']
    else:
        s['lang']=I18n.default_lang
        lang_selected=I18n.default_lang

    return lang_selected

def get_menu(modules_admin):

    menu=OrderedDict()
                    
    for mod in modules_admin:
        if type(mod[1]).__name__!='list':
            menu[mod[2]]=mod
        else:
            
            menu[mod[2]]=mod[0]
            
            for submod in mod[1]:
                menu[submod[2]]=submod
                
    return menu
