from paramecio.citoplasma.mtemplates import env_theme, PTemplate
from paramecio.citoplasma.urls import make_url
from bottle import route, request
from settings import config

env=env_theme(__file__)

@route('/example')
def home():
    
    t=PTemplate(env)

    return "Hello World!!"

