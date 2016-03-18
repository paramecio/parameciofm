import os, sys, traceback, inspect
from importlib import import_module
from bottle import route, get, post, run, default_app, abort, request, static_file, load
from settings import config, modules
from beaker.middleware import SessionMiddleware

#Prepare links for static.
#WARNING: only use this feature in development, not in production.

#def create_app():
    
arr_module_path={}

if config.yes_static==True:
    
    @route('/media/<filename:path>')
    def send_static(filename):
        return static_file(filename, root='themes/'+config.theme+'/media/')
    
    def add_func_static_module(module):
        
        @route('/mediafrom/<module>/<filename:path>')
        def send_static_module(module, filename):
            
            path_module=arr_module_path[module]+'/media/'
            
            file_path_module=path_module+filename
            
            path='themes/'+config.theme+'/media/'+module
            
            file_path=path+filename
            
            if os.path.isfile(file_path):
                return static_file(filename, root=path)
                
            else:
                return static_file(filename, root=path_module)
else:
    
    def add_func_static_module(module):
        pass

routes={}

module_loaded=None

#Import modules to load

for module in config.modules:
    
    controller_path=load(module)
        
    controller_base=os.path.dirname(controller_path.__file__)
    
    base_module=module.split('.')[-1]
    
    arr_module_path[base_module]=controller_base
    
    dir_controllers=os.listdir(controller_base)
    
    add_func_static_module(controller_base)
    
"""
    try:
        
        controller_path=load(module)
        
        controller_base=os.path.dirname(controller_path.__file__)
        
        base_module=module.split('.')[-1]
        
        arr_module_path[base_module]=controller_base
        
        dir_controllers=os.listdir(controller_base)
        
        for controller in dir_controllers:
            
            if controller.find('.py')!=-1 and controller.find('__init__')==-1:
                
                controller_py=controller.replace('.py', '')
                
                load(module+'.'+controller_py)

        add_func_static_module(controller_base)
        
    except:
        
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
"""
#exit()

#Prepare ssl

if config.ssl==True:
    
    from citoplasma.gunicornssl import GunicornServerSSL
    
    GunicornServerSSL.cert_pem=config.cert_pem
    GunicornServerSSL.privkey_pem=config.privkey_pem
    
    config.server_used=GunicornServerSSL

#Prepare app

app = application  = default_app()

if config.session_enabled==True:
    #Create dir for sessions
    
    if not os.path.isdir(config.session_opts['session.data_dir']):
        os.makedirs(config.session_opts['session.data_dir'], 0o700, True)

    app = SessionMiddleware(app, config.session_opts, environ_key=config.cookie_name)

def run_app(app):

    run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
"""
if __name__ == "__main__":
    run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
    #else:
        #return run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
"""

