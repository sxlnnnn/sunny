#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.web
from model.handle import DML
from settings import template_variables,COOKIE_NAME


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        template_variables["username"] = self.get_secure_cookie(COOKIE_NAME)
        return self.get_secure_cookie(COOKIE_NAME)

    def check_authenticated(self):
        user_name = self.get_secure_cookie(COOKIE_NAME)
        obj = DML()
        user_obj = obj.get_user(user_name)
        user_group = user_obj.user_group
        if user_group != 'admin':
            self.redirect("/")



