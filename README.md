[![PyPI version](https://img.shields.io/pypi/v/ansible.svg)](https://pypi.python.org/pypi/ansible/2.4.1.0)

# developer
Setup developer enviroment for linux desktops.
## Supported os distribution:
CentOS 6
CentOS 7
Debian 7
Debian 8
Ubuntu 12.04
Ubuntu 14.04
Ubuntu 16.04

## Including tasks:
* General setting
  * Proxy setting
  * APT/YUM source mirrors
  * Developer account define
* SDKs
  * JDK
  * Scala
  * Go
  * NodeJS
  * Python2/Python3
* Editors
  * Vim Setting
  * Sublime
  * Meld
* Tools
  * Chrome
  * NFS
  * Samba
  * VNC
* Developer Tools
  * Maven
  * Gradle
  * Eclipse
  * Idea IDE
  * Docker
  * Ansible

## Usage
Define inventory
```sh
cp hosts .hosts
vi .hosts
```
Run
```sh
ansible-playbook -i .hosts install-machine.yml
```
