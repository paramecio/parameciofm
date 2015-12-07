from citoplasma.lists import SimpleList
from bottle import request, redirect 
from citoplasma.urls import add_get_parameters
from citoplasma.templates import set_flash_message
from cromosoma.formsutils import show_form
from citoplasma.i18n import I18n
from citoplasma.httputils import GetPostFiles

class GenerateAdminClass:
    
    def __init__(self, model, url, t):
        
        self.model_name=''
        
        self.model=model
        
        self.t=t

        self.list=SimpleList(model, url, t)
        
        self.arr_fields_edit=model.fields.keys()
        
        self.url=url
        
        self.safe=0;
        
        self.arr_links={}
        
        self.hierarchy=None
        
        self.text_add_item=''
        
        self.no_insert=False
        
        self.no_delete=False
        
        self.title=''
        
        self.id=0
        
        self.template_insert='utils/insertform.phtml'
        
        self.template_admin='utils/admin.phtml'

    def show(self):
        
        GetPostFiles.obtain_get()
        
        GetPostFiles.get['op_admin']=GetPostFiles.get.get('op_admin', '0')
        
        GetPostFiles.get['id']=GetPostFiles.get.get('id', '0')
        
        if GetPostFiles.get['op_admin']=='1':
            
            post=None
            
            if len(self.model.forms)==0:
                self.model.create_forms(self.arr_fields_edit)
            
            title_edit=I18n.lang('common', 'add_new_item', 'Add new item')
            
            if GetPostFiles.get['id']!='0':
                post=self.model.select_a_row(GetPostFiles.get['id'])
                title_edit=I18n.lang('common', 'edit_new_item', 'Edit item')
            
            if post==None:
                post={}
            
            form=show_form(post, self.model.forms, self.t, False)
                
            return self.t.load_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=GetPostFiles.get['id'])
        
        elif GetPostFiles.get['op_admin']=='2':
            
            GetPostFiles.obtain_post()
            
            post=GetPostFiles.post
            
            insert_row=self.model.insert
            
            try:
                
                GetPostFiles.get['id']=str(int(GetPostFiles.get['id']))
            
            except:
                
                GetPostFiles.get['id']='0'
            
            title_edit=I18n.lang('common', 'add_new_item', 'Add new item')
                
            
            if GetPostFiles.get['id']!='0':
                insert_row=self.model.update
                title_edit=I18n.lang('common', 'edit_new_item', 'Edit item')
                self.model.conditions=['WHERE `'+self.model.name+'`.`'+self.model.name_field_id+'`=%s', [GetPostFiles.get['id']]]
            
            if insert_row(post):
                set_flash_message(I18n.lang('common', 'task_successful', 'Task successful'))
                redirect(self.url)
            else:

                form=show_form(post, self.model.forms, self.t, True)
                return self.t.load_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=GetPostFiles.get['id'])

            
            pass
            
        elif GetPostFiles.get['op_admin']=='3':
    
            if GetPostFiles.get['id']!='0':
                self.model.conditions=['WHERE `'+self.model.name+'`.`'+self.model.name_field_id+'`=%s', [GetPostFiles.get['id']]]
                self.model.delete()
                set_flash_message(I18n.lang('common', 'task_successful', 'Task successful'))
                redirect(self.url)
    
        else:
            return self.t.load_template(self.template_admin, admin=self)

