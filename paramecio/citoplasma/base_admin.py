#!/usr/bin/env python3

from paramecio.citoplasma.mtemplates import PTemplate
from paramecio.citoplasma.adminutils import check_login, get_language, get_menu
from paramecio.cromosoma.webmodel import WebModel
from paramecio.citoplasma.sessions import get_session
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

#Load menu in runtime
        
menu=get_menu(config_admin.modules_admin)

def base_admin(func_view, env, title, **args):
    
    env.directories.insert(1, config.paramecio_root+'/modules/admin/templates')
    
    content_index=''

    connection=WebModel.connection()
    #Fix, make local variable
    
    t=PTemplate(env)
    
    s=get_session()
    
    if check_login():
                
    
        lang_selected=get_language(s)
        
        content_index=func_view(connection, t, s, **args)

        return t.render_template('admin/content.html', title=title, content_index=content_index, menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
        
    else:
        redirect(make_url(config.admin_folder))
        
def base_simple_admin(func_view, env, title, **args):
    
    if check_login():
        
        return func_view(connection, t, s, **args)
    
    
