#!/usr/bin/env python3

from itsdangerous import URLSafeSerializer
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from bottle import request, response
import os
import json

try:

    from settings import config

except:

    class config:
        cookie_name='paramecio.session'
        key_encrypt=create_key_encrypt_256(30)

# Cookie session
# This save the session in a cookie for maximum performance. In next version i can use memcached or something for session
# In next versions have two secret_keys for more security.

class ParamecioSession:
    
    def __init__(self, session_dict):
        self.session=session_dict
    
    def get(self, name, default_value):
        
        if not name in self.session:
            self.session[name]=default_value

        return self.session[name]

    def __getitem__(self, key):
        
        return self.session[key]
        
    def __setitem__(self, key, value):
        
        self.session[key]=value
        
    def __delitem__(self, key):
        
        if key!='token':
            del self.session[key]

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
        
    def remove(self):
        response.delete_cookie(config.cookie_name, path="/")
        
    def delete(self):
        self.remove()
        
    def save(self):
        
        path_cookie=config.session_opts['session.data_dir']+'/session_'+self.session['token']
        
        with open(path_cookie, 'w') as f:
            f.write(json.dumps(self.session))
        

def generate_session(session={}):
    
    #secret=URLSafeSerializer(config.key_encrypt)
    
    #session=secret.dumps(session)
    
    token=create_key(30).replace('/', '#')
    
    response.set_cookie(config.cookie_name, token, path=config.session_opts['session.path'])
    
    s={'token': token}
    
    request.environ['session']=s
    
    return s

def get_session():
    
    s={}
    
    if request.environ:
    
        if not 'session' in request.environ:
            
            cookie=None
            
            if request.cookies.get(config.cookie_name):
                cookie=request.get_cookie(config.cookie_name)
             
            if not cookie:
                
                s=generate_session()
                
            else:
                    
                path_cookie=config.session_opts['session.data_dir']+'/session_'+cookie
                
                if os.path.isfile(path_cookie):
                    
                    with open(path_cookie) as f:
                        s=json.loads(f.read())
                else:
                    s={'token': cookie}
                    
                request.environ['session']=s

                    
        else:
            
            s=request.environ['session']
    
    return ParamecioSession(s)
    
    

"""
def generate_session():
    s=request.environ.get(config.cookie_name)
    s.invalidate()

def get_session():
    
    try:
    
        if config.cookie_name in request.environ:
            
            return request.environ.get(config.cookie_name)
            #ParamecioSession()
        else:
            return None
    
    except:
        
        return None
"""
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
