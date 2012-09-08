#! /usr/bin/env python
# -*- coding: utf-8 -*-

from controllers import handler

urls = [
    (r'/', handler.Index),
    (r'/callback', handler.Callback),
    (r'/info', handler.Info),
    (r'/show', handler.Show),
]
