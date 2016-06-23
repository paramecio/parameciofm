#!/usr/bin/python3

import argparse
import os
import shutil
import getpass
import re
from pathlib import Path
from base64 import b64encode
from paramecio.cromosoma.webmodel import WebModel
from paramecio.modules.admin.models.admin import UserAdmin
from subprocess import call
from urllib.parse import urlparse

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
        
        conn=WebModel.connection()
        
        useradmin=UserAdmin(conn)
        
        if not useradmin.query(sql):
            print('Error: cannot create database, check the data of database')
        
        else:
            
            useradmin.query('use '+db)
            
            admin=input('Do you want create admin site? y/n: ')
        
            if admin=='y' or admin=='Y':
                
                try:
        
                    shutil.copy(workdir+'/settings/modules.py.admin', path_settings+'/modules.py')
        
                    shutil.copy(workdir+'/settings/config_admin.py.sample', path_settings+'/config_admin.py')
                
                    sql=useradmin.create_table()
                    
                    if not useradmin.query(sql):
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
                    exit(1)
                
        pass
    
        # Install modules
        
        if args.modules.strip()!='':
        
            arr_modules=args.modules.split(',')
            
            final_modules=[]
            
            final_modules_models=[]
            
            if len(arr_modules)>0:
                
                for k, module in enumerate(arr_modules):
                    
                    module=module.strip()
                    
                    try:
                    
                        u=urlparse(module)
                    
                        module_path=os.path.basename(u.path)
                    
                    except:
                        print('Error: not valid url for repository')
                        exit(1)
                    
                
                    if call("git clone %s %s/modules/%s" % (module, path, module_path), shell=True) > 0:
                        print('Error, cannot  install the module %s' % module_path)
                        exit(1)
                    else:
                        print('Added module %s' % module_path)
                        
                    final_modules.append(("modules/%s" % (module_path)).replace('/', '.'))
                    final_modules_models.append("modules/%s/models" % (module_path))

                    # Execute postscript
                    
                    postscript="%s/modules/%s/install/postinstall.py" % (path, module_path)
                    
                    if os.path.isfile(postscript):
                        
                        os.chmod(postscript, 0o755)
                        
                        if call(postscript, shell=True) > 0:
                            print('Error, cannot execute the postinstall script')
                            exit(1)
                        else:
                            print('Postinstall script finished')
                        
                    
                # Edit  config.py
                
                with open(path_settings+'/config.py') as f:
                    
                    modules_final='\''+'\', \''.join(final_modules)+'\''
                    
                    p=re.compile(r"^modules=\[(.*)\]$")
                    
                    #config_file=p.sub(r"modules=[\1, "+modules_final+"]", "modules=['paramecio.modules.welcome', 'paramecio.modules.admin', 'paramecio.modules.lang', 'modules.pastafari', 'modules.monit', 'modules.example']")
                    
                    final_config=''
                    
                    for line in f:
                        if p.match(line):
                            line=p.sub(r"modules=[\1, "+modules_final+"]", line)
                        final_config+=line
                    
                with open(path_settings+'/config.py', 'w') as f:
                    
                    f.write(final_config)
                    
                    print('Updated configuration for add new modules...')
                
                real_dir=os.getcwd()
                    
                os.chdir(args.path)
                
                #Regenerating modules.py
                
                regenerate='regenerate.py'
                
                os.chmod(regenerate, 0o755)
                
                if call('./regenerate.py', shell=True) > 0:
                    print('Error, cannot regenerate the modules.py script')
                    exit(1)
                else:
                    print('Regeneration of modules.py finished')
                
                # Installing models
                    
                padmin='padmin.py'
                
                os.chmod(padmin, 0o755)
                
                for models_path in final_modules_models:
                    
                    #models_path="modules/%s/models" % (module_path)
                    
                    if os.path.isdir(models_path):
                        
                        models_files=os.listdir(models_path)
                        
                        m=re.compile(".*\.py$")
                        
                        underscore=re.compile("^__.*")
                        
                        for f in models_files:
                            
                            if m.match(f) and not underscore.match(f):
                                
                                if call('./padmin.py --model '+models_path+'/'+f, shell=True) > 0:
                                    print('Error, cannot create the modules of '+models_path+'/'+f)
                                else:
                                    print('Modules from '+models_path+'/'+f+' created')
                    

if __name__=="__main__":
    start()
