#!/usr/bin/env python3

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
        self.name_field_id=self.name+'_form'
        self.help=''
        
    def form(self):
        
        return '<input type="'+self.type+'" class="'+self.css+'" name="'+self.name+'" id="'+self.name_field_id+'" value="'+self.setform(self.default_value)+'" />'
    
    def show_formatted(self, value):
    
        return value
    
    #Method for escape value for html input. DON'T CHANGE IF YOU DON'T KNOWN WHAT ARE YOU DOING
    
    def setform(self, value):
        
        value=str(value)
        
        return value.replace('"', '&quot;').replace("'", '&#39;')
    
    def change_name(self, new_name):
        
        self.name=new_name

        self.name_field_id=self.name+'_form'

        return ""

class SimpleTextForm(BaseForm):
    
    def __init__(self, name, value):
        super().__init__(name, value)
        
        self.after_text=''
    
    def form(self):
        
        return super().form()+' '+self.after_text

class TextForm(BaseForm):
    
    def __init__(self, name, value):
        super(TextForm, self).__init__(name, value)
        
    def form(self):
        
        return '<textarea class="'+self.css+'" name="'+self.name+'" id="'+self.name+'_form">'+self.setform(self.default_value)+'</textarea>'

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
    
    def __init__(self, name, value, elements=OrderedDict()):
        super(SelectForm, self).__init__(name, value)
        self.arr_select=elements
    
    def form(self):
        
        the_form='<select name="'+self.name+'" id="'+self.name_field_id+'">\n'
        
        arr_selected={self.default_value: 'selected'}
        
        for k,v in self.arr_select.items():
            arr_selected[k]=arr_selected.get(k, '')
            
            the_form+="<option value=\""+self.setform(str(k))+"\" "+arr_selected[k]+">"+self.setform(str(v))+"</option>"
        
        the_form+='</select>\n'
        
        return the_form

class SelectModelForm(SelectForm):
    
    def __init__(self, name, value, model, field_name, field_value, field_parent=None):
        super(SelectModelForm, self).__init__(name, value)
        
        try:
            self.default_value=int(self.default_value)
        except:
            self.default_value=0
            
        self.arr_select=OrderedDict()
        self.model=model
        self.field_name=field_name
        self.field_value=field_value
        self.field_parent=field_parent
        
        self.form=self.normal_form
        
        if self.field_parent!=None:
            self.form=self.parent_form
        
        
    def normal_form(self):
        
        self.arr_select['']=''
        
        with self.model.select([self.field_name, self.field_value], True) as cur:        
            for arr_value in cur:
                
                self.arr_select[arr_value[self.field_value]]=arr_value[self.field_name]
                
            try:
            
                self.default_value=int(self.default_value)
                
            except:
                self.default_value=0
        
        return super().form()
        
    def parent_form(self):
        
        self.arr_select['']=''
        
        arr_son={}
        
        old_conditions=self.model.conditions
        old_limit=self.model.limit
        
        self.model.limit=''
        
        self.model.set_conditions('WHERE 1=1', [])
        
        
        with self.model.select([self.field_name, self.field_value, self.field_parent], True) as cur:
        
            for arr_value in cur:
                
                if not arr_value[self.field_parent] in arr_son:
                    
                    arr_son[arr_value[self.field_parent]]=[]
                
                arr_son[arr_value[self.field_parent]].append([arr_value[self.field_value], arr_value[self.field_name]])
        
        self.create_son(0, arr_son)
        
        self.model.conditions=old_conditions
        self.model.limit=old_limit
        
        try:
        
            self.default_value=int(self.default_value)
            
        except:
            self.default_value=0
        
        return super().form()
        

    def create_son(self, parent_id, arr_son, separator=''):
        
        if parent_id in arr_son:        
            for son in arr_son[parent_id]:
                self.arr_select[son[0]]=separator+son[1]
                
                son_separator=separator
                
                if son[0] in arr_son:    
                    son_separator+='--'
                    self.create_son(son[0],arr_son, son_separator)
