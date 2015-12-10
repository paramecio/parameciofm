#!/usr/bin/python

from mako.template import Template
from mako.lookup import TemplateLookup
from paramecio.citoplasma.urls import make_url, make_media_url, make_media_url_module, add_get_parameters
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.sessions import get_session
from settings import config
from os import path

# Preparing envs for views of modules, and views of 

""" A simple function for load views from themes using jinja2 

Env use loader = FileSystemLoader(['/path/to/templates', '/other/path'])
env = Environment(loader=FileSystemLoader(['/path/to/templates', '/other/path']))
template = env.get_template('mytemplate.html')
"""

class ptemplate:
    
    def __init__(self, module):
        
        module=path.dirname(module)
        
        self.autoescape_ext=('html', 'htm', 'xml', 'phtml')
        
        self.env=self.env_theme(module)
        
        self.filters={}
        
        #Adding basic filters for urls
        self.add_filter(make_url)
        
        self.add_filter(make_media_url)
        
        self.add_filter(make_media_url_module)
        
        self.add_filter(add_get_parameters)
        
        I18n_lang=I18n.lang
        
        self.add_filter(I18n.lang)
        
        self.add_filter(add_css_home)
        
        self.add_filter(add_js_home)
        
        self.add_filter(add_css_home_local)
        
        self.add_filter(add_js_home_local)
        
        self.add_filter(add_header_home)
        
        #self.auto_reload=True
        
        # Clean HeaderHTML
        
        HeaderHTML.css=[]
        HeaderHTML.js=[]
        HeaderHTML.header=[]
        HeaderHTML.cache_header=[]
        HeaderHTML.css_local={}
        HeaderHTML.js_local={}
    
    def clean_header_cache(self):
        
        HeaderHTML.css=[]
        HeaderHTML.js=[]
        HeaderHTML.css_local={}
        HeaderHTML.js_local={}
        HeaderHTML.header=[]
        HeaderHTML.cache_header=[]
    
    def guess_autoescape(self, template_name):
        
        if template_name is None or '.' not in template_name:
            return False
        
        ext = template_name.rsplit('.', 1)[1]
        return ext in self.autoescape_ext

    def env_theme(self, module):

        theme_templates='themes/'+config.theme+'/templates'

        module_templates=module+'/templates'
        
        #Standard templates
        
        standard_templates=path.dirname(__file__)+'/templates'
        #print(standard_templates)
        return TemplateLookup(directories=[theme_templates, module_templates, standard_templates], default_filters=['h'], input_encoding='utf-8', encoding_errors='replace')

        #return Environment(autoescape=self.guess_autoescape, auto_reload=True, loader=FileSystemLoader([theme_templates, module_templates]))

    def load_template(self, template_file, **arguments):
        
        template = self.env.get_template(template_file)
        
        arguments['HeaderHTML']=HeaderHTML
        
        arguments['show_flash_message']=show_flash_message
        
        for filter_name, filter_ in self.filters.items():
            arguments[filter_name]=filter_
        
        #Will be nice add hooks here
        
        return template.render(**arguments)

    def add_filter(self, filter_name):

        self.filters[filter_name.__name__]=filter_name


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
        
        for module, arr_js in HeaderHTML.js_local.items():
            for js in arr_js:
                final_js.append('<script language="Javascript" src="'+make_media_url_module('js/'+js, module)+'"></script>')
        
        return "\n".join(final_js)

    def css_home():
        
        final_css=[]
        
        for css in HeaderHTML.css:
            final_css.append('<link href="'+make_media_url('css/'+css)+'" rel="stylesheet" type="text/css"/>')

        for module, arr_css in HeaderHTML.css_local.items():
            
            for css in arr_css:
            
                final_css.append('<link href="'+make_media_url_module('css/'+css, module)+'" rel="stylesheet" type="text/css"/>')

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
        
    return ''
        
def add_js_home(js):
    
    if not js in HeaderHTML.js:
        HeaderHTML.js.append(js)

    return ''

def add_css_home_local(css, module):
    
    if not css in HeaderHTML.css_local:
        
        HeaderHTML.css_local[module]=HeaderHTML.css_local.get(module, [])
        
        HeaderHTML.css_local[module].append(css)

    return ''

def add_js_home_local(js, module):
    
    if not js in HeaderHTML.js_local:
        
        HeaderHTML.js_local[module]=HeaderHTML.js_local.get(module, [])
        
        HeaderHTML.js_local[module].append(js)

    return ''

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
    
