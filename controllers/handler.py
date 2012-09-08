#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from weibo import APIClient

from config.settings import (
    APP_KEY,
    APP_SECRET,
    CALLBACK_URL,
    template_file,
)

class GlobalData:
    pass

gd = GlobalData()

class Index(tornado.web.RequestHandler):
    def post(self):
        gd.client = APIClient(app_key=APP_KEY, 
                           app_secret=APP_SECRET,
                           redirect_uri=CALLBACK_URL)
        url = gd.client.get_authorize_url()
        self.render(template_file('welcome.html'), authorized_url=url)

class Callback(tornado.web.RequestHandler):
    def post(self):
        code = self.get_argument('code')
        gd.client = APIClient(app_key=APP_KEY,
                           app_secret=APP_SECRET,
                           redirect_uri=CALLBACK_URL)
        r = gd.client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        gd.client.set_access_token(access_token, expires_in)
        self.redirect('/info')

class Info(tornado.web.RequestHandler):
    def get(self):
        self.render(template_file('info.html'))

class Show(tornado.web.RequestHandler):
    def post(self):
        get_screen_name = True
        screen_name = self.get_argument('screen_name', default=None)
        if not screen_name:
            uid = self.get_argument('uid', default=None)
            get_screen_name = False
        if get_screen_name:
            res = gd.client.get.statuses__user_timeline(
                                screen_name=screen_name)
        elif uid:
            res = gd.client.get.statuses__user_timeline(user_id=uid)
        else:
            self.redirect('/info')
        self.render(template_file('show.html'), res=res)
