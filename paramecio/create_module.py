#!/usr/bin/env python3

import traceback
import argparse
import os,sys
import shutil
import getpass
from pathlib import Path
from settings import config
from importlib import import_module

def start():

    parser=argparse.ArgumentParser(description='A tool for create new modules for paramecio')

    parser.add_argument('--path', help='The path where the new paramecio module is located', required=True)

    args=parser.parse_args()
    
    workdir=os.path.dirname(os.path.abspath(__file__))
    
    # Create directory
    
    path=Path('modules/'+args.path)
    
    try:
        path.mkdir(0o755, True)
        
    except:
        
        print('Error: cannot create the directory. Check if exists and if you have permissions')
        exit(1)

    #Create base controller file
    
    #f=open('modules/'+args.path+'/index.py', 'w')
    
    try:
        shutil.copy(workdir+'/examples/index.py', 'modules/'+args.path)

    except:
        
        print('Error: cannot copy controller example. Check if you have permissions')
        exit(1)
    
    # Regenerate modules
    
    regenerate_modules_config()

def regenerate_modules_config():
    
    print("Regenerating modules configuration...")
    
    modules=[]
    
    modules.append("#!/usr/bin/env python3\n\n")
    modules.append("list_modules=[]\n\n")
    
    for module in config.modules:
    
        try:
            
            controller_path=import_module(module)
            
            controller_base=os.path.dirname(controller_path.__file__)
            
            base_module=module.split('.')[-1]
            
            dir_controllers=os.listdir(controller_base)
            
            modules.append('from '+module+' import ')
            
            arr_controllers=[]
            
            for controller in dir_controllers:
                
                if controller.find('.py')!=-1 and controller.find('__init__')==-1:
                    
                    controller_py=controller.replace('.py', '')
                    
                    arr_controllers.append(controller_py)
                    
                    #load(module+'.'+controller_py)


            modules.append(", ".join(arr_controllers))

            modules.append("\n\n")

            #add_func_static_module(controller_base)
            
        except:
            
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
            exit(1)
    
    f=open('./settings/modules.py', 'w')
    
    f.write("".join(modules))
    
    f.close()

if __name__=="__main__":
    start()
