
#from modules.pastafari.models.servers import OsServer
from paramecio.citoplasma.generate_admin_class import GenerateConfigClass
from paramecio.citoplasma.lists import SimpleList
from paramecio.citoplasma.adminutils import make_admin_url
#from paramecio.citoplasma.urls import make_url
from paramecio.citoplasma.i18n import I18n
from paramecio.citoplasma.urls import add_get_parameters
from settings import config
from paramecio.citoplasma.httputils import GetPostFiles
from paramecio.cromosoma.coreforms import SelectForm, BaseForm
from paramecio.cromosoma.extraforms.i18nform import I18nForm
import re, json
from collections import OrderedDict
from importlib import import_module

def admin(**args):
    
    t=args['t']

    forms=GetPostFiles()
    
    forms.obtain_query()
    
    selected_module=forms.query.get('module_admin', '')
    
    op=forms.query.get('op', '')    
    
    check_module=re.compile(r'^modules\..*$')
    
    load_mod=None
    
    module_final=OrderedDict()
    
    module_final['0']=''

    for module in config.modules:
        if check_module.match(module):
        
            module=module.replace('modules.', '')
        
            module_final[module]=module

    form_module=SelectForm('module_admin', selected_module, module_final)
    
    arr_lang={}
    
    arr_i18n_form=[]
    
    if selected_module!='':
        #Load module

        if op=='':

            try:
                load_mod=import_module('modules.'+selected_module+'.i18n.'+selected_module)

                for lang in I18n.dict_i18n:

                    for k,v in I18n.l[lang][selected_module].items():

                        #new_form=I18nForm(k, json.dumps(v), '')

                        #arr_i18n_form.append(new_form)
                        
                        arr_lang[k]=arr_lang.get(k, {})
                        arr_lang[k][lang]=v

                z=0

                for k, v in arr_lang.items():
                    
                    new_form=I18nForm(k, json.dumps(v), BaseForm('', ''))

                    new_form.name_field_id='lang_field_'+str(z)

                    arr_i18n_form.append(new_form)
                    
                    z+=1
                    
            except:
                pass
        
        else:
            
            # Create file
            
            t.show_basic_template=False
            
            file_lang="#!/usr/bin/env python3\n\n"
        
            file_lang+="from paramecio.citoplasma.i18n import I18n\n\n"
            
            z=0
            
            for lang in I18n.dict_i18n:
            
                file_lang+="I18n.l['%s']=I18n.l.get('%s', {})\n\n" % (lang, lang)
                
                file_lang+="I18n.l['"+lang+"']['"+selected_module+"']=I18n.l['"+lang+"'].get('"+selected_module+"', {})\n\n"
                
                forms.obtain_post()
                
                for key, text in I18n.l[lang][selected_module].items():
                    
                    if key in forms.post:
                        arr_l=json.loads(forms.post[key])
                        
                        file_lang+="I18n.l['"+lang+"']['"+selected_module+"']['"+key+"']='"+arr_l[lang].replace("'", "\\'")+"'\n\n"
                        
                        z+=1
                
                """
                for key, text in tmp_lang[selected_module].items():
                    
                    if not key in I18n.l[lang][selected_module]:
                        
                         I18n.l[lang][selected_module][key]=text

                    file_lang+="I18n.l['"+lang+"']['"+selected_module+"']['"+key+"']='"+I18n.l[lang][selected_module][key].replace("'", "\\'")+"'\n\n"
                """
            
            error=0
            
            if z>0:
            
                final_file='modules/'+selected_module+'/i18n/'+selected_module+'.py'
                
                old_file=''
                
                with open(final_file, 'r') as f:
                    old_file=f.read()
                    
                
                f=open(final_file, 'w')
                
                try:
                
                    f.write(file_lang)
                    
                except:

                    f.write(old_file)                    
                    error=1 
                
                f.close()

            return {'error': error}

    
    return t.load_template('utils/translations.phtml', modules=module_final, selected_module=selected_module, form_module=form_module, arr_i18n_form=arr_i18n_form)
