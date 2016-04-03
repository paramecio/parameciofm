#!/usr/bin/python3

from bottle import request
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.keyutils import create_key_encrypt

class GetPostFiles:

    # Need this for obtain utf8 valid values
    get={}
    
    post={}
    
    files={}

    @staticmethod
    def obtain_get():
        
        GetPostFiles.get={}
        
        GetPostFiles.get=request.query.decode()
    
    @staticmethod
    def obtain_post(required_post=[]):
        
        GetPostFiles.post={}
        
        GetPostFiles.post=request.forms.decode()
        
        for post in required_post:
            
            GetPostFiles.post[post]=GetPostFiles.post.get(post, '')

        s=get_session()
        
        if 'csrf_token' in s:
            
            GetPostFiles.post['csrf_token']=GetPostFiles.post.get('csrf_token', '')
            
            if GetPostFiles.post['csrf_token']!=s['csrf_token']:
                
                raise NameError('Error: you need a valid csrf_token')

        else:
            raise NameError('Error: you don\'t send any valid csrf_token')

        #Check post_token
    
    @staticmethod
    def obtain_files():
        
        GetPostFiles.files=request.files
