from paramecio.citoplasma.lists import SimpleList
from bottle import request
from paramecio.citoplasma.urls import add_get_parameters, redirect
from paramecio.citoplasma.mtemplates import set_flash_message
from paramecio.cromosoma.formsutils import show_form
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.httputils import GetPostFiles
from collections import OrderedDict

class GenerateAdminClass:
    
    def __init__(self, model, url, t):
        
        self.model_name=''
        
        self.model=model
        
        self.t=t

        self.list=SimpleList(model, url, t)
        
        self.arr_fields_edit=list(model.fields.keys())
        
        del self.arr_fields_edit[self.arr_fields_edit.index(model.name_field_id)]
        
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
        
        self.template_verify_delete='utils/verify_delete.phtml'

    def show(self):
        
        getpostfiles=GetPostFiles()
        
        getpostfiles.obtain_get()
        
        getpostfiles.get['op_admin']=getpostfiles.get.get('op_admin', '0')
        
        getpostfiles.get['id']=getpostfiles.get.get('id', '0')
        
        if len(self.model.forms)==0:

            self.model.create_forms()
        
        edit_forms=OrderedDict()
        
        url_action=self.url
        
        for key_form in self.arr_fields_edit:
            edit_forms[key_form]=self.model.forms[key_form]
        
        if getpostfiles.get['op_admin']=='1':
            
            post=None
            
            title_edit=I18n.lang('common', 'add_new_item', 'Add new item')
            
            if getpostfiles.get['id']!='0':
                post=self.model.select_a_row(getpostfiles.get['id'], [], True)
                title_edit=I18n.lang('common', 'edit_new_item', 'Edit item')
            
            if post==None or post==False:
                
                if getpostfiles.get['id']=='0':
                    post={}
                else:
                    return ""
            
            url_action=add_get_parameters(self.url, op_admin=2, id=getpostfiles.get['id'])
            
            form=show_form(post, edit_forms, self.t, False)
                
            return self.t.render_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=getpostfiles.get['id'], url_action=url_action)
        
        elif getpostfiles.get['op_admin']=='2':
            
            getpostfiles.obtain_post()
            
            #post=getpostfiles.post
            
            self.model.reset_conditions()
            
            insert_row=self.model.insert
            
            try:
                
                getpostfiles.get['id']=str(int(getpostfiles.get['id']))
            
            except:
                
                getpostfiles.get['id']='0'
            
            title_edit=I18n.lang('common', 'add_new_item', 'Add new item')
                
            
            if getpostfiles.get['id']!='0':
                insert_row=self.model.update
                title_edit=I18n.lang('common', 'edit_new_item', 'Edit item')
                self.model.conditions=['WHERE `'+self.model.name+'`.`'+self.model.name_field_id+'`=%s', [getpostfiles.get['id']]]
            
            if insert_row(getpostfiles.post):
                set_flash_message(I18n.lang('common', 'task_successful', 'Task successful'))
                redirect(self.url)
            else:
                url_action=add_get_parameters(self.url, op_admin=2, id=getpostfiles.get['id'])
                
                form=show_form(getpostfiles.post, edit_forms, self.t, True)
                return self.t.render_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=getpostfiles.get['id'], url_action=url_action)

            
            pass
            
        elif getpostfiles.get['op_admin']=='3':
            
            verified=getpostfiles.get.get('verified', '0')
            
            if verified=='1':
    
                if getpostfiles.get['id']!='0':
                    self.model.conditions=['WHERE `'+self.model.name+'`.`'+self.model.name_field_id+'`=%s', [getpostfiles.get['id']]]
                    self.model.delete()
                    set_flash_message(I18n.lang('common', 'task_successful', 'Task successful'))
                    redirect(self.url)
    
            else:
                
                return self.t.render_template(self.template_verify_delete, url=self.url, item_id=getpostfiles.get['id'], op_admin=3, verified=1)
    
        else:
            return self.t.render_template(self.template_admin, admin=self)

    """
    def show_config(self):
        
        
        getpostfiles=GetPostFiles()
        
        getpostfiles.obtain_query()        
        
        op=getpostfiles.query.get('op', '')
        
        object_id=getpostfiles.query.get('id', '0')
        
        c=self.model.select_count
        
        if op=='':
            
            # Show the form
            

            
            return self.t.render_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=object_id)            
            
    """

class GenerateConfigClass:
    
    def __init__(self, model, url, t):

        self.model_name=''
        
        self.model=model
        
        self.title_name=model.label
        
        self.t=t
        
        self.url=url
        
        self.arr_fields_edit=list(model.fields.keys())

        del self.arr_fields_edit[self.arr_fields_edit.index(model.name_field_id)]
        
        self.template_insert='utils/insertform.phtml'

    def show(self):
        
        getpostfiles=GetPostFiles()
        
        getpostfiles.obtain_query()
        
        getpostfiles.query['op_config']=getpostfiles.query.get('op_config', '0')
        
        if len(self.model.forms)==0:

            self.model.create_forms()

        title_edit=I18n.lang('common', 'edit', 'Edit')+' '+self.title_name

        edit_forms=OrderedDict()

        form_values={}
            
        for key_form in self.arr_fields_edit:
            edit_forms[key_form]=self.model.forms[key_form]

        url_action=add_get_parameters(self.url, op_config=1)
    
        if getpostfiles.query['op_config']=='1':
            
            getpostfiles.obtain_post()
            
            c=self.model.select_count()

            insert_model=self.model.insert
            
            if c:
                insert_model=self.model.update

            if insert_model(getpostfiles.post):
                set_flash_message(I18n.lang('common', 'task_successful', 'Task successful'))
                redirect(self.url)
            else:

                form=show_form(getpostfiles.post, edit_forms, self.t, True)

                return self.t.render_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id='0', url_action=url_action)                
            
        else:
            form_values=self.model.select_a_row_where()
            
            if not form_values:
                form_values={}
            
            form=show_form(form_values, edit_forms, self.t, True)            
            
            return self.t.render_template(self.template_insert, admin=self, title_edit=title_edit, form=form, model=self.model, id=0, url_action=url_action)
        
