#!/usr/bin/env python3

import json, re
from bottle import request, response
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.keyutils import create_key_encrypt

try:

    from settings import config
    
    no_csrf=False
    
    if hasattr(config, 'no_csrf'):
        no_csrf=config.no_csrf

except:

    class config:
        no_csrf=False


def filter_ajax(data, filter_tags=True):
    
    response.set_header('Content-type', 'application/json')
    
    #arr_data=map(
    
    json_encoded=json.dumps(data)
    
    #if filter_tags:
    #    json_encoded=json_encoded.replace('<', '&lt;').replace('>', '&gt;')
        
        #json_encoded=re.sub(r'\\"', '&quot;', json_encoded)
           
        #json_encoded=re.sub('\\"', "", json_encoded)
        #json_encoded=re.sub('\"', "&quot;", json_encoded)
        
        #replace('\\"', '&quot;')
        #replace('\\\\', '${slashes}').
        
    return json_encoded
    
class GetPostFiles:

    # Need this for obtain utf8 valid values
    
    def __init__(self):
    
        # Deprecated. use self.query
    
        self.get={}
        
        self.query={}
        
        self.post={}
        
        self.files={}
        
    def obtain_query(self):
        
        self.query={}
        
        self.query=request.query.decode()

    # Deprecated, is confuse. 

    def obtain_get(self):
        
        self.get={}
        
        self.get=request.query.decode()
    
    def obtain_post(self, required_post=[], ignore_csrf_token=False):
        
        self.post={}
        
        self.post=request.forms.decode()
        
        if len(required_post)==0:
            required_post=self.post.keys()
        
        for post in required_post:
            self.post[post]=self.post.get(post, '')
        
        s=get_session()
        
        if ignore_csrf_token==False and no_csrf==False:
        
            if 'csrf_token' in s:
                
                self.post['csrf_token']=self.post.get('csrf_token', '')
                
                if self.post['csrf_token']!=s['csrf_token'] and self.post['csrf_token'].strip()!="":
                    
                    raise NameError('Error: you need a valid csrf_token')
                else:
                    #Clean csrf_token
                    
                    del s['csrf_token']
                    
                    s.save()
                    

            else:
                raise NameError('Error: you don\'t send any valid csrf_token')

        #Check post_token
    
    def obtain_files(self):
        
        self.files=request.files
    
def request_method():
    
    return request.method
