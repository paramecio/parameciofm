#!/usr/bin/python3

# A simple utility for filter ips. Only use this if you don't use a server with blocking ips system

from settings import config
from bottle import request

def filterip():
    #Check ip
    ip = request.environ.get('REMOTE_ADDR')
    
    if ip in config.allowed_ips:
    
        return True
    else:
        
        return False
    