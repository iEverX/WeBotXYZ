#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.template

from weibo import APIClient

from controllers.helper import send_mail
from config.settings import (
    APP_KEY,
    APP_SECRET,
    CALLBACK_URL,
    settings,
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
        self.render('welcome.html', authorized_url=url)

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
        self.render('info.html')

class Show(tornado.web.RequestHandler):
    def post(self):
        show = self.get_argument('show', default='0')
        email = self.get_argument('email', default='').strip()
        if show == '0' and not email:
            self.redirect('/info')
        count = int(self.get_argument('count', default='50'))
        get_screen_name = True
        screen_name = self.get_argument('screen_name', default='').strip()
        if not screen_name:
            uid = self.get_argument('uid', default='').strip()
            get_screen_name = False
        if get_screen_name:
            res = gd.client.get.statuses__user_timeline(
                                screen_name=screen_name, count=count)
        elif uid:
            res = gd.client.get.statuses__user_timeline(user_id=uid, 
                                                        count=count)
        else:
            self.redirect('/info')
        loader = tornado.template.Loader(settings['template_path'])
        content = loader.load('show.html').generate(res=res)
        if email:
            if send_mail(email.split(';'), 
                         'WeBotXYZ', content):
                self.write('<p style="color: green">send mail successfully!</p>')
            else:
                self.write('<p style="color: red">send mail failed!!</p>')
        if show == '1':
            self.write(content)
