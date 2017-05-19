#!/usr/bin/python3

from paramecio.wsgiapp import app
from paramecio.citoplasma.mtemplates import env_theme, PTemplate
from settings import config
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.i18n import I18n
from bottle import response
import os

#t=PTemplate(env)
    
#t.add_filter(make_admin_url)
workdir=os.getcwd()

arr_t={}

#dynamic javascript load
@app.route('/mediajs/<module>/<lang>/<filename:path>')
def send_javascript(module, lang, filename):    

    s=get_session()
    
    if lang in I18n.dict_i18n:
        s['lang']=lang

    path_module='modules/'+module+'/js'
    
    path='themes/'+config.theme+'/js/'+module

    file_path_module=path_module+'/'+filename
    file_path_theme=path+'/'+filename
    
    file_path=file_path_module
    load_path=path_module
    
    if os.path.isfile(file_path_theme):
        
        file_path=file_path_theme
        load_path=path
    
    if not load_path in arr_t:
        env=env_theme(load_path)
        arr_t[load_path]=PTemplate(env)

    response.set_header('Content-type', 'application/javascript')

    return arr_t[load_path].load_template(filename)
