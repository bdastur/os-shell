# os-shell
---

[![PyPI Version](https://img.shields.io/pypi/v/os-shell.svg)](https://pypi.python.org/pypi/os-shell)

An interactive OpenStack command shell.

![alt text](https://github.com/bdastur/os-shell/blob/master/docs/images/os_shell_cmdline.gif "Interactive Shell")



## Installation
Simplest way to install is using pip

If installing in a virtualenv
```
pip install os-shell
```

If you are not installing in a virtualenv, run:
```
sudo pip install os-shell
```

## Supported Python Versions.
Currently supported version of python:

  * 2.7.x and greater

## Basic Usage
os-shell accepts the same commands and options as the openstack CLI. Once in the shell you dont need to specify 'openstack' as the prefix.

*Example:*
```
$os-shell
openstack> server list
+--------------------------------------+----------------------+--------+----------------------------------+---------------+
| ID                                   | Name                 | Status | Networks                         | Image Name    |
+--------------------------------------+----------------------+--------+----------------------------------+---------------+
| 75aa51d8-169d-4f0c-b227-c338c885d71f | centos7_server-4bff  | ACTIVE | behzad-dastur-net=100.73.166.106 |               |
| 6ec1b630-823c-4006-8367-f376849cc6c6 | elastic-ace9         | ACTIVE | behzad-dastsur-net=100.73.166.108 |               |
| dfa7b936-70ac-4fba-a41c-2a9b67ddc2a9 | rundeck-centos7-e7f4 | ACTIVE | behzad-dastur-net=100.73.166.109 |               |
| a3ab4dc1-5373-4d19-b6f4-3f947f3a5e52 | staytus-centos-fde9  | ACTIVE | behzad-dasatur-net=100.73.166.110 |               |
+--------------------------------------+----------------------+--------+----------------------------------+---------------+
openstack>

openstack> network list --format json
[
  {
      "Subnets": "389ebaef-aee7-4b61-9639-fe89010755ef", 
          "ID": "4d4dcf18-b1b3-4196-9b80-06ba11fa2b13", 
              "Name": "behzad-dastur-net"
  }
]>openstack>


```

## Features

### Auto completion of commands and options
Providing the correct commands and options as you type, so you never have to remember the tedious commands.

### Inline command history and auto suggest from history.
When in the shell, you can use the up arrow keys to get to previous commands. Also suggest from previous commands.

### auto suggestion for resources.
os-shell caches the current images, flavors and networks information during startup and suggests relevant options during 
command execution.


## Feedback:
User feedback and suggests are most welcome. Create an issue for a feature, fix.



