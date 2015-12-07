#!/usr/bin/python3

from bottle import request
from settings import config

def get_session():
        return request.environ.get(config.cookie_name)