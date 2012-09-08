#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

APP_KEY = '4232452412'
APP_SECRET = '967416511520e83e040e49c71588b71f'
CALLBACK_URL = 'http://apps.weibo.com/webotxyz/callback'

mail_info = {
    'host': 'smtp.126.com',
    'sender': 'webotxyz',
    'sender_address': 'webotxyz@126.com',
    'sender_password': 'we159357',
}

_template_root = path.abspath(path.dirname(__file__))
_template_root = _template_root[:_template_root.rindex('/')]
_template_root = path.join(_template_root, 'templates')

settings = {'template_path': _template_root}
