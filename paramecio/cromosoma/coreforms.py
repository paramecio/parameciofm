#!/usr/bin/python3

from collections import OrderedDict

#Forms para python3

class BaseForm:
    
    def __init__(self, name, value):
        
        self.label=name
        self.name=name
        self.default_value=value
        self.css=''
        self.type='text'
        self.field=None
        self.required=False
        self.txt_error=''
        
    def form(self):
        
        return '<input type="'+self.type+'" class="'+self.css+'" name="'+self.name+'" id="'+self.name+'_form" value="'+self.setform(self.default_value)+'">'
    
    def show_formatted(self, value):
    
        return value
    
    #Method for escape value for html input. DON'T CHANGE IF YOU DON'T KNOWN WHAT ARE YOU DOING
    
    def setform(self, value):
        
        value=str(value)
        
        return value.replace('"', '&quot;')

class TextForm(BaseForm):
    
    def __init__(self, name, value):
        super(TextForm, self).__init__(name, value)

class PasswordForm(BaseForm):
    
    def __init__(self, name, value):
        super(PasswordForm, self).__init__(name, value)
        self.type='password'
        
    def setform(self, value):
        return ""

class HiddenForm(BaseForm):
    
    def __init__(self, name, value):
        super(HiddenForm, self).__init__(name, value)
        self.type='hidden'


class SelectForm(BaseForm):
    
    def __init__(self, name, value):
        super(SelectForm, self).__init__(name, value)
        self.arr_select=OrderedDict()
    
    def form(self):
        
        the_form='<select name="'+self.name+'">\n'
        
        arr_selected={self.default_value: 'selected'}
        
        for k,v in self.arr_select.items():
            arr_selected[k]=arr_selected.get(k, '')
            the_form+="<option value=\""+str(k)+"\" "+arr_selected[k]+">"+v+"</option>"
        
        the_form+='</select>\n'
        
        return the_form
    