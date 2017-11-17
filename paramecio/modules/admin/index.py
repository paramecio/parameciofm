#!/usr/bin/env python3

import traceback, sys
from paramecio.citoplasma.mtemplates import env_theme, PTemplate
from paramecio.modules.admin.models.admin import UserAdmin
from paramecio.citoplasma.i18n import load_lang, I18n
from paramecio.citoplasma.urls import make_url, add_get_parameters, redirect
from paramecio.citoplasma.sessions import get_session, generate_session
from bottle import get,post,response,request
from settings import config
from settings import config_admin
from paramecio.citoplasma.adminutils import get_menu, get_language, make_admin_url, check_login
from paramecio.citoplasma.httputils import GetPostFiles
from paramecio.cromosoma.formsutils import show_form, pass_values_to_form, set_extra_forms_user
from paramecio.cromosoma.coreforms import PasswordForm
from paramecio.cromosoma.webmodel import WebModel
from importlib import import_module, reload
from collections import OrderedDict
from time import time
from paramecio.citoplasma.keyutils import create_key_encrypt, create_key_encrypt_256, create_key
from paramecio.citoplasma.sendmail import SendMail
from os import path
from paramecio.wsgiapp import app
import copy
from paramecio.i18n import admin

#from citoplasma.login import LoginClass
# Check login

yes_recovery_login=False
email_address='localhost'

if hasattr(config, 'yes_recovery_login'):
    yes_recovery_login=config.yes_recovery_login

if hasattr(config, 'email_address'):
    email_address=config.email_address

#load_lang(['paramecio', 'admin'], ['paramecio', 'common'])


key_encrypt=config.key_encrypt #create_key_encrypt()

module_admin=path.dirname(__file__)

env=env_theme(__file__)

# Preload modules

#Load menu
                
menu=get_menu(config_admin.modules_admin)

module_imported={}

for k, v in menu.items():
    if type(v).__name__=='list':
        if k[:1]!='/':
            module_imported[k]=import_module(v[1])

#print(d)

