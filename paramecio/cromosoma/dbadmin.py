#!/usr/bin/env python3

import argparse
import os,traceback
import sys, inspect
import shutil
import re
from datetime import date
from pathlib import Path
from colorama import init, Fore, Back, Style
from importlib import import_module, reload
from paramecio.cromosoma.webmodel import WebModel
from settings import config

#from models import books

def start():
    
    connection=WebModel.connection()
    
    #connection.connect_to_db(WebModel.connections['default'])
    
    parser = argparse.ArgumentParser(description='A tool for create tables in databases using models from Cromosoma')

    parser.add_argument('--model', help='Model python path', required=True)
    
    parser.add_argument('--config', help='The config file', required=False)
    
    args = parser.parse_args()
    
    init()
    
    #Import config
    
    config_file='config'
    
    if args.config!=None:
        config_file=args.config
    
    try:
    
        config=import_module('settings.'+config_file)
        
    except:
        e = sys.exc_info()[0]
        v = sys.exc_info()[1]
            
        print(Fore.WHITE+Back.RED+Style.BRIGHT+"Config file not found: %s %s" % (e, v))
        
        exit(1)
    
    #print(WebModel.connections)
    
    if '/' in args.model:
        
        args.model=args.model.replace('/', '.')[:-3] #.replace('.py', '')
    
    try:
    
        model=import_module(args.model)
        
        for name, obj in inspect.getmembers(sys.modules[model.__name__]):
            if inspect.isclass(obj):
                if obj.__module__==args.model and hasattr(obj, 'webmodel'):
                    
                    WebModel.model[name.lower()]=obj(connection)
                    
                    
                    #WebModel.modelobj
        
    except:
        """
        e = sys.exc_info()[0]
        v = sys.exc_info()[1]
            
        print(Fore.WHITE+Back.RED+Style.BRIGHT +"Error, file with model not found: %s %s" % (e, v))
        """
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        
        exit(1)
    
    #load the table of databases
    
    cursor=connection.query("show tables")
    
    table_exists=[]
    
    for row in cursor:
        table=list(row.values())[0]
        
        if table in WebModel.model:
            table_exists.append(table)
        
        #If don't want order
        #set([1,2,3,4]) - set([2,5])
        
    tables=list(WebModel.model.keys())
    
    #Array diff ordered
    
    new_tables=[x for x in tables if x not in table_exists]
    
    #If don't want order
    #new_tables=set(tables)-set(table_exists)
    
    #Need order new_tables
    
    changes=0
    
    #Create new tables
    
    if len(new_tables)>0:
        print(Style.BRIGHT+"Creating new tables...")
        
        changes+=1
        
        for table in new_tables:
            print(Style.NORMAL+"--Creating table "+table+"...")
            connection.query(WebModel.model[table].create_table())

        for table in new_tables:
            
            print("--Adding indexes and constraints for the new table "+table)

            for k_field, index in WebModel.arr_sql_index[table].items():
                print("---Added index to "+k_field)
                connection.query(index)
                
            for k_set, index_set in WebModel.arr_sql_set_index[table].items():
                
                if index_set!="":
                    connection.query(index_set)
                    print("---Added constraint to "+k_set)
                
            print("--Adding uniques elements for the new table")

    #See if changes exists
    
    #Check if created tables are modified.
    
    try:
    
        model_old=import_module('backups.'+args.model)
        
        for name, obj in inspect.getmembers(sys.modules[model_old.__name__]):
            if inspect.isclass(obj):
                if obj.__module__=='backups.'+args.model and hasattr(obj, 'webmodel'):
                    
                    WebModel.model['old_'+name.lower()]=obj(connection)
        
        print(Style.BRIGHT+"Checking old versions of model for find changes...")
        
        for table in tables:
        #connection.query("")
            #Check if new table
            
            #fields_to_add, fields_to_modify, fields_to_add_index, fields_to_add_constraint, fields_to_add_unique, fields_to_delete_index, fields_to_delete_unique, fields_to_delete_constraint, fields_to_delete
            
            fields_to_add=[]
            fields_to_modify=[]
            fields_to_add_index=[]
            fields_to_add_constraint=[]
            fields_to_add_unique=[]
            fields_to_delete_index=[]
            fields_to_delete_unique=[]
            fields_to_delete_constraint=[]
            fields_to_delete=[]
            
            old_table='old_'+table
            
            if not old_table in WebModel.model:
                WebModel.model[old_table]=WebModel.model[table]
            
            for f, v in WebModel.model[table].fields.items():
                
                if not f in WebModel.model[old_table].fields:
                    
                    fields_to_add.append(f)
                    
                    #Add index
                    
                    if v.indexed==True:
                        
                        fields_to_add_index.append(f)
                        
                        changes+=1
                    
                    #Add unique
                    
                    if v.unique==True:
                        
                        fields_to_add_unique.append(f)
                        
                        changes+=1
                    
                    #Add constraint
                    
                    if v.foreignkey==True:
                        
                        fields_to_add_constraint.append(f)
                        
                        changes+=1
                    
                    changes+=1
                
                #If exists field in old webmodel and new
                
                else:
                    
                    v_old=WebModel.model[old_table].fields[f]
                    
                    if v.get_type_sql()!=v_old.get_type_sql():
                        
                        fields_to_modify.append(f)
                        
                        changes+=1
                
                    #Add index
                    
                    if v.indexed==True and v_old.indexed==False:
                        
                        fields_to_add_index.append(f)
                        
                        changes+=1
                    
                    if v.indexed==False and v_old.indexed==True:
                        
                        fields_to_delete_index.append(f)
                        
                        changes+=1
                    
                    #Add unique
                    
                    if v.unique==True and v_old.unique==False:
                        
                        fields_to_add_unique.append(f)
                        
                        changes+=1
                        
                    if v.unique==False and v_old.unique==True:
                        
                        fields_to_delete_unique.append(f)
                        
                        changes+=1
                    
                    #Add constraint
                    
                    if v.foreignkey==True and v_old.foreignkey==False:
                        
                        fields_to_add_constraint.append(f)
                        
                        changes+=1
                        
                    if v.foreignkey==False and v_old.foreignkey==True:
                        
                        fields_to_delete_constraint.append(f)
                        
                        changes+=1
                
            for f, v in WebModel.model[old_table].fields.items():
                
                if not f in WebModel.model[table].fields:
                    
                    #Add constraint
                    
                    if v.foreignkey==True:
                        
                        fields_to_delete_constraint.append(f)
                        
                        changes+=1
                    
                    fields_to_delete.append(f)
                    
                    changes+=1
            
            WebModel.model[table].update_table(fields_to_add, fields_to_modify, fields_to_add_index, fields_to_add_constraint, fields_to_add_unique, fields_to_delete_index, fields_to_delete_unique, fields_to_delete_constraint, fields_to_delete)
                
            #for field_update in arr_update:
                
            
        #Make a for in fields, if the field not exist in old model, create, if is not same type, recreate. If no have index now, delete index, if is a new index, create, same thing with uniques
        
        #for field in WebModel.model
        
    except ImportError:
        
        pass
    
    except:
        
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        
        exit(1)
    
    original_file_path=args.model.replace('.', '/')+'.py'
    
    backup_path='backups/'+original_file_path
    
    if changes>0:
        print(Style.BRIGHT+"Creating backup of the model. WARNING: DON'T DELETE BACKUPS DIRECTORY IF YOU WANT MAKE CHANGES IN THE FUTURE WITHOUT MODIFY DIRECTLY THE DATABASE")
        
        create_backup(original_file_path, backup_path)
        
    else:
        if not os.path.isfile(backup_path):
            create_backup(original_file_path, backup_path)
    
    # Execute script
    
    arr_script_model=args.model.split('.')
    
    arr_script_model.pop()
    
    script_model='.'.join(arr_script_model)+'.scripts.install'
    
    script_py=script_model.replace('.', '/')+'.py'

    if os.path.isfile(script_py):
        
        locked_file='/'.join(arr_script_model)+'/scripts/locked'
        
        if not os.path.isfile(locked_file):

            script_install=import_module(script_model)
            
            script_install.run()
            
            f=open(locked_file, 'w')
            
            f.write('OK')
            
            f.close()
    
    
    #script_model=args.model+''
    
    print(Style.BRIGHT+"All tasks finished")
        
def create_backup(original_file_path, file_path):
    
    #Create copy
    
    path=os.path.dirname(file_path)
    
    p=Path(path)
        
    if not p.is_dir():
        p.mkdir(0o755, True)
        with open(path+'/__init__.py', 'w') as f:
            f.write("#!/usr/bin/env python3\n")
        
    #Create path
        
    if os.path.isfile(file_path):
        today = date.today()
        shutil.copy(file_path, file_path+'.'+today.strftime("%Y%M%d%H%M%S"))
    
    new_file=""
    
    f=open(original_file_path)
    
    for line in f:
        """
        new_line=line.replace("model[\"", "model[\"old_")
        new_line=new_line.replace("model['", "model['old_")
        
        new_line=new_line.replace("WebModel(\"", "WebModel(\"old_")
        new_line=new_line.replace("WebModel('", "WebModel('old_")
        """
        new_file+=line
    
    f.close()
    
    f=open(file_path, 'w')
    
    f.write(new_file)
    
    f.close()
