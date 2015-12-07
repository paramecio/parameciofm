#!/usr/bin/python3

from paramecio.modules.admin.models.admin import UserAdmin
from paramecio.citoplasma.urls import make_url
from paramecio.citoplasma.generate_admin_class import GenerateAdminClass
from paramecio.citoplasma.i18n import I18n
from paramecio.cromosoma.coreforms import SelectForm

def admin(t):
    
    user_admin=UserAdmin()
    
    user_admin.fields['privileges'].name_form=SelectForm
    
    user_admin.create_forms(['username', 'password', 'email', 'privileges'])
    
    user_admin.forms['privileges'].arr_select={0: I18n.lang('admin', 'without_privileges', 'Without privileges'), 1: I18n.lang('admin', 'selected_privileges', 'Selected privileges'), 2: I18n.lang('admin', 'administrator', 'Administrator')}
    
    user_admin.fields['password'].protected=False
    
    url=make_url('admin/ausers', {})
    
    admin=GenerateAdminClass(user_admin, url, t)
    
    admin.list.fields_showed=['username', 'privileges']
    
    admin.list.search_fields=['username']
    
    #admin.list.limit_pages=5
    
    return admin.show()