@app.get('/'+config.admin_folder)
@app.get('/'+config.admin_folder+'/<module>')
@app.post('/'+config.admin_folder+'/<module>')
@app.get('/'+config.admin_folder+'/<module>/<submodule>')
@app.post('/'+config.admin_folder+'/<module>/<submodule>')
def home(module='', submodule=''):
    
    # A simple boolean used for show or not the code of admin module in standard template
    
    connection=WebModel.connection()
    user_admin=UserAdmin(connection)
    
    #Fix, make local variable
    
    t=PTemplate(env)
    
    t.add_filter(make_admin_url)
    
    t.show_basic_template=True
    
    if submodule!='':
        module+='/'+submodule
    
    #t.clean_header_cache()
    
    #check if login
    
    s=get_session()
    
    if check_login():
        
        s['id']=s.get('id', 0)
        
        lang_selected=get_language(s)
        
        user_admin.set_conditions('WHERE id=%s', [s['id']])
        
        # Check if user id exists in session
        
        c=user_admin.select_count()
        
        if c>0:
            
            if s['privileges']==2:
                            #pass
                
                if module in menu:
                    
                    #Load module
                    
                    
                    try:
                        #new_module=import_module(menu[module][1])
                        
                        #t.inject_folder=path.dirname(new_module.__file__).replace('/admin', '')
                        
                        #t.env=t.env_theme(path.dirname(__file__))
                        
                        t.env.directories.insert(1, path.dirname(module_imported[module].__file__).replace('/admin', '')+'/templates')
                        #print(t.env.directories)
                        #if config.reloader:
                            #reload(new_module)
                    
                    except ImportError:
                        
                        print("Exception in user code:")
                        print("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        print("-"*60)
                        
                        return "No exists admin module"
                    
                    #args={'t': t, 'connection': connection}

                    content_index=module_imported[module].admin(t=t, connection=connection)

                    if t.show_basic_template==True:   
                        
                        title_module=menu[module][0]
                        
                        if type(content_index).__name__=='list':
                            title_module=content_index[0]
                            content_index=content_index[1]
                        connection.close()
                        return t.load_template('admin/content.html', title=title_module, content_index=content_index, menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
                    else:
                        
                        connection.close()
                        
                        return content_index
                        
                else:
                    connection.close()
                    
                    return t.load_template('admin/index.html', title=I18n.lang('admin', 'welcome_to_paramecio', 'Welcome to Paramecio Admin!!!'), menu=menu, lang_selected=lang_selected, arr_i18n=I18n.dict_i18n)
                    
            connection.close()    
            return ""
                
        else:
            
            logout()
        
        connection.close()
        
        return ""
            
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
                     connection.close()
                     response.delete_cookie("remember_login")
                 else:
                     s=get_session()
            
                     s['id']=arr_user['id']
                     s['login']=1
                     s['privileges']=arr_user['privileges']
                     
                     s.save()
                     
                     connection.close()
                     
                     redirect(make_url(config.admin_folder))
            
            else:
                
                post={}
                
                user_admin.yes_repeat_password=False

                user_admin.fields['password'].required=True
                
                user_admin.create_forms(['username', 'password'])
                
                forms=show_form(post, user_admin.forms, t, yes_error=False)
                
                connection.close()
                
                return t.load_template('admin/login.phtml', forms=forms, yes_recovery_login=yes_recovery_login)
                
        else:
        
            post={}
            
            set_extra_forms_user(user_admin)
            
            forms=show_form(post, user_admin.forms, t, yes_error=False)
            
            connection.close()

            return t.load_template('admin/register.phtml', forms=forms)
    
    connection.close()
    
    return ""
    
@app.post('/'+config.admin_folder+'/login')
def login():
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    getpostfiles=GetPostFiles()
    
    getpostfiles.obtain_post()
    
    getpostfiles.post['username']=getpostfiles.post.get('username', '')
    getpostfiles.post['password']=getpostfiles.post.get('password', '')
    
    username=user_admin.fields['username'].check(getpostfiles.post['username'])
    
    password=getpostfiles.post['password'].strip()
    
    user_admin.conditions=['WHERE username=%s', [username]]
    
    arr_user=user_admin.select_a_row_where(['id', 'password', 'privileges', 'lang', 'num_tries'])
    
    if arr_user==False:
        
        s=get_session()
                
        s['csrf_token']=create_key_encrypt()
        
        s.save()
        connection.close()
        return {'error': 1, 'csrf_token': s['csrf_token']}
    else:
        
        num_tries=int(arr_user['num_tries'])
        
        if arr_user['num_tries']<3:
        
            if user_admin.fields['password'].verify(password, arr_user['password']):
                
                s=get_session()
                
                s['id']=arr_user['id']
                s['login']=1
                s['privileges']=arr_user['privileges']
                s['lang']=arr_user['lang']
                
                if s['lang']=='':
                    s['lang']=I18n.default_lang
                
                remember_login=getpostfiles.post.get('remember_login', '0')
                
                if remember_login=='1':
                    
                    timestamp=time()+315360000
                    
                    random_text=create_key_encrypt()
                    
                    #Update user with autologin token
                    
                    user_admin.check_user=False
                    
                    user_admin.conditions=['WHERE username=%s', [username]]
                    
                    user_admin.valid_fields=['token_login']
                    
                    user_admin.reset_require()
                    
                    if user_admin.update({'token_login': random_text}):
                        
                        response.set_cookie('remember_login', random_text, path=config.session_opts['session.path'], expires=timestamp, secret=key_encrypt)
                    #else:
                        #print(user_admin.query_error)
                s.save()
                
                connection.close()
                
                return {'error': 0}
            else:
                
                user_admin.check_user=False
                    
                user_admin.conditions=['WHERE username=%s', [username]]
                
                user_admin.valid_fields=['num_tries']
                
                user_admin.reset_require()
                
                user_admin.update({'num_tries': arr_user['num_tries']+1})
                
                s=get_session()
                
                s['csrf_token']=create_key_encrypt()
                
                s.save()
                
                connection.close()
                
                return {'error': 1, 'csrf_token': s['csrf_token']}
        else:
            s=get_session()
                
            s['csrf_token']=create_key_encrypt()
            
            s.save()
            
            connection.close()
            
            return {'error': 1, 'csrf_token': s['csrf_token']}


@app.post('/'+config.admin_folder+'/register')
def register():
    
    getpostfiles=GetPostFiles()
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    user_admin.conditions=['WHERE privileges=%s', [2]]
    
    c=user_admin.select_count()
    
    if c==0:
        
        getpostfiles.obtain_post()
        
        getpostfiles.post['privileges']=2
        
        user_admin.valid_fields=['username', 'email', 'password', 'privileges']
        
        user_admin.create_forms()
        
        if user_admin.insert(getpostfiles.post, False):
        
            error= {'error': 0}
            connection.close()
            return error
        
        else:
            
            user_admin.check_all_fields(getpostfiles.post, False)
            
            pass_values_to_form(getpostfiles.post, user_admin.forms, yes_error=True)
            
            s=get_session()
                
            s['csrf_token']=create_key_encrypt()
            
            error={'error': 1, 'csrf_token': s['csrf_token']}
            
            for field in user_admin.valid_fields:
                    
                    error[field]=user_admin.forms[field].txt_error
            
            error['repeat_password']=user_admin.forms['repeat_password'].txt_error
            
            #error['password_repeat']=I18n.lang('common', 'password_no_match', 'Passwords doesn\'t match')
            
            s.save()
            
            connection.close()
            
            return error
        
    else:
        
        connection.close()
        
        return {'error': 1}
        
@app.get('/'+config.admin_folder+'/logout')
def logout():
    
    s=get_session()
    
    if 'login' in s.keys():
    
        del s['login']
        del s['privileges']
        
        s.save()
    
    s.delete()
    
    if request.get_cookie("remember_login", secret=key_encrypt):
           
        # delete cookie
        response.delete_cookie("remember_login", path="/")
    
    #return ""
    
    redirect(make_url(config.admin_folder))

@app.get('/'+config.admin_folder+'/recovery_password')
def recovery_password():
    
    t=PTemplate(env)
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    post={}
    
    user_admin.create_forms(['email'])
    
    forms=show_form(post, user_admin.forms, t, yes_error=False)
    
    #connection.close()
    connection.close()
    return t.load_template('admin/recovery.phtml', forms=forms)

@app.post('/'+config.admin_folder+'/recovery_password')
def send_password():
    
    connection=WebModel.connection()
    
    user_admin=UserAdmin(connection)
    
    t=PTemplate(env)
    
    getpost=GetPostFiles()
    
    getpost.obtain_post()
    
    email=getpost.post.get('email',  '')
    
    email=user_admin.fields['email'].check(email)
    
    if user_admin.fields['email'].error:
        
        s=get_session()
                
        s['csrf_token']=create_key_encrypt()
        
        s.save()
        connection.close()
        return {'email': user_admin.fields['email'].txt_error, 'error': 1, 'csrf_token': s['csrf_token']}
        
    else:
        
        user_admin.set_conditions('WHERE email=%s', [email])
        
        user_admin.yes_reset_conditions=False
        
        if user_admin.select_count()==1:
            
            user_admin.reset_require()
            
            user_admin.valid_fields=['token_recovery']
            
            user_admin.check_user=False
            
            token=create_key_encrypt_256()
            
            if user_admin.update({'token_recovery': token}):
                
                send_mail=SendMail()
                
                content_mail=t.load_template('admin/recovery_mail.phtml', token=token)
                
                if not send_mail.send(email_address, [email], I18n.lang('admin', 'send_email', 'Email for recovery your password'), content_mail):
                    return {'email': 'Error: i cannot send mail', 'error': 1}
                
        connection.close()
        
        return {'email': '', 'error': 0}
        
        
@app.get('/'+config.admin_folder+'/check_token')
def check_token():
    t=PTemplate(env)
    
    return t.load_template('admin/check_token.phtml')
    
@app.post('/'+config.admin_folder+'/check_token')
def check_code_token():
    
    t=PTemplate(env)
    
    if yes_recovery_login==True:
    
        getpost=GetPostFiles()
        
        getpost.obtain_post()
        
        connection=WebModel.connection()
    
        user_admin=UserAdmin(connection)
        
        token=getpost.post.get('token',  '')
        
        token=user_admin.fields['token_recovery'].check(token)
    
        if token.strip()!='':
            
            user_admin.set_conditions('WHERE token_recovery=%s', [token])
            
            user_admin.yes_reset_conditions=False
            
            arr_user=user_admin.select_a_row_where(['id', 'email'])
            
            if arr_user:
                
                new_password=create_key()
                           
                user_admin.valid_fields=['password', 'token_recovery', 'num_tries']

                user_admin.reset_require()
                
                user_admin.check_user=False
                
                if user_admin.update({'password': new_password, 'token_recovery': "", 'num_tries': 0}, False):
                    
                    send_mail=SendMail()
                    
                    content_mail=t.load_template('admin/recovery_password.phtml', password=new_password)
                    
                    if not send_mail.send(email_address, [arr_user['email']], I18n.lang('admin', 'send_password_email', 'Your new password'), content_mail):
                        return {'token': 'Error: i cannot send mail', 'error': 1}
                    
                    return {'token': 'Error: cannot send the maild with the new password', 'error': 0} 
    
    s=get_session()
                
    s['csrf_token']=create_key_encrypt()
    
    s.save()
    
    return {'token': 'Error: token is not valid', 'error': 1,  'csrf_token': s['csrf_token']}
