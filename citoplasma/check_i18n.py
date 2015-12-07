#!/usr/bin/python3

import os
import re

pattern=re.compile('^\w+\.py$')

ignored=re.compile('^[__|\.].*$')

lang_p=re.compile()

def start():
    
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

    # Open all files in a loop with modules from dictionary created from open files, if module not exists, the file is in i18n
    
    # Load array from file, if file not exists, is created
    
    # If not exists the key with text, add them in arrays loaded from created array
    
    # Rewrite the file with the new arrys and close the file. Open next file
    
    