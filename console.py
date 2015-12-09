#!/usr/bin/python3

import argparse
import os
import shutil
from pathlib import Path

def start():

    parser=argparse.ArgumentParser(description='A tool for create new paramecio sites')

    parser.add_argument('--path', help='The path where the paramecio site is created', required=True)

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
        
        print('Error: cannot copy the file. Check if exists and if you have permissions for this task')
        
    # Question about mysql configuration? If yes, install configuration
    
    # Question about install admin site.


if __name__=="__main__":
    start()