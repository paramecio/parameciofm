#!/usr/bin/python3

import argparse
import os
import re
from pathlib import Path
from importlib import import_module
from paramecio.citoplasma.i18n import I18n
from settings import config

pattern=re.compile('^\w+\.(py|html|phtml)$')

ignored=re.compile('^[__|\.].*$')

lang_p=re.compile("I18n\.lang\('(.*?)',\s+'(.*?)',\s+'(.*?)'\)")
lang_t=re.compile("\${lang\('(.*?)',\s+'(.*?)',\s+'(.*?)'\)\}")

tmp_lang={}

def start():
    
    global lang_p
    global lang_t
    
    # Module to search a file where save the file.
    
    parser = argparse.ArgumentParser(description='A tool for create python language files')
    
    parser.add_argument('--module', help='The module where search lang files', required=False)
    
    args = parser.parse_args()
    
    #Without arguments, search in paramecio directory all language files
    
    path_save='paramecio/i18n'
    
    path='paramecio'
    
    if args.module!=None:
        
        path=args.module
        
        path_save=args.module+'/i18n'
        
        module_base=os.path.basename(args.module)
        
        lang_p=re.compile("I18n\.lang\('("+module_base+"?)',\s+'(.*?)',\s+'(.*?)'\)")
        lang_t=re.compile("\${lang\('("+module_base+"?)',\s+'(.*?)',\s+'(.*?)'\)\}")
    
    
    if not os.path.isdir(path):
        
        print("Error: directory to scan doesn't exists")
    
        exit(1)
    
    scandir(path, path_save)
    
    #Save the files

    file_lang=''
    
    for module in tmp_lang.keys():
        
        # Save in a file
        real_path=path_save
        
        if not os.path.isdir(real_path):
        
            p=Path(real_path)
            p.mkdir(0o755, True)
        
        try:
            path_module=path_save.replace('/', '.')+'.'+module
            
            import_module(path_module)
            
            #Add values to tmp lang
            
            #for real_key, real_text in I18n.l[lang][module].items():
                #tmp_lang[module][real_key]=real_text
                
        except:
            pass
            
        
        file_lang="#!/usr/bin/python3\n\n"
        
        file_lang+="from paramecio.citoplasma.i18n import I18n\n\n"
        
        for lang in I18n.dict_i18n:
            
            file_lang+="I18n.l['"+lang+"']={'"+module+"': {}}\n\n"
            
            I18n.l[lang]=I18n.l.get(lang, {})
            
            I18n.l[lang][module]=I18n.l[lang].get(module, {})
            
            for key, text in tmp_lang[module].items():
                
                if not key in I18n.l[lang][module]:
                    
                     I18n.l[lang][module][key]=text

                file_lang+="I18n.l['"+lang+"']['"+module+"']['"+key+"']='"+I18n.l[lang][module][key]+"'\n\n"
            
            final_file=real_path+'/'+module+'.py'
            
        f=open(final_file, 'w')
        
        f.write(file_lang)
        
        f.close()
    
    pass

def scandir(path, module_search=''):
    
    list=os.listdir(path)
    
    for name in list:
        
        new_path=path+'/'+name
        
        if os.path.isdir(new_path):           
            if ignored.match(name)==None:
                scandir(new_path)
        elif pattern.match(name)!=None and ignored.match(name)==None:
            
            f=open(new_path)
            
            for line in f:
                
                match_p=lang_p.search(line)
                match_t=lang_t.search(line)
                
                if match_p!=None:
                     #print(match_p.group(1))
                     
                    module=match_p.group(1)
                    symbol=match_p.group(2)
                    text_default=match_p.group(3)
                    
                    tmp_lang[module]=tmp_lang.get(module, {})

                    tmp_lang[module][symbol]=tmp_lang[module].get(symbol, text_default)
                    
                if match_t!=None:
                    
                    module=match_t.group(1)
                    symbol=match_t.group(2)
                    text_default=match_t.group(3)
                    
                    tmp_lang[module]=tmp_lang.get(module, {})

                    tmp_lang[module][symbol]=tmp_lang[module].get(symbol, text_default)
            
            f.close()
                
            #print('archivo->'+path+'/'+name)
            # Open file
            # obtain modules, keys, and default text

    #Open all files in path specified. If not specified, see in all files recursively in path.
    
    #Extract lang and I18n.lang and fill i18n property that save the values of language texts, only extracs key specified in option key, if not specified, extract last member of path key.

    # Open all language files in a loop with modules from dictionary created from open files, if module path is not specified, the file is in paramecio.i18n. With module path the language files are saved in i18n directory into the path, for example if path is modules/panel, the files are saved in modules/panel/i18n/example.py. If key option is saved then only saved lang with keys selected. Normally you only need a file by module and by default. key option is the last member of path. For example, you can create a language file for a module and use in other module, but don't extract key used in the other module language file used. 
    
    # THe array i18n is overwrited loading the lang files.
    
    # Save the files in specified path.

if __name__=='__main__':
    
    start()
    
    