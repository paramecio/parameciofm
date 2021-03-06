#!/usr/bin/env python3

from paramecio.citoplasma.i18n import I18n
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma.usermodel import UserModel
from paramecio.cromosoma import corefields
from paramecio.cromosoma.extrafields.emailfield import EmailField
from paramecio.cromosoma.extrafields.passwordfield import PasswordField
from paramecio.cromosoma.extrafields.langfield import LangField

class PrivilegesField(corefields.IntegerField):

    def show_formatted(self, value):
        
        value=int(value)
        
        if value==0:
            return I18n.lang('admin', 'without_privileges', 'Without privileges')
        elif value==1:
            return I18n.lang('admin', 'selected_privileges', 'Selected privileges')
        elif value==2:
            return I18n.lang('admin', 'administrator', 'Administrator')

_username=corefields.CharField('username')
_password=PasswordField('password')
_email=EmailField('email')
_token_recovery=corefields.CharField('token_recovery')
_token_login=corefields.CharField('token_login')
_privileges=PrivilegesField('privileges')
_lang=LangField('lang', 20)
_disabled=corefields.BooleanField('disabled')
_num_tries=corefields.IntegerField('num_tries', 1)

class UserAdmin(UserModel):
    
    #def create_fields(self):
    def __init__(self, connection=None):

        super().__init__(connection)

        # I can change other fields here, how the name.
        """
        self.register(_username)
        
        self.fields['username'].required=True
        
        self.register(_password)

        self.fields['password'].required=True
        
        self.register(_email)

        self.fields['email'].required=True
        
        self.register(_token_recovery)

        self.register(_token_login)
        
        self.register(_privileges)
        
        self.register(_lang)
        
        self.register(_disabled)
        
        self.register(_num_tries)
        """
        
        self.register(corefields.CharField('username'))
        
        self.fields['username'].required=True
        
        self.register(PasswordField('password'))

        self.fields['password'].required=True
        
        self.register(EmailField('email'))

        self.fields['email'].required=True
        
        self.register(corefields.CharField('token_recovery'))

        self.register(corefields.CharField('token_login'))
        
        self.register(PrivilegesField('privileges'))
        
        self.register(LangField('lang', 20))
        
        self.register(corefields.BooleanField('disabled'))
        
        self.register(corefields.IntegerField('num_tries', 1))
        
"""

user_admin=WebModel('user_admin')

user_admin.register(corefields.CharField('username'))

user_admin.fields['username'].required=True

user_admin.register(corefields.CharField('password'))

user_admin.fields['password'].required=True

user_admin.register(EmailField('email'))

user_admin.fields['email'].required=True

user_admin.register(corefields.CharField('token_recovery'))

user_admin.register(corefields.BooleanField('privileges'))

#user_admin.register(corefields.CharField('prueba'))

"""
