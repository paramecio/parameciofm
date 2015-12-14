#!/usr/bin/python3

from paramecio.citoplasma.mtemplates import ptemplate
from paramecio.modules.admin.models.admin import UserAdmin
from paramecio.citoplasma.i18n import load_lang, I18n
from paramecio.citoplasma.urls import make_url, add_get_parameters
from paramecio.citoplasma.sessions import get_session
from bottle import get,post,response,request
from settings import config
from settings import config_admin
from paramecio.citoplasma.lists import SimpleList
from paramecio.citoplasma.generate_admin_class import GenerateAdminClass
from paramecio.citoplasma.httputils import GetPostFiles
from paramecio.cromosoma.formsutils import show_form, pass_values_to_form
from paramecio.cromosoma.coreforms import PasswordForm
from importlib import import_module, reload
from bottle import redirect
from collections import OrderedDict
from time import time
from hashlib import sha512
from os import urandom, path

#from citoplasma.login import LoginClass
# Check login

def create_key_encrypt():
    
    return sha512(urandom(10)).hexdigest()

key_encrypt=create_key_encrypt()

module_admin=path.dirname(__file__)

t=ptemplate(__file__)

load_lang(['paramecio', 'admin'], ['paramecio', 'common'])

@get('/'+config.admin_folder)
@get('/'+config.admin_folder+'/<module>')
@post('/'+config.admin_folder+'/<module>')
def home(module=''):
    
    t.clean_header_cache()
    
    #check if login
    
    user_admin=UserAdmin()
    
    s=get_session()
    
    if 'login' in s:
        
        s['id']=s.get('id', 0)
        
        user_admin.conditions=['WHERE id=%s', [s['id']]]
        
        # Check if user id exists in session
        
        c=user_admin.select_count()
        
        if c>0:
        
            if s['privileges']==2:
                
                #Load menu
                
                menu=OrderedDict()
                
                for key, mod in config_admin.modules_admin.items():
                    if type(mod[1]).__name__!='dict':
                        menu[key]=mod
                    else:
                        menu[key]=mod[0]
                        
                        for subkey, submod in mod[1].items():
                            menu[subkey]=submod
                            #pass
                        
                if module in menu:
                    
                    #Load module
                    
                    new_module=import_module(menu[module][1])
                    
                    if config.reloader:
                        reload(new_module)
                    
                    return t.load_template('admin/content.html', title=menu[module][0], content_index=new_module.admin(t), menu=menu)
                    
                else:
                    return t.load_template('admin/index.html', title=I18n.lang('admin', 'welcome_to_paramecio', 'Welcome to Paramecio Admin!!!'), menu=menu)
                
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
                
                return t.load_template('admin/login.phtml', forms=forms)
                
        else:
        
            post={}
            
            set_extra_forms_user(user_admin)
            
            forms=show_form(post, user_admin.forms, t, yes_error=False)

            return t.load_template('admin/register.phtml', forms=forms)

@post('/'+config.admin_folder+'/login')
def login():
    
    user_admin=UserAdmin()
    
    GetPostFiles.obtain_post()
    
    GetPostFiles.post['username']=GetPostFiles.post.get('username', '')
    GetPostFiles.post['password']=GetPostFiles.post.get('password', '')
    
    username=user_admin.fields['username'].check(GetPostFiles.post['username'])
    
    password=GetPostFiles.post['password'].strip()
    
    user_admin.conditions=['WHERE username=%s', [username]]
    
    arr_user=user_admin.select_a_row_where(['id', 'password', 'privileges'])
    
    if arr_user==False:
        
        return {'error': 1}
    else:
        
        if user_admin.fields['password'].verify(password, arr_user['password']):
            
            s=get_session()
            
            s['id']=arr_user['id']
            s['login']=1
            s['privileges']=arr_user['privileges']
            
            remember_login=GetPostFiles.post.get('remember_login', '0')
            
            if remember_login=='1':
                
                timestamp=time()+315360000
                
                random_text=sha512(urandom(10)).hexdigest()
                
                #Update user with autologin token
                
                user_admin.check_user=False
                
                user_admin.conditions=['WHERE username=%s', [username]]
                
                user_admin.valid_fields=['token_login']
                
                user_admin.reset_require()
                
                if user_admin.update({'token_login': random_text}):
                    
                    response.set_cookie('remember_login', random_text, expires=timestamp, secret=key_encrypt)
                #else:
                    #print(user_admin.query_error)
            
            
            return {'error': 0}
        else:
            return {'error': 1}


@post('/'+config.admin_folder+'/register')
def register():
    
    user_admin=UserAdmin()
    
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
    
    if request.get_cookie("remember_login", secret=key_encrypt):
           
        # delete cookie
        response.delete_cookie("remember_login")
    
    redirect('/'+config.admin_folder)
    

def set_extra_forms_user(user_admin):
    
    user_admin.fields['password'].required=True
    user_admin.fields['email'].required=True

    user_admin.create_forms(['username', 'email', 'password'])
    
    user_admin.forms['repeat_password']=PasswordForm('repeat_password', '')
    
    user_admin.forms['repeat_password'].required=1
    
    user_admin.forms['repeat_password'].label=I18n.lang('common', 'repeat_password', 'Repeat Password')



    """user_admin.create_forms()
    
    users=user_admin.select()"""

#By default id is not showed
