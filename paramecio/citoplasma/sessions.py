#!/usr/bin/python3

from itsdangerous import JSONWebSignatureSerializer
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from bottle import request, response

try:

    from settings import config

except:

    class config:
        cookie_name='paramecio_session'
        key_encrypt=create_key_encrypt_256(30)
        

class ParamecioSession:
    
    def __init__(self):
            self.session=request.environ.get(config.cookie_name)
            #self.token=request.get_cookie(config.cookie_name)
    
    def get(self, name, default_value):
        
        if not name in self.session:
            self.session[name]=default_value
            request.environ[config.cookie_name]=self.session
            request.environ[config.cookie_name]['save']=True

        return self.session[name]

    def __getitem__(self, key):
        
        return self.session[key]
        
    def __setitem__(self, key, value):
        
        self.session[key]=value
        request.environ[config.cookie_name]=self.session
        request.environ[config.cookie_name]['save']=True
        
    def __delitem__(self, key):
        
        del self.session[key]
        request.environ[config.cookie_name]=self.session
        request.environ[config.cookie_name]['save']=True

    def __contains__(self, key):
        
        if key in self.session:
            return True
        else:
            return False

    def __iter__(self):
        return self.session

    def __str__(self):
        return self.session.__str__()

    def keys(self):
        return self.session.keys()
        
        

def generate_session():
    
    random_text=create_key_encrypt_256(30)
    response.set_cookie(config.cookie_name, random_text)
    request.environ[config.cookie_name]={'token': random_text}

def get_session():
    
    if config.cookie_name in request.environ:
        
        return ParamecioSession()
    else:
        return None
    
    """
    try: 
        
        # Check if session was loaded, if loaded, get cache
        
        #return request.environ.get(config.cookie_name)
        code_session=request.get_cookie(config.cookie_name)
        
        try:
        
            #with fopen(config.session_opts['session.data_dir']) as signed_session:
            pass
                

        except:
            
            return {}
    
    except:
        
        return {}
    """
