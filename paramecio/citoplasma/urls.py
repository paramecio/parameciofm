#!/usr/bin/python3

from settings import config

#Simple method for make urls

def make_url(path, query_args={}):
    
    """
        This is a method for create urls for the system
        
       
        Keyword arguments:
        module -- The module where search code to execute
        controller -- The controller where search code to execute
        method -- The method to execute
        query_args -- a ser of get variables for add to url
        
    """
    
    get_query=''
    
    if len(query_args)>0:
        
        get_query='?'+"&".join( [x+'='+y for x,y in query_args.items()] )
    
    return config.base_url+path+get_query

def add_get_parameters(url, **args):
    
    added_url='&'
    
    if url.find('?')==-1:
        added_url='?'
    
    return url+added_url+"&".join( [x+'='+str(y) for x,y in args.items()] )

if config.yes_static==True:
    
    def make_media_url(file_path):
        
        return config.media_url+'media/'+file_path
        
    def make_media_url_module(file_path, module):
        
        return config.media_url+'mediafrom/'+module+'/'+file_path
else:
    
    def make_media_url(file_path):

        return config.media_url+'media/'+file_path
    
    def make_media_url_module(file_path, module):

        return config.media_url+'media/'+module+'/'+file_path
