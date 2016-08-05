#!/usr/bin/python3

from collections import OrderedDict
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.urls import make_url

try:

    from settings import config

except:

    class config:
        admin_folder='admin'
        
def make_admin_url(url, query_args={}):
    
    return make_url('%s/%s' % (config.admin_folder, url), query_args)

def get_language(s):
    
    s['lang']=s.get('lang', None)
        
    lang_selected=None
    
    if s['lang']!=None:
        lang_selected=s['lang']
    else:
        s['lang']=I18n.default_lang
        s.save()
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

def check_login():
    
    s=get_session()
    
    if 'login' in s:
        
        if 'privileges' in s:
        
            if s['privileges']==2:
                
                return True
    
    return False

