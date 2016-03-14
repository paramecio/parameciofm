#!/usr/bin/python3

from bottle import request

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
    
    @staticmethod
    def obtain_files():
        
        GetPostFiles.files=request.files
