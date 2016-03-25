#!/usr/bin/python

from jinja2 import Template, Environment, FileSystemLoader
from paramecio.citoplasma.urls import make_url, make_media_url, make_media_url_module, add_get_parameters
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.sessions import get_session
from settings import config

# Preparing envs for views of modules, and views of 

""" A simple function for load views from themes using jinja2 

Env use loader = FileSystemLoader(['/path/to/templates', '/other/path'])
env = Environment(loader=FileSystemLoader(['/path/to/templates', '/other/path']))
template = env.get_template('mytemplate.html')
"""

class ptemplate:
    
    def __init__(self, module):
        
        self.autoescape_ext=('html', 'htm', 'xml', 'phtml')
        
        self.env=self.env_theme(module)
        
        #Adding basic filters for urls
        
        self.add_filter(make_url)
        
        self.add_filter(make_media_url)
        
        self.add_filter(make_media_url_module)
        
        self.add_filter(add_get_parameters)
        
        I18n_lang=I18n.lang
        
        self.add_filter(I18n.lang)
        
        self.add_filter(add_css_home)
        
        self.add_filter(add_js_home)
        
        self.add_filter(add_header_home)
        
        self.auto_reload=True
        
        # Clean HeaderHTML
        
        HeaderHTML.css=[]
        HeaderHTML.js=[]
        HeaderHTML.header=[]
        HeaderHTML.cache_header=[]
    
    def guess_autoescape(self, template_name):
        
        if template_name is None or '.' not in template_name:
            return False
        
        ext = template_name.rsplit('.', 1)[1]
        return ext in self.autoescape_ext

    def env_theme(self, module):

        #standard_templates=path.dirname(__file__)+'/templates'

        module_templates=module+'/templates'
        
        theme_templates='themes/'+config.theme+'/templates'

        return Environment(autoescape=self.guess_autoescape, auto_reload=True, loader=FileSystemLoader([theme_templates, module_templates]))

    def load_template(self, template_file, **arguments):
        
        template = self.env.get_template(template_file)
        
        arguments['HeaderHTML']=HeaderHTML
        
        arguments['show_flash_message']=show_flash_message
        
        #Will be nice add hooks here
        
        return template.render(arguments)

    def add_filter(self, filter_name):

        self.env.filters[filter_name.__name__]=filter_name


class HeaderHTML:
    
    css=[]
    js=[]
    header=[]
    cache_header={}

    def header_home():
        
        final_header="\n".join(HeaderHTML.header)
        
        HeaderHTML.header=[]
        
        return final_header

    def js_home():

        final_js=[]
        
        for js in HeaderHTML.js:
            final_js.append('<script language="Javascript" src="'+make_media_url('js/'+js)+'"></script>')
        
        HeaderHTML.js=[]
        
        return "\n".join(final_js)

    def css_home():
        
        final_css=[]
        
        for css in HeaderHTML.css:
            final_css.append('<link href="'+make_media_url('css/'+css)+'" rel="stylesheet" type="text/css"/>')

        HeaderHTML.css=[]

        return "\n".join(final_css)


def add_header_home(variable, only_one_time=False):
        
        
        if only_one_time==True:
            HeaderHTML.cache_header.get(variable, 0)
            
            if cache_header[variable]==1:
                return ''
        #HeaderHTML.cache_header[variable]=1
        
        HeaderHTML.header.append(variable)
        
        return ''

def add_css_home(css):
    
    if not css in HeaderHTML.css:
        HeaderHTML.css.append(css)
    
    return ""
    
def add_js_home(js):
    
    if not js in HeaderHTML.js:
        HeaderHTML.js.append(js)
    
    return ""

def set_flash_message(message):
    
    s=get_session()
    
    s['flash']=s.get('flash', "")
    
    s['flash']=message
    
def show_flash_message():
    
    message=""
    
    s=get_session()
    
    s['flash']=s.get('flash', "")
    
    if s['flash']!="":
        message='<div class="flash">'+s['flash']+'</div>'
    
    s['flash']=''
    
    return message
    
standard_t=ptemplate(__file__)
