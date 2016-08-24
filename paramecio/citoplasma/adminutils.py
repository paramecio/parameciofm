#!/usr/bin/python3

from collections import OrderedDict
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.urls import make_url
from paramecio.cromosoma.webmodel import WebModel
from paramecio.citoplasma import mtemplates
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
    
def base_admin(func_view, env, title, **args):
    
    env.directories.insert(1, config.paramecio_root+'/modules/admin/templates')
    
    content_index=''

    connection=WebModel.connection()
    #Fix, make local variable
    
    t=mtemplates.PTemplate(env)
    
    s=get_session()
    
    if check_login():
                
        #Load menu
        
        menu=get_menu(config_admin.modules_admin)
    
        lang_selected=get_language(s)
        
        content_index=func_view(connection, t, s, **args)

        return t.load_template('admin/content.html', title=title, content_index=content_index, menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
        
    else:
        redirect(make_url(config.admin_folder))

