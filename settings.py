#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Database
DATABASES = {
    'DBTYPE': 'mysql',
    'ENGINE': 'mysqldb',
    'USER': 'docker',
    'PASSWORD': 'docker',
    'HOST': '192.168.91.92',
    'PORT': '3306',
    'DBNAME': 'docker',
}


template_variables = dict(
    username="",
)


COOKIE_NAME = "user_id"

NODE_LIST = ['node_ip', 'port']
