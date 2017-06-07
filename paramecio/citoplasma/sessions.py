#!/usr/bin/env python3

from itsdangerous import URLSafeSerializer
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from bottle import request, response
import os
import json
import fcntl
import errno
import time
import shutil
import uuid
from diskcache import Cache

try:

    from settings import config

except:

    class config:
        cookie_name='paramecio.session'
        key_encrypt=create_key_encrypt_256(30)
        session_opts={'session.data_dir': 'sessions', 'session.type': 'file', 'session.path': 'paramecio'}

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
        
        # Here get the function for load session
        
        save_session(self.session['token'], self.session)

def generate_session(session={}):
    
    #secret=URLSafeSerializer(config.key_encrypt)
    
    #session=secret.dumps(session)
    
    token=create_key(30).replace('/', '#')

    s={'token': token}

    response.set_cookie(config.cookie_name, token, path=config.session_opts['session.path'])
    
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
                
                # Here get the function for load session
                
                s=load_session(cookie)
                
                request.environ['session']=s

                    
        else:
            
            s=request.environ['session']
    
    return ParamecioSession(s)

if config.session_opts['session.type']=='mysql':
    
    pass
    
elif config.session_opts['session.type']=='redis':
    
    import redis

    def load_session(token):
        
        s={}
        
        r=redis.StrictRedis(host=config.session_opts['session.host'], port=config.session_opts['session.port'], db=config.session_opts['session.db'])
        
        value=r.get(token)
        
        if not value:
            s={'token': token}
        else:
            try:
                s=json.loads(value.decode('utf-8'))
            except:
                s={'token': token}
        return s

    def save_session(token, session):

        r=redis.StrictRedis(host=config.session_opts['session.host'], port=config.session_opts['session.port'], db=config.session_opts['session.db'])
        
        r.set(token, json.dumps(session))

    def after_session():
        pass

else:
    
    cache=Cache(config.session_opts['session.data_dir'])

    def load_session(token):
        
        # Here get the function for load session

        if token in cache:
            s=json.loads(cache[token])
        else:
            s={'token': token}
            cache.add(token, json.dumps(s))
            
        return s

    def save_session(token, session):
            
        cache[token]=json.dumps(session)
            #pass
        pass
            #Lock file, if cannot lock wait

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
            return ParamecioSession({})
    
    except:
        
        return ParamecioSession({})
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
