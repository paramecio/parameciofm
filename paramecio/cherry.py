# Import your application as:
# from wsgi import application
# Example:

from index import application
from settings import config

# Import CherryPy
import cherrypy

def run_cherrypy_server():
    
    access_log=''
    error_log=''
    
    if hasattr(config, 'access_log'):
        access_log=config.access_log
    if hasattr(config, 'error_log'):
        error_log=config.error_log
        
    cherrypy.config.update({'engine.autoreload.on': config.reloader, 'log.access_file': access_log, 'log.error_file': error_log})

    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host=config.host
    server.socket_port=config.port
    
    server.thread_pool=10
    
    if hasattr(config, 'thread_pool'):
        server.thread_pool=config.thread_pool

    # For SSL Support
    
    # By default use pyopenssl
    
    server.ssl_module='pyopenssl'
    
    if hasattr(config, 'ssl_module'):
        server.ssl_module=config.ssl_module
        
    if hasattr(config, 'ssl_certificate') and hasattr(config, 'private_key') and hasattr(config, 'certificate_chain'):
        server.ssl_certificate=config.ssl_certificate
        server.ssl_private_key=config.ssl_private_key
        server.ssl_certificate_chain=config.certificate_chain

    # Subscribe this server
    server.subscribe()

    # Example for a 2nd server (same steps as above):
    # Remember to use a different port

    # server2             = cherrypy._cpserver.Server()

    # server2.socket_host = "0.0.0.0"
    # server2.socket_port = 8081
    # server2.thread_pool = 30
    # server2.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()

