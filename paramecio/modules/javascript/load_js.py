#!/usr/bin/python3

from paramecio.wsgiapp import app
from paramecio.citoplasma.mtemplates import env_theme, PTemplate
from settings import config
import os

#t=PTemplate(env)
    
#t.add_filter(make_admin_url)
workdir=os.getcwd()

arr_t={}

#dynamic javascript load
@app.route('/mediajs/<module>/<lang>/<filename:path>')
def send_javascript(module, lang, filename):    

    path_module=workdir+'/modules/'+module+'/js/'
    
    path=workdir+'/themes/'+config.theme+'/js/'+module

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
    
    return arr_t[module].load_template(file_path)
