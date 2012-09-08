#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop

from config.url import urls
from config.settings import settings

application = tornado.web.Application(urls, **settings)

if __name__ == '__main__':
    application.listen(9009)
    tornado.ioloop.IOLoop.instance().start()
