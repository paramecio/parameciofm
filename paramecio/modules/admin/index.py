#!/usr/bin/python3

import traceback, sys
from paramecio.citoplasma.mtemplates import ptemplate
from paramecio.modules.admin.models.admin import UserAdmin
from paramecio.citoplasma.i18n import load_lang, I18n
from paramecio.citoplasma.urls import make_url, add_get_parameters
from paramecio.citoplasma.sessions import get_session, generate_session
from bottle import get,post,response,request
from settings import config
from settings import config_admin
from paramecio.citoplasma.lists import SimpleList
from paramecio.citoplasma.generate_admin_class import GenerateAdminClass
from paramecio.citoplasma.httputils import GetPostFiles
from paramecio.cromosoma.formsutils import show_form, pass_values_to_form, set_extra_forms_user
from paramecio.cromosoma.coreforms import PasswordForm
from paramecio.cromosoma.webmodel import WebModel
from importlib import import_module, reload
from bottle import redirect
from collections import OrderedDict
from time import time
from paramecio.citoplasma.keyutils import create_key_encrypt
from os import path

#from citoplasma.login import LoginClass
# Check login

load_lang(['paramecio', 'admin'], ['paramecio', 'common'])

key_encrypt=create_key_encrypt()

module_admin=path.dirname(__file__)

t=ptemplate(__file__)

