#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from base import BaseHandler
from model.handle import DML


class Check(BaseHandler):
    @staticmethod
    def md5(result):
        import hashlib
        m = hashlib.md5()
        m.update(result.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def login_check(input_username, input_password):
        obj = DML()
        user_obj = obj.get_user(input_username)
        if user_obj:
            md5_input_password = Check.md5(input_password)
            if user_obj.password == md5_input_password:
                return user_obj.user_group
            else:
                return "Incorrect password"
        else:
            return "Invalid username"
