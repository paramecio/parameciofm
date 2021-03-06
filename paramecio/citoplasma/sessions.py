#!/usr/bin/env python3

from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from oslo_concurrency import lockutils


try:

    from settings import config

except:

    class config:
        cookie_name='paramecio.session'
        key_encrypt=create_key_encrypt_256(30)
        session_opts={'session.data_dir': 'sessions', 'session.type': 'file', 'session.path': 'paramecio'}

from itsdangerous import JSONWebSignatureSerializer
from bottle import request, response
import os
import json
import fcntl
import errno
import time
import shutil
import uuid
#from diskcache import Cache
#from dogpile.cache import make_region

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
        
    def reset(self):
        
        token=self.session['token']
        self.session={'token': token}
        self.save()


def get_session():
    
    s={}

    try:
        
        if request.environ:
        
            if not 'session' in request.environ:
                
                cookie=None
                
                if request.cookies.get(config.cookie_name):
                    cookie=request.get_cookie(config.cookie_name)
                 
                if not cookie:
                    
                    if hasattr(request, 'app'):
                    
                        s=generate_session()
                    
                else:
                    
                    # Here get the function for load session
                    
                    s=load_session(cookie)
                    
                    request.environ['session']=s

                        
            else:
                
                s=request.environ['session']
    except RuntimeError:
        
        pass
    
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
    
    def generate_session(session={}):
        
        #secret=URLSafeSerializer(config.key_encrypt)
        
        #session=secret.dumps(session)
        
        token=create_key(30).replace('/', '#')

        s={'token': token}

        response.set_cookie(config.cookie_name, token, path=config.session_opts['session.path'])
        
        request.environ['session']=s

        file_session=config.session_opts['session.data_dir']+'/'+token+'_session'
            
        save_session(token, s, True)

        request.environ['session']=s
        
        return s
        
    def regenerate_session():
        
        token=create_key(30).replace('/', '#')

        s={'token': token}

        response.set_cookie(config.cookie_name, token, path=config.session_opts['session.path'])

        file_session=config.session_opts['session.data_dir']+'/'+token+'_session'
            
        save_session(token, s, True)

        request.environ['session']=s
        
        return ParamecioSession(s)
    
    def load_session(token):
        
        file_session=config.session_opts['session.data_dir']+'/'+token+'_session'
        
        if os.path.isfile(file_session):
        
            with open(file_session) as f:
            
                try:
                
                    s=json.loads(f.read())
                    os.utime(file_session)
        
                except:
                    
                    s={'token': token}
                
        else:
            return generate_session({'token': token})
        
        return s
        
    @lockutils.synchronized('not_thread_safe')
    def save_session(token, session, create_file=False):
        
        file_session=config.session_opts['session.data_dir']+'/'+token+'_session'

        # Check if exists lock

        if os.path.isfile(file_session) or create_file:
            
            with open(file_session, 'w') as f:                
                #try:
                json_session=json.dumps(session)
                
                f.write(json_session)
