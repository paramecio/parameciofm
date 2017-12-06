#!/usr/bin/env python3

from settings import config
from bottle import request, response, HTTPResponse

# A modified version of bottle url for don't need set x-proxy shit for redirect...

def redirect(url, code=None):
    """ Aborts execution and causes a 303 or 302 redirect, depending on
        the HTTP protocol version. """
    if not code:
       	code = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    res = response.copy(cls=HTTPResponse)
    res.status = code
    res.body = ""
    res.set_header('Location', url)
    raise res

#Simple method for make urls

def make_url(path, query_args={}):
    
    """
        This is a method for create urls for the system
        
        Keyword arguments:
        path -- The path to the module
        query_args -- a ser of get variables for add to url
        
    """
    
    get_query=''
    
    if len(query_args)>0:
        
        get_query='?'+"&".join( [x+'='+y for x,y in query_args.items()] )
    
    return config.base_url+path+get_query
    
def make_url_domain(path, query_args={}):
    
    return config.domain_url+make_url(path, query_args)

def add_get_parameters(url, **args):
    
    added_url='&'
    
    if url.find('?')==-1:
        added_url='?'
    
    return url+added_url+"&".join( [x+'='+str(y) for x,y in args.items()] )

def get_actual_url():
    
    return config.base_url[:len(config.base_url)-1]+request.path

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
