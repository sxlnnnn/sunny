#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core.user import Login,Logout
from core.views import Home, ConList, NodeList, NodeManage, NodeModify, NodeAdd, NodeDel, ConModify, ConManage, ConCreate, ConAction, ConStart, ConStop, ConRestart, ConDestroy

urls = [
    (r"/", Login),
    (r"/login", Login),
    (r"/logout", Logout),
    (r"/home", Home),
    (r"/nodelist", NodeList),
    (r"/conlist", ConList),
    (r"/nodemanage", NodeManage),
    (r"/nodemodify", NodeModify),
    (r"/nodeadd", NodeAdd),
    (r"/nodedel", NodeDel),
    (r"/conmanage", ConManage),
    (r"/conmodify", ConModify),
    (r"/concreate", ConCreate),
    (r"/conaction", ConAction),
    (r"/constart", ConStart),
    (r"/constop", ConStop),
    (r"/conrestart", ConRestart),
    (r"/condestroy", ConDestroy),
]