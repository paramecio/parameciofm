import os, sys, traceback, inspect, resource
from importlib import import_module
from bottle import route, get, post, run, default_app, abort, request, response, static_file, load, hook, error
from settings import config, modules
#from beaker.middleware import SessionMiddleware
from mimetypes import guess_type
from paramecio.cromosoma.webmodel import WebModel
from paramecio.citoplasma.datetime import set_timezone
from itsdangerous import JSONWebSignatureSerializer
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from paramecio.wsgiapp import app
#from paramecio.citoplasma.sessions import generate_session

#Prepare links for static.
#WARNING: only use this feature in development, not in production.

#def create_app():
workdir=os.getcwd()
arr_module_path={}
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
            return static_file(filename, root=path)
            
        else:
            mimetype=guess_type(path_module+'/'+filename)
            return static_file(filename, root=path_module)
"""
else:
    
    def add_func_static_module(module):
        pass
"""

def print_memory():
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    #print(request.cookies)

routes={}

module_loaded=None

#Getting paths for loaded modules for use in media load files

for module in config.modules:
    
    #controller_path=sys.modules[module]
    
    controller_base=sys.modules[module].__path__[0]
    
    base_module=module.split('.')[-1]
    
    arr_module_path[base_module]=controller_base

#Prepare ssl

if config.ssl==True:
    
    from citoplasma.gunicornssl import GunicornServerSSL
    
    GunicornServerSSL.cert_pem=config.cert_pem
    GunicornServerSSL.privkey_pem=config.privkey_pem
    
    config.server_used=GunicornServerSSL

#Prepare app

application=app

#app.add_hook('before_request', print_memory)

#app.add_hook('after_request', WebModel.close)

if config.session_enabled==True:
    #Create dir for sessions
    
    if 'session.data_dir' in config.session_opts:
        
        if not os.path.isdir(config.session_opts['session.data_dir']):
            os.makedirs(config.session_opts['session.data_dir'], 0o700, True)
    
    """
    key_encrypt=config.key_encrypt

    if config.session_opts['session.type']=='file':

        def load_session():
            
            code_session=request.get_cookie(config.cookie_name, secret=config.key_encrypt)
            
            if code_session==None:
                # Send cookie
                generate_session()
            else:
                
                # Check if file exists
                
                if os.path.isfile(config.session_opts['session.data_dir']+'/session_'+code_session):
                    with open(config.session_opts['session.data_dir']+'/session_'+code_session, 'r') as f:
                        
                        try:
                        
                            s = JSONWebSignatureSerializer(key_encrypt)
                            session_dict=f.read()
                            request.environ[config.cookie_name]=s.loads(session_dict)
                            request.environ[config.cookie_name]['token']=code_session
                        
                        except:
                            
                            # Clean fake session
                            
                            try: 
                                os.remove(config.session_opts['session.data_dir']+'/session_'+code_session)
                            
                            except:
                                
                                pass
                            
                            generate_session()
                    
                else:
                    request.environ[config.cookie_name]={'token': code_session}

        def save_session():
            
            save_session=request.environ[config.cookie_name]
            if 'save' in save_session:
                del save_session['save']
            # Here define the session type, if memcached, save data in memcached
                try:
                    with open(config.session_opts['session.data_dir']+'/session_'+save_session['token'], 'w') as f:
                        s = JSONWebSignatureSerializer(key_encrypt)
                        json_encode=s.dumps(save_session)
                        f.write(json_encode.decode('utf8'))
            
                except:
                    pass

        #request.environ[config.cookie_name]['save']
    #def save_session()
    
    app.add_hook('before_request', load_session)
    app.add_hook('after_request', save_session)
    #def 
    """
    #app = SessionMiddleware(app, config.session_opts, environ_key=config.cookie_name)

# Clean last slash

@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
    
# Set error screen if not debug setted

if config.debug==False:
    @app.error(404)
    def error404(error):
        return 'Error: page not found'
else:
    @app.error(500)
    def error500(error):
        return error

set_timezone()

def run_app(app):

    run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader, interval=0.5)
"""
if __name__ == "__main__":
    run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
    #else:
        #return run(app=app, host=config.host, server=config.server_used, port=config.port, debug=config.debug, reloader=config.reloader)
"""

