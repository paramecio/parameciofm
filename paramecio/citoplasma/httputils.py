#!/usr/bin/python3

from bottle import request
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.keyutils import create_key_encrypt

class GetPostFiles:

    # Need this for obtain utf8 valid values
    
    def __init__(self):
    
        self.get={}
        
        self.post={}
        
        self.files={}

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
        
        if ignore_csrf_token==False:
        
            if 'csrf_token' in s:
                
                self.post['csrf_token']=self.post.get('csrf_token', '')
                
                if self.post['csrf_token']!=s['csrf_token'] and self.post['csrf_token'].strip()!="":
                    
                    raise NameError('Error: you need a valid csrf_token')
                else:
                    #Clean csrf_token
                    
                    del s['csrf_token']
                    

            else:
                raise NameError('Error: you don\'t send any valid csrf_token')

        #Check post_token
    
    def obtain_files(self):
        
        self.files=request.files
