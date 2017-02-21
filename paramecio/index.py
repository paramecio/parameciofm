import os, sys, traceback, inspect, resource
from importlib import import_module
from bottle import route, get, post, run, default_app, abort, request, response, static_file, load, hook, error, debug, redirect
from settings import config
#from beaker.middleware import SessionMiddleware
from mimetypes import guess_type
from paramecio.cromosoma.webmodel import WebModel
from paramecio.citoplasma.datetime import set_timezone
from itsdangerous import JSONWebSignatureSerializer
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from paramecio.wsgiapp import app

modules_pass=False

#app.reset()

#from paramecio.citoplasma.sessions import generate_session

#Prepare links for static.
#WARNING: only use this feature in development, not in production.

#def create_app():
workdir=os.getcwd()
arr_module_path={}

def prepare_app():

    def print_memory():
        print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    routes={}

    module_loaded=None

    #Getting paths for loaded modules for use in media load files

    for module in config.modules:
        
        #controller_path=sys.modules[module]
        
        controller_base=sys.modules[module].__path__[0]
        
        base_module=module.split('.')[-1]
        
        arr_module_path[base_module]=controller_base

    #app.add_hook('before_request', print_memory)

    if config.session_enabled==True:
        #Create dir for sessions
        
        if 'session.data_dir' in config.session_opts:
            
            if not os.path.isdir(config.session_opts['session.data_dir']):
                os.makedirs(config.session_opts['session.data_dir'], 0o700, True)
        
    set_timezone()


# Clean last slash

@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
    
# Set error screen if not debug setted

if config.debug==False:
    @app.error(404)
    def error404(error):
        return 'Error: page not found'

debug(config.debug)

#Prepare app

application=app

# Prepare static routes

if config.yes_static==True:
    
    @app.route('/media/<filename:path>')
    def send_static(filename):
        mimetype=guess_type(workdir+'/themes/'+config.theme+'/media/'+filename)
        
        return static_file(filename, root=workdir+'/themes/'+config.theme+'/media/', mimetype=mimetype[0])
    
    #def add_func_static_module(module):
        
    @app.route('/mediafrom/<module>/<filename:path>')
    def send_static_module(module, filename):
        
        path_module=arr_module_path[module]+'/media/'
        
        file_path_module=path_module+filename
        
        path=workdir+'/themes/'+config.theme+'/media/'+module
        
        file_path=path+'/'+filename
        
        if os.path.isfile(file_path):
            mimetype=guess_type(path+'/'+filename)
            return static_file(filename, root=path, mimetype=mimetype[0])
            
        else:
            mimetype=guess_type(path_module+'/'+filename)
            return static_file(filename, root=path_module, mimetype=mimetype[0])

# Load modules

try:

    from settings import modules
    
    prepare_app()
    
except:

    @app.route('/')
    def catch_errors(all='/'):
        try:
            from pathlib import Path
            from settings import modules
            import time
            prepare_app()
            p=Path('index.py')
            p.touch()
            time.sleep(1)
        except:
            raise
            
        redirect(request.url)
    catch_errors=app.route('/<all:path>')(catch_errors)

        
def run_app(app):
    if config.server_used!='cherrypy':
        run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
    else:
        from paramecio.cherry import run_cherrypy_server
        run_cherrypy_server()

