# A simple webframework based in Bottle and Mako for create nice webapps

#Installation

This guide give you step by step for install paramecio sucessfully.

## Requirements

For install Paramecio you need a server preferably with GNU/Linux installed. Paramecio is tested normally in Debian derivated how Ubuntu, and Red hat derivated distros how Centos or Fedora but should work fine in FreeBSD, MacOSX and other *nix like operating systems.

Also, you need the next software installed  in  your os:

### Python 3.4 or later. 

Paramecio should work fine in 3.3 but is tested in 3.4 and 3.5 python 3 versions.

In Debian and Ubuntu you can install Python 3 using the next command: `apt-get install python3`.

In Fedora and other Red Hat derived distros you can use `yum install python3`. In RedHat/Centos 6 or 7 you need install [Ius Repos](https://ius.io/GettingStarted/) for get sane versions of python3. In new Fedora versions you can use dnf, a drop-in replacement for yum: `dnf install python3`.

### MySQL or MariaDB database servers. 

MariaDB 10.0 and later are recommended.

In Debian and Ubuntu you can install MariaDB using the next command: `apt-get install mariadb-server`.

In Fedora and other Red Hat derived distros you can use `yum install mariadb-server`. 
In RedHat/Centos 6 probably you need install adittional repositories for get latest versions of mariadb, but with MySQL 5.5, Paramecio should work fine.

When you will install the mysql server, you should create a new user and database for Paramecio.

### Pip

Pip is the package manager of python. You can use the package manager of your os for get python dependencies packages but in my experience is better install the packages directly with pip. 

In Debian and Ubuntu you can install pip using the next command: `apt-get install python3-pip`.

In Fedora and other Red Hat derived distros you can use `yum install python3-pip`. Of course, the command can change if you use Centos 6/7 with **Ius repos**.

### Git

[Git](https://git-scm.com/) is a tool used for manage source code repositories. Also is a tool that can be used for distribute software. For install the next tools you need git installed in your server.

In Debian and Ubuntu you can install git using the next command: `apt-get install git`.

In Fedora and other Red Hat derived distros you can use `yum install git` or `dnf install git` in last fedora versions.

## Install Paramecio Framework

You can install the framework using the next command in your server:

`pip3 install parameciofm`

or if you want development version:

`pip3 install git+https://github.com/paramecio/parameciofm`

This command will install in your server paramecio framework with its dependencies.

When Paramecio finish the installing, you can create your first paramecio site with `paramecio` command.

> If you install passlib and bcrypt python modules, your paramecio install will use bcrypt algorithm for crypt system passwords. If not, default system implementation crypt algorithm (normally the more strong algorithm available in the system) will be used.

### Tipical errors

If you get an error in your installation of dependencies how MarkupSafe or SqlAlchemy, please install gcc or install manually mako and sqlalchemy with your system package manager. For example, for debian and ubuntu:

`apt-get install python3-mako python3-sqlalchemy` and try pip3 command again.

