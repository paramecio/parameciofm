import os, sys, traceback, inspect
from importlib import import_module, reload
from bottle import route, get, post, run, default_app, abort, request, static_file
from settings import config
from beaker.middleware import SessionMiddleware

#Prepare links for static.
#WARNING: only use this feature in development, not in production.

def create_app():

    if config.yes_static==True:
        
        @route('/media/<filename:path>')
        def send_static(filename):
            return static_file(filename, root='themes/'+config.theme+'/media/')
        
        def add_func_static_module(module):
            
            @route('/mediafrom/<module>/<filename:path>')
            def send_static_module(module, filename):
                
                path_module=module+'/media/'
                
                file_path_module=path_module+filename
                
                path=module+'/media/'
                
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
        
        try:
            
            #dir_controllers=os.listdir(config.base_modules.replace('.', '/')+'/'+module)
            
            #arr_views=[x for x in dir_modules if x.find('.py')!=-1 and x.find('__init__')==-1]
            """
            for controller in config.base_modules:
                if controller.find('.py')!=-1 and controller.find('__init__')==-1:
                    controller=controller.replace('.py', '')
            """
            controller_path=import_module(module)
            
            controller_base=os.path.dirname(controller_path.__file__)
            
            dir_controllers=os.listdir(controller_base)
            
            for controller in dir_controllers:
                
                if controller.find('.py')!=-1 and controller.find('__init__')==-1:
                    
                    controller_py=controller.replace('.py', '')
                    print(controller_py)
                    import_module(module+'.'+controller_py)

            add_func_static_module(controller_base)
            
        except:
            
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
    
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
    
    if __name__ == "__main__":
        run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
    else:
        return run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)


