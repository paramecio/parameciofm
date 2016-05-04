#!/usr/bin/python3

import argparse
import os
import shutil
import getpass
from pathlib import Path
from base64 import b64encode
from paramecio.cromosoma.webmodel import WebModel
from paramecio.modules.admin.models.admin import UserAdmin

def start():

    parser=argparse.ArgumentParser(description='A tool for create new paramecio sites')

    parser.add_argument('--path', help='The path where the paramecio site is located', required=True)

    parser.add_argument('--modules', help='A list separated by commas with the git repos for download modules for this site', required=False)

    parser.add_argument('--symlink', help='Set if create direct symlink to paramecio in new site', required=False, nargs='?', const='1')

    args=parser.parse_args()
    
    workdir=os.path.dirname(os.path.abspath(__file__))
    
    # Create directory
    
    path=Path(args.path)
    
    try:
        path.mkdir(0o755, True)
        
    except:
        
        print('Error: cannot create the directory. Check if exists and if you have permissions')
        exit()
    # Create folder settings and copy index.py, admin.py 
    
    path_settings=args.path+'/settings'
    
    try:
    
        os.mkdir(path_settings, 0o755)
    except:
        print('Error: cannot create the directory. Check if exists and if you have permissions')
        
    # Copy the files. Need optimization, use an array for save the filenames and a simple for loop.
    
    try:
        
        shutil.copy(workdir+'/settings/config.py.sample', path_settings+'/config.py')
        
    except:
        
        print('Error: cannot copy the file config.py. Check if exists and if you have permissions for this task')
    
    try:
        
        shutil.copy(workdir+'/frontend/index.py', args.path+'/index.py')
        
    except:
        
        print('Error: cannot copy the file index.py. Check if exists and if you have permissions for this task')
    
    try:
        
        shutil.copy(workdir+'/frontend/padmin.py', args.path+'/padmin.py')
        
    except:
        
        print('Error: cannot copy the file padmin.py. Check if exists and if you have permissions for this task')
    
    try:
        
        shutil.copy(workdir+'/frontend/i18nadmin.py', args.path+'/i18nadmin.py')
        
    except:
        
        print('Error: cannot copy the file i18nadmin.py. Check if exists and if you have permissions for this task')
        
    try:
        
        shutil.copy(workdir+'/frontend/regenerate.py', args.path+'/regenerate.py')
        
    except:
        
        print('Error: cannot copy the file regenerate.py. Check if exists and if you have permissions for this task')
    
    try:
        
        shutil.copy(workdir+'/frontend/create_module.py', args.path+'/create_module.py')
        
    except:
        
        print('Error: cannot copy the file create_module.py. Check if exists and if you have permissions for this task')
        

    try:
        
        shutil.copy(workdir+'/settings/modules.py', path_settings+'/modules.py')
        
    except:
        
        print('Error: cannot copy the file modules.py. Check if exists and if you have permissions for this task')
    
    if args.symlink!=None:
        try:
            os.symlink(workdir, args.path+'/paramecio', True)
            
        except:
            print('Error: cannot symlink paramecio in new site')

    f=open(path_settings+'/config.py', 'r')
    
    conf=f.read()
    
    f.close()
    
    random_bytes = os.urandom(24)
    secret_key_session = b64encode(random_bytes).decode('utf-8').strip()
    
    conf=conf.replace('im smoking fool', secret_key_session)
    
    f=open(path_settings+'/config.py', 'w')
    
    f.write(conf)
    
    f.close()
    
    # Question about mysql configuration? If yes, install configuration
    
    s=input('Do you want use paramecio with MySQL database? y/n: ')
    
    if s=='y' or s=='Y':
        
        host_db=input('MySQL database server host, by default localhost: ').strip()
        
        db=input('MySQL database name, by default paramecio_db: ').strip()
        
        user_db=input('MySQL database user, by default root: ').strip()
        
        pass_db=getpass.getpass('MySQL database password, by default "": ').strip()
        
        if host_db=='':
            
            host_db='localhost'
        
        if user_db=='':
            
            user_db='root'
        
        #user=UserAdmin()

        #Create db
        
        if db=="":
            db='paramecio_db'
        
        WebModel.connections={'default': {'name': 'default', 'host': host_db, 'user': user_db, 'password': pass_db, 'db': '', 'charset': 'utf8mb4', 'set_connection': False} }
        
        connection_code="WebModel.connections={'default': {'name': 'default', 'host': '"+host_db+"', 'user': '"+user_db+"', 'password': '"+pass_db+"', 'db': '"+db+"', 'charset': 'utf8mb4', 'set_connection': False} }"
        
        with open(path_settings+'/config.py', 'a') as f:
            f.write("\n\n"+connection_code)
            f.close()
        
        sql='create database '+db
        
        if not WebModel.query(WebModel, sql):
            print('Error: cannot create database, check the data of database')
        
        else:
            
            WebModel.query(WebModel, 'use '+db)
            
            admin=input('Do you want create admin site? y/n: ')
        
            if admin=='y' or admin=='Y':
                
                try:
        
                    shutil.copy(workdir+'/settings/modules.py.admin', path_settings+'/modules.py')
        
                    shutil.copy(workdir+'/settings/config_admin.py.sample', path_settings+'/config_admin.py')
                
                    useradmin=UserAdmin()
                
                    sql=useradmin.create_table()
                    
                    if not WebModel.query(WebModel, sql):
                        print('Error: cannot create table admin, you can create this table with padmin.py')
                    else:
                        
                        # Add admin module to config
                        with open(path_settings+'/config.py', 'r') as f:
                            
                            config_text=f.read()
                            
                            f.close()
                        
                        config_text=config_text.replace("modules=['paramecio.modules.welcome']", "modules=['paramecio.modules.welcome', 'paramecio.modules.admin', 'paramecio.modules.lang']")
                        
                        with open(path_settings+'/config.py', 'w') as f:
                            
                            f.write(config_text)
                            
                            f.close()

                        try:
        
                            shutil.copy(workdir+'/settings/modules.py.admin', path_settings+'/modules.py')
                            
                        except:
                            
                            print('Error: cannot copy the file modules.py. Check if exists and if you have permissions for this task')
                        
                        print('Created admin site...')
                
                except:
                    
                    print('Error: cannot copy the file padmin.py. Check if exists and if you have permissions for this task')
                
                
        pass
    
        # Question about install admin site.

if __name__=="__main__":
    start()
