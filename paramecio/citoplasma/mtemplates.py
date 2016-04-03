#!/usr/bin/python

from bottle import hook
from mako.template import Template
from mako.lookup import TemplateLookup
from paramecio.citoplasma.urls import make_url, make_media_url, make_media_url_module, add_get_parameters
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.sessions import get_session
from paramecio.cromosoma.formsutils import csrf_token
from settings import config
from os import path

# Preparing envs for views of modules, and views of 

""" A simple function for load views from themes using jinja2 

Env use loader = FileSystemLoader(['/path/to/templates', '/other/path'])
env = Environment(loader=FileSystemLoader(['/path/to/templates', '/other/path']))
template = env.get_template('mytemplate.html')
"""

#@hook('after_request')
#def clean_tpl_cache():
    
    #ptemplate.clean_header_cache()
    #pass


class ptemplate:
    
    template_context=None
    
    # A simple method used in internal things of paramecio
    
    show_basic_template=True
    
    def __init__(self, module, cache_enabled=True, cache_impl='', cache_args={}):
        
        ext=module[len(module)-3:]
        
        if ext=='.py':
        
            module=path.dirname(module)
        
        self.autoescape_ext=('html', 'htm', 'xml', 'phtml')
        
        self.cache_enabled=cache_enabled
        
        self.cache_impl=cache_impl
        
        self.cache_args=cache_args
        
        self.module_directory="./tmp/modules"
        
        self.env=self.env_theme(module)
        
        self.filters={}
        
        #Place where templates contexts is loaded
        
        self.templates={}
        
        #Adding basic filters for urls
        self.add_filter(make_url)
        
        self.add_filter(make_media_url)
        
        self.add_filter(make_media_url_module)
        
        self.add_filter(add_get_parameters)
        
        self.add_filter(csrf_token)
        
        I18n_lang=I18n.lang
        
        self.add_filter(I18n.lang)
        
        self.add_filter(add_css_home)
        
        self.add_filter(add_js_home)
        
        self.add_filter(add_css_home_local)
        
        self.add_filter(add_js_home_local)
        
        self.add_filter(add_header_home)
        
        self.filters['HeaderHTML']=HeaderHTML
        
        self.filters['show_flash_message']=show_flash_message
        
        #self.auto_reload=True
        
        # Clean HeaderHTML
        
        HeaderHTML.css=[]
        HeaderHTML.js=[]
        HeaderHTML.header=[]
        HeaderHTML.cache_header=[]
        HeaderHTML.css_local={}
        HeaderHTML.js_local={}
        
        
    @staticmethod
    def clean_header_cache():
        
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

        standard_templates=path.dirname(__file__)+'/templates'

        module_templates=module+'/templates'
        
        theme_templates='themes/'+config.theme+'/templates'
        
        #Standard templates
        #print(standard_templates)
        return TemplateLookup(directories=[theme_templates, module_templates, standard_templates], default_filters=['h'], input_encoding='utf-8', encoding_errors='replace', cache_enabled=self.cache_enabled, cache_impl=self.cache_impl, cache_args=self.cache_args, module_directory=self.module_directory)

        #, cache_enabled=self.cache_enabled, cache_impl=self.cache_impl, cache_args=self.cache_args

        #return Environment(autoescape=self.guess_autoescape, auto_reload=True, loader=FileSystemLoader([theme_templates, module_templates]))

    def load_templates(self, template_files):
        
        for template_file in template_files:
            
            self.templates[template_file]=self.env.get_template(template_file)

    def load_template(self, template_file, **arguments):
        
        template = self.env.get_template(template_file)
        
        arguments.update(self.filters)
        
        #arguments['make_media_url']=make_media_url
        
        return template.render(**arguments)

    def render_template(self, template_file, **arguments):
        
        arguments.update(self.filters)
        
        return self.templates[template_file].render(**arguments)

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
        
        HeaderHTML.js=[]
        HeaderHTML.js_local={}
        
        return "\n".join(final_js)

    def css_home():
        
        final_css=[]
        
        for css in HeaderHTML.css:
            final_css.append('<link href="'+make_media_url('css/'+css)+'" rel="stylesheet" type="text/css"/>')

        for module, arr_css in HeaderHTML.css_local.items():
            
            for css in arr_css:
            
                final_css.append('<link href="'+make_media_url_module('css/'+css, module)+'" rel="stylesheet" type="text/css"/>')

        HeaderHTML.css=[]
        HeaderHTML.css_local={}

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
    
    s['flash']=message
    
    s.save()
    
def show_flash_message():
    
    message=""
    
    s=get_session()
    
    s['flash']=s.get('flash', "")
    
    if s['flash']!="":
        message='<div class="flash">'+s['flash']+'</div>'
    
    s['flash']=''
    
    s.save()
    
    return message
    
standard_t=ptemplate(__file__)
