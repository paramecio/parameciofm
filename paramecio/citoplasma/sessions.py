#!/usr/bin/python3

from bottle import request

try:

    from settings import config

except:

    class config:
        cookie_name='paramecio_session'
    

def get_session():
    return request.environ.get(config.cookie_name)
