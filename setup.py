#!/usr/bin/env python3

import sys
import os
from setuptools import setup, find_packages


if sys.version_info < (3, 3):
    raise NotImplementedError("Sorry, you need at least Python 3.3 to use paramecio.")

#import paramecio
# Pillow should be installed after if you need ImageField
# If you install passlib and bcrypt, the password system will use bcrypt by default, if not, will use native crypt libc 

setup(name='paramecio',
      version='0.1.2',
      description='Fast and simple Framework based in bottle and Mako.',
      long_description='This framework is simple framework used for create web apps. Paramecio is modular and fast. By default have a module called admin that can be used for create admin sites',
      author='Antonio de la Rosa Caballero',
      author_email='webmaster@web-t-sys.com',
      url='http://paramecioproject.com/',
      packages=['paramecio'],
      include_package_data=True,
      install_requires=['bottle', 'mako', 'mysqlclient', 'sqlalchemy', 'beaker>=1.8.0', 'itsdangerous', 'colorama','cherrypy', 'arrow'],
      entry_points={'console_scripts': [
        'paramecio = paramecio.console:start',
      ]},
      license='GPLV2',
      platforms = 'any',
      classifiers=['Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLV2 License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
     )