@get('/'+config.admin_folder)
@get('/'+config.admin_folder+'/<module>')
@post('/'+config.admin_folder+'/<module>')
@get('/'+config.admin_folder+'/<module>/<submodule>')
@post('/'+config.admin_folder+'/<module>/<submodule>')
def home(module='', submodule=''):
    
    # A simple boolean used for show or not the code of admin module in standard template
    connection=WebModel.connection()
    ptemplate.show_basic_template=True
    
    if submodule!='':
        module+='/'+submodule
    
    #t.clean_header_cache()
    
    #check if login
    
    user_admin=UserAdmin(connection)
    
    s=get_session()
    
    if 'login' in s:
        
        s['id']=s.get('id', 0)
        
        s['lang']=s.get('lang', None)
        
        lang_selected=None
        
        if s['lang']!=None:
            lang_selected=s['lang']
        else:
            s['lang']=I18n.default_lang
        
        user_admin.conditions=['WHERE id=%s', [s['id']]]
        
        # Check if user id exists in session
        
        c=user_admin.select_count()
        
        if c>0:
        
            if s['privileges']==2:
                
                #Load menu
                
                menu=OrderedDict()
                
                #modules_admin.append([I18n.lang('panel', 'servers_config', 'Server\'s configuration'), [I18n.lang('panel', 'servers_types', 'Server\'s types'), 'modules.panel.admin.types'], 'servers_config'])
                
                for mod in config_admin.modules_admin:
                    if type(mod[1]).__name__!='list':
                        menu[mod[2]]=mod
                    else:
                        
                        menu[mod[2]]=mod[0]
                        
                        for submod in mod[1]:
                            menu[submod[2]]=submod
                            #pass
                        
                if module in menu:
                    
                    #Load module
                    
                    
                    try:
                        new_module=import_module(menu[module][1])
                    
                        if config.reloader:
                            reload(new_module)
                    
                    except ImportError:
                        
                        print("Exception in user code:")
                        print("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        print("-"*60)
                        
                        return "No exists admin module"

                    #args={'t': t, 'connection': connection}

                    content_index=new_module.admin(t=t, connection=connection)

                    if ptemplate.show_basic_template==True:   
                    
                        return t.load_template('admin/content.html', title=menu[module][0], content_index=content_index, menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
                    else:
                        
                        return content_index
                        
                else:
                    return t.load_template('admin/index.html', title=I18n.lang('admin', 'welcome_to_paramecio', 'Welcome to Paramecio Admin!!!'), menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
                
        else:
            
            logout()
            
    else:
        
        user_admin.conditions=['WHERE privileges=%s', [2]]
        
        c=user_admin.select_count()
        
        if c>0:
            
            if request.get_cookie("remember_login", secret=key_encrypt):
            
                 #check login
            
                 token_login=request.get_cookie("remember_login", secret=key_encrypt)
            
                 user_admin.conditions=['WHERE token_login=%s', [token_login]]
    
                 arr_user=user_admin.select_a_row_where(['id', 'privileges'])
                 
                 if arr_user==False:
                     # delete cookioe
                     response.delete_cookie("remember_login")
                 else:
                     s=get_session()
            
                     s['id']=arr_user['id']
                     s['login']=1
                     s['privileges']=arr_user['privileges']
                     
                     redirect('/'+config.admin_folder)
            
            else:
                
                post={}
                
                user_admin.yes_repeat_password=False

                user_admin.fields['password'].required=True
                
                user_admin.create_forms(['username', 'password'])
                
                forms=show_form(post, user_admin.forms, t, yes_error=False)
                
                #connection.close()
                
                return t.load_template('admin/login.phtml', forms=forms)
                
        else:
        
            post={}
            
            set_extra_forms_user(user_admin)
            
            forms=show_form(post, user_admin.forms, t, yes_error=False)

            return t.load_template('admin/register.phtml', forms=forms)

@post('/'+config.admin_folder+'/login')
def login():
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    GetPostFiles.obtain_post()
    
    GetPostFiles.post['username']=GetPostFiles.post.get('username', '')
    GetPostFiles.post['password']=GetPostFiles.post.get('password', '')
    
    username=user_admin.fields['username'].check(GetPostFiles.post['username'])
    
    password=GetPostFiles.post['password'].strip()
    
    user_admin.conditions=['WHERE username=%s', [username]]
    
    arr_user=user_admin.select_a_row_where(['id', 'password', 'privileges', 'lang'])
    
    if arr_user==False:
        
        return {'error': 1}
    else:
        
        if user_admin.fields['password'].verify(password, arr_user['password']):
            
            generate_session()
            
            s=get_session()
            
            s['id']=arr_user['id']
            s['login']=1
            s['privileges']=arr_user['privileges']
            s['lang']=arr_user['lang']
            
            if s['lang']=='':
                s['lang']=I18n.default_lang
            
            remember_login=GetPostFiles.post.get('remember_login', '0')
            
            if remember_login=='1':
                
                timestamp=time()+315360000
                
                random_text=create_key_encrypt()
                
                #Update user with autologin token
                
                user_admin.check_user=False
                
                user_admin.conditions=['WHERE username=%s', [username]]
                
                user_admin.valid_fields=['token_login']
                
                user_admin.reset_require()
                
                if user_admin.update({'token_login': random_text}):
                    
                    response.set_cookie('remember_login', random_text, path="/", expires=timestamp, secret=key_encrypt)
                #else:
                    #print(user_admin.query_error)
            #s.save()
            
            return {'error': 0}
        else:
            return {'error': 1}


@post('/'+config.admin_folder+'/register')
def register():
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    user_admin.conditions=['WHERE privileges=%s', 2]
    
    c=user_admin.select_count()
    
    if c==0:
        
        GetPostFiles.obtain_post()
        
        GetPostFiles.post['privileges']=2
        
        user_admin.valid_fields=['username', 'email', 'password', 'privileges']
        
        user_admin.create_forms()
        
        if user_admin.insert(GetPostFiles.post, False):
        
            error= {'error': 0}
            
            return error
        
        else:
            
            user_admin.check_all_fields(GetPostFiles.post, False)
            
            pass_values_to_form(GetPostFiles.post, user_admin.forms, yes_error=True)
            
            error={'error': 1}
            
            for field in user_admin.fields.values():
                    
                    error[field.name]=field.txt_error
            
            #error['password_repeat']=I18n.lang('common', 'password_no_match', 'Passwords doesn\'t match')
            
            return error
        
    else:
    
        return {'error': 1}
        
@get('/'+config.admin_folder+'/logout')
def logout():
    
    s=get_session()
    
    if 'login' in s.keys():
    
        del s['login']
        del s['privileges']
        
        #s.save()
    
    s.remove()
    
    if request.get_cookie("remember_login", secret=key_encrypt):
           
        # delete cookie
        response.delete_cookie("remember_login", path="/")
    
    #return ""
    
    redirect('/'+config.admin_folder)
    
"""
def set_extra_forms_user(user_admin):
    
    user_admin.fields['password'].required=True
    user_admin.fields['email'].required=True

    user_admin.create_forms(['username', 'email', 'password'])
    
    user_admin.forms['repeat_password']=PasswordForm('repeat_password', '')
    
    user_admin.forms['repeat_password'].required=1
    
    user_admin.forms['repeat_password'].label=I18n.lang('common', 'repeat_password', 'Repeat Password')
"""


"""user_admin.create_forms()
    
    users=user_admin.select()"""

#By default id is not showed
