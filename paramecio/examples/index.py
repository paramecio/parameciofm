from paramecio.citoplasma.mtemplates import ptemplate
from paramecio.citoplasma.urls import make_url
from bottle import route, request
from settings import config

t=ptemplate(__file__)

@route('/example')
def home():

    return "Hello World!!"

