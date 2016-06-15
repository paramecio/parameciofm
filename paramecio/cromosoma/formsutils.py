#!/usr/bin/python3

from paramecio.cromosoma import corefields
from paramecio.cromosoma.coreforms import PasswordForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.keyutils import create_key_encrypt
from bottle import request

# Need unittest

def pass_values_to_form(post, arr_form, yes_error=True):
    
    for key, value in arr_form.items():
        
        post[key]=post.get(key, '')
        
        #if arr_form[key].default_value=='':
        arr_form[key].default_value=post[key]
        
        if arr_form[key].field==None:
            arr_form[key].field=corefields.CharField(key, 255, required=False) 
        
        # Recheck value if no set error field
        if arr_form[key].field.error == None:
            arr_form[key].field.check(post[key])
        
        arr_form[key].txt_error=""
        
        if arr_form[key].required==True and arr_form[key].field.error==True and yes_error==True:
           arr_form[key].txt_error=arr_form[key].field.txt_error

        # Reset error on field. 

        arr_form[key].field.error=None

    return arr_form
    
class CheckForm():
    
    def __init__(self):
        
        self.error=0

    def check(self, post, arr_form):
        
        for k in arr_form.keys():
            
            post[k]=post.get(k, '')
            
            if arr_form[k].field==None:
               arr_form[k].field=corefields.CharField(k, 255, required=False) 
            
            post[k]=arr_form[k].field.check(post[k])
            arr_form[k].txt_error=arr_form[k].field.txt_error
            
            if arr_form[k].field.error==True and arr_form[k].required==True:
                self.error+=1
        
        return post, arr_form

def show_form(post, arr_form, t, yes_error=True, modelform_tpl='forms/modelform.phtml'):
        
        # Create csrf_token in session
        
        s=get_session()
        
        s['csrf_token']=create_key_encrypt()
        
        if yes_error==True:
            pass_values_to_form(post, arr_form, yes_error)
        
        return t.load_template(modelform_tpl, forms=arr_form)

#Simple Function for add repeat_password form to user model

def set_extra_forms_user(user_admin):
    
    user_admin.fields['password'].required=True
    user_admin.fields['email'].required=True

    user_admin.create_forms(['username', 'email', 'password'])
    
    user_admin.forms['repeat_password']=PasswordForm('repeat_password', '')
    
    user_admin.forms['repeat_password'].required=True
    
    user_admin.forms['repeat_password'].label=I18n.lang('common', 'repeat_password', 'Repeat Password')

#Function for initial values for necessary fields.

def ini_fields(fields):
    pass

def csrf_token():
    
    s=get_session()
    s['csrf_token']=create_key_encrypt()
    
    return '<input type="hidden" name="csrf_token" id="csrf_token" value="'+s['csrf_token']+'" />'

def request_type():
    
    return request.environ['REQUEST_METHOD']
    
