#!/usr/bin/env python3

from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma.coreforms import PasswordForm
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.httputils import GetPostFiles

class UserModel(WebModel):
    
    def __init__(self, name_field_id="id"):
        
        super().__init__(name_field_id) 
        
        self.password_field='password'
        self.email_field='email'
        self.username_field='username'
        self.yes_repeat_password=True
        self.check_user=True
    
    def create_forms(self, arr_fields=[]):
        
        # Add password_repeat to forms from the model
        
        arr_fields=super().create_forms(arr_fields)
        
        if self.password_field in arr_fields and self.yes_repeat_password:
            
            repeat_password=PasswordForm('repeat_password', '')
    
            repeat_password.required=1
            
            repeat_password.label=I18n.lang('common', 'repeat_password', 'Repeat Password')
            
            repeat_password.field=self.fields['password']
            
            self.create_form_after(self.password_field, repeat_password)
        
        return arr_fields
            
    """
    def insert(self, dict_values, external_agent=True):
        
        if 'password' in dict_values:
            
            dict_values['repeat_password']=dict_values.get('repeat_password', '')
            
            if dict_values['repeat_password']!=dict_values[self.password_field]:
                self.fields[self.password_field].error=True
                self.fields['password'].txt_error=I18n.lang('common', 'error_passwords_no_match', 'Error: passwords doesn\'t match')
            
            return super().insert(dict_values, external_agent)
    """
    
    def check_all_fields(self, dict_values, external_agent, yes_update=False, errors_set="insert"):
        
        error=0
        
        try:
            
            fields, values, update_values=super().check_all_fields(dict_values, external_agent, yes_update, errors_set)
        except: 
            
            error+=1
        
        if self.check_user==True:
        
            # Check if passwords matches
            
            if self.password_field in dict_values:
                
                dict_values['repeat_password']=dict_values.get('repeat_password', '')
                
                if dict_values[self.password_field].strip()!="":
                
                    if dict_values['repeat_password']!=dict_values[self.password_field]:
                        
                        self.fields[self.password_field].error=True
                        self.fields[self.password_field].txt_error=I18n.lang('common', 'error_passwords_no_match', 'Error: passwords doesn\'t match')
                    
                        error+=1

            # Check if exists user with same email or password
            
            get_id=0
            
            if self.updated:
                # Need the id
                #GetPostFiles.obtain_get()
                #GetPostFiles.obtain_post()
                
                getpostfiles=GetPostFiles()
                
                getpostfiles.obtain_get()
                
                get_id=getpostfiles.get.get(self.name_field_id, '0')
                
                post_id=getpostfiles.post.get(self.name_field_id, '0')
                
                if get_id!='0':
                    get_id=int(get_id)
                
                if post_id!='0':
                    get_id=int(post_id)
                
                pass
            
            get_id=int(get_id)
            
            sql_id=''
            
            original_conditions=self.conditions
            
            self.reset_conditions()
            
            if self.username_field in dict_values:
            
                self.conditions=['WHERE username=%s AND '+self.name_field_id+'!=%s', [dict_values[self.username_field], get_id]]
                
            if self.select_count()>0:
                
                self.fields[self.username_field].error=True
                self.fields[self.username_field].txt_error=I18n.lang('common', 'error_username_exists', 'Error: username exists in database')
                self.fields_errors[self.username_field].append(self.fields[self.username_field].txt_error) 
                error+=1

            
            if self.email_field in dict_values:
            
                self.conditions=['WHERE email=%s AND '+self.name_field_id+'!=%s', [dict_values[self.email_field], get_id]]            
                
            if self.select_count()>0:
                
                self.fields[self.email_field].error=True
                self.fields[self.email_field].txt_error=I18n.lang('common', 'error_email_exists', 'Error: email exists in database')
                self.fields_errors[self.email_field].append(self.fields[self.email_field].txt_error) 
                                
                error+=1
            
            self.conditions=original_conditions
        
        if error>0:
            self.query_error+='Error:if is not expected, please, check that you disabled the special checkings of this model'
            return False

        return fields, values, update_values
        
    
    
    
    
