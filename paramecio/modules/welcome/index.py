#!/usr/bin/env python3

from paramecio.citoplasma.mtemplates import PTemplate, env_theme
from paramecio.citoplasma.urls import make_url
from bottle import route, request
from settings import config

#t=ptemplate(__file__)
env=env_theme(__file__)

@route('/welcome')
def home():
    
    t=PTemplate(env)

    return t.load_template('welcome.html', title="Welcome to Paramecio!!!", content="The simple web framework writed in Python3!!!")

@route('/welcome/<id:int>')
def page(id):
    
    t=PTemplate(env)
    
    return t.load_template('index.html', title="A simple example of a page", id=id, value=request.query.value)

@route('/welcome/test/<id:int>')
def test(id):
    
    return make_url('welcome/test/5', {'ohmygod': 'This is gooood', 'shutup':'Shut up!!'})

if config.default_module=="welcome":

    home = route("/")(home)
