#!/usr/bin/python3

import argparse
import os
import shutil
import getpass
from pathlib import Path
from paramecio.cromosoma.webmodel import WebModel
from paramecio.modules.admin.models.admin import UserAdmin

def start():

    parser=argparse.ArgumentParser(description='A tool for create new paramecio sites')

    parser.add_argument('--path', help='The path where the paramecio site is located', required=True)

    args=parser.parse_args()
    
    workdir=os.path.dirname(os.path.abspath(__file__))
    
    # Create directory
    
    path=Path(args.path)
    
    try:
        path.mkdir(0o755, True)
        
    except:
        
        print('Error: cannot create the directory. Check if exists and if you have permissions')

    # Create folder settings and copy index.py, admin.py 
    
    path_settings=args.path+'/settings'
    
    try:
    
        os.mkdir(path_settings, 0o755)
    except:
        print('Error: cannot create the directory. Check if exists and if you have permissions')
        
    # Copy the files
    
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
        
        
        connection="WebModel.connections={'default': {'name': 'default', 'host': '"+host_db+"', 'user': '"+user_db+"', 'password': '"+pass_db+"', 'db': 'example', 'charset': 'utf8mb4', 'set_connection': False} }"
        
        with open(path_settings+'/config.py', 'a') as f:
            f.write("\n\n"+connection)
            f.close()
        
        #user=UserAdmin()

        #Create db
        
        if db=="":
            db='paramecio_db'
        
        WebModel.connections={'default': {'name': 'default', 'host': host_db, 'user': user_db, 'password': pass_db, 'db': '', 'charset': 'utf8mb4', 'set_connection': False} }
        
        sql='create database '+db
        
        if not WebModel.query(WebModel, sql):
            print('Error: cannot create database, check the data of database')
        
        else:
            
            WebModel.query(WebModel, 'use '+db)
            
            admin=input('Do you want create admin site? y/n: ')
        
            if admin=='y' or admin=='Y':
                
                try:
        
                    shutil.copy(workdir+'/settings/config_admin.py.sample', path_settings+'/config_admin.py')
                
                    useradmin=UserAdmin()
                
                    sql=useradmin.create_table()
                    
                    if not WebModel.query(WebModel, sql):
                        print('Error: cannot create table admin, you can create this table with padmin.py')
                    else:
                        print('Created admin site...')
                
                except:
                    
                    print('Error: cannot copy the file padmin.py. Check if exists and if you have permissions for this task')
                
                
        pass
    
        # Question about install admin site.


if __name__=="__main__":
    start()