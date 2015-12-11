#!/usr/bin/python3

import os
import re

pattern=re.compile('^\w+\.py$')

ignored=re.compile('^[__|\.].*$')

lang_p=re.compile("I18n.lang\('(.*)',\s+'(.*)',\s+'(.*)'\)")

def start():
    
    # Module to search a file where save the file.
    
    scandir('.')
    
    pass

def scandir(path):
    
    list=os.listdir(path)
    
    for name in list:
        
        new_path=path+'/'+name
        
        if os.path.isdir(new_path):           
            if ignored.match(name)==None:
                scandir(new_path)
        elif pattern.match(name)!=None and ignored.match(name)==None:
            
            f=open(new_path)
            
            
            
            f.close()
            
            #print('archivo->'+path+'/'+name)
            # Open file
            # obtain modules, keys, and default text

    #Open all files in path specified. If not specified, see in all files recursively in path.
    
    #Extract lang and I18n.lang and fill i18n property that save the values of language texts, only extracs key specified in option key, if not specified, extract last member of path key.

    # Open all language files in a loop with modules from dictionary created from open files, if module path is not specified, the file is in paramecio.i18n. With module path the language files are saved in i18n directory into the path, for example if path is modules/panel, the files are saved in modules/panel/i18n/example.py. If key option is saved then only saved lang with keys selected. Normally you only need a file by module and by default. key option is the last member of path. For example, you can create a language file for a module and use in other module, but don't extract key used in the other module language file used. 
    
    # THe array i18n is overwrited loading the lang files.
    
    # Save the files in specified path.
    
    