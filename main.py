#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define,options,parse_command_line
define('port', default=8000, type=int, help="listen port")
from urls import urls

if __name__ == '__main__':
    SETTINGS = {
        "template_path": os.path.join(os.path.dirname(__file__),"templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "login_url": "/login",
        "cookie_secret": "235lksjfASKJFlks=jdfGLKS=JDFLKSsfjlk234dsjflksdjffj/=sf"
    }
    application = tornado.web.Application(handlers=urls,**SETTINGS)
    parse_command_line()
    print('serve listen port %s' % options.port)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()