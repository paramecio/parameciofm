#!/usr/bin/python3

from bottle import request

class GetPostFiles:

    # Need this for obtain utf8 valid values
    get={}
    
    post={}
    
    files=None

    @staticmethod
    def obtain_get():
        
        GetPostFiles.get={}
        
        GetPostFiles.get=request.query.decode()
    
    @staticmethod
    def obtain_post():
        
        GetPostFiles.post={}
        
        GetPostFiles.post=request.forms.decode()
    
    @staticmethod
    def obtain_files():
        
        GetPostFiles.files=request.files