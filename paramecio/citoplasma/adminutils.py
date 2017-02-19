#!/usr/bin/env python3

from collections import OrderedDict
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.urls import make_url
from paramecio.citoplasma.i18n import I18n

try:

    from settings import config

except:

    class config:
        admin_folder='admin'
try:

    from settings import config_admin

except:

    class config_admin:
        modules_admin=[]

#Function for get an admin url

def make_admin_url(url, query_args={}):
    
    """Function for get an admin url
    
    A special function based in make_url for get admin urls. You can use only the module admin part in the url and get a real url for use in your templates or other functions.
    
    Args:
        url (str): The url without admin part for use how base. Example: with 'pages' as url value you get http://localhost:8080/admin/pages
        query_args (dict): A serie of dictionary values where you get a url query result as it: {'key1': 'value1', 'key2': 'value2'} -> key1=value1&key2=value2
        
    Returns:
        str: A new url valid for use in href links directing to admin site
    
    """
    
    return make_url('%s/%s' % (config.admin_folder, url), query_args)

def get_language(s):
    
    """Function for get language from a session
    
    With this function you gan get easily the language of session
    
    Args:
        s (session): A session object where the language value is stored
        
    Returns:
        str: The language string
    
    """
    
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

    """Function for get a ordered dict with modules admin
    
    With this method you get a menu ordered dict for use internally in admin module. 
    
    Args:
        modules_admin (OrderedDict): The ordereddict used get it from admin configuration of Paramecio system
    
    Returns:
        OrderedDict: A new dict prepared for use in admin module.
    
    """

    menu=OrderedDict()
                    
    for mod in modules_admin:
        if type(mod[1]).__name__!='list':
            menu[mod[2]]=mod
        else:
            
            menu[mod[2]]=mod[0]
            
            for submod in mod[1]:
                if submod[2] in menu:
                    print('WARNING: you would not set the admin url for '+submod[2]+' with same general name of module if is not stand alone admin file')
                menu[submod[2]]=submod
                
    return menu

def check_login():
    
    """Function for check if correct login in admin module
    
    With this function you can check if the online user is login or not
    """
    
    s=get_session()
    
    if 'login' in s:
        
        if 'privileges' in s:
        
            if s['privileges']==2:
                
                return True
    
    return False
    
