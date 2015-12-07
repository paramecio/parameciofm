#!/usr/bin/python3

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
    
    def create_forms(self, arr_fields={}):
        
        # Add password_repeat to forms from the model
        
        super().create_forms(arr_fields)
        
        if self.password_field in arr_fields and self.yes_repeat_password:
            
            repeat_password=PasswordForm('repeat_password', '')
    
            repeat_password.required=1
            
            repeat_password.label=I18n.lang('common', 'repeat_password', 'Repeat Password')
            
            self.create_form_after(self.password_field, repeat_password)
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
        
        try:
            
            fields, values, update_values=super().check_all_fields(dict_values, external_agent, yes_update, errors_set)
        except: 
            
            return False
        
        # Check if passwords matches
        
        if self.password_field in dict_values:
            
            dict_values['repeat_password']=dict_values.get('repeat_password', '')
            
            if dict_values['repeat_password']!=dict_values[self.password_field]:
                
                if dict_values[self.password_field].strip()!="":
                    
                    self.fields[self.password_field].error=True
                    self.fields[self.password_field].txt_error=I18n.lang('common', 'error_passwords_no_match', 'Error: passwords doesn\'t match')
                
                return False

        # Check if exists user with same email or password
        
        get_id=0
        
        if self.updated:
            # Need the id
            GetPostFiles.obtain_get()
            GetPostFiles.obtain_post()
            
            get_id=GetPostFiles.get.get(self.name_field_id, '0')
            
            post_id=GetPostFiles.post.get(self.name_field_id, '0')
            
            if get_id!='0':
                get_id=int(get_id)
            
            if post_id!='0':
                get_id=int(post_id)
            
            pass
        
        sql_id=''
        
        original_conditions=self.conditions
        
        self.reset_conditions()
        
        if self.username_field in dict_values:
        
            self.conditions=['WHERE username=%s', [dict_values[self.username_field]]]

        
        if self.email_field in dict_values:
        
            if len(self.conditions[1])>0:
        
                self.conditions[0]+=' OR email=%s'
            else:
                self.conditions[0]='WHERE email=%s'
                self.conditions[1]=[]
        
            self.conditions[1].append([dict_values[self.email_field]])
        
        if get_id>0:
            self.conditions[0]=' AND '+self.username_field+'=%s'
            self.conditions[1].append(get_id)
            
        
        if self.select_count()>0:
            
            self.fields[self.username_field].error=True
            self.fields[self.username_field].txt_error=I18n.lang('common', 'error_username_or_password_exists', 'Error: username or email exists in database')
            
            return False
        
        self.conditions=original_conditions

        return fields, values, update_values
        
    
    
    
    