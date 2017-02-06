#!/usr/bin/env python3

from paramecio.citoplasma.mtemplates import PTemplate, env_theme
from paramecio.citoplasma.urls import make_url
from paramecio.wsgiapp import app
from settings import config
from bottle import request

#t=ptemplate(__file__)
env=env_theme(__file__)

t=PTemplate(env)

@app.route('/welcome')
def home():
    
    return t.render_template('welcome.html', title="Welcome to Paramecio!!!", content="The simple web framework writed in Python3!!!")

@app.route('/welcome/<id:int>')
def page(id):
    return t.render_template('index.html', title="A simple example of a page", id=id, value=request.query.value)

@app.route('/welcome/test/<id:int>')
def test(id):
    
    return make_url('welcome/test/5', {'ohmygod': 'This is gooood', 'shutup':'Shut up!!'})

if config.default_module=="welcome":

    home = app.route("/")(home)
