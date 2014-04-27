async_amqp
==============
Conference materials.

Requirements
============
* Vagrant
* VirtualBox/VMware
* Python 2.x

Installation steps
==================
* Clone this repository and run vagrant from the root of project: `vagrant up`
* Install Python requirements: `pip install -r requirements.txt`

Note for Mac OS users
=====================
If you have problem while installing gevent on your mac try this:

    ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install -r requirements.txt