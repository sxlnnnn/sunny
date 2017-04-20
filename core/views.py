#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import uuid, json, time
import tornado.web
import threading

from base import BaseHandler
from model.handle import DML
from settings import template_variables
from myswarm import Myswarm
from  config import basejson


class Home(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        con_objs = obj.con_usage_info()
        self.render('home.html', con_objs=con_objs, name=template_variables)


class ConList(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        con_objs = obj.con_usage_info()
        self.render('con_list.html', con_objs=con_objs, name=template_variables)


class ConModify(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        con_id = self.get_argument('con_id')
        con_data = obj.get_con_usage_info(con_id)
        con_obj = con_data[0]
        self.render("con_modify.html",con_obj=con_obj, name=template_variables)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        obj = DML()
        con_id = self.get_argument('con_id')
        user_name = self.get_argument('user_name')
        con_app = self.get_argument('con_app')
        con_desc = self.get_argument('con_desc')
        obj.con_usage_modify(con_id, user_name, con_app, con_desc)
        self.write("<script language='javascript'>window.location.href='/conlist'</script>")


class ConManage(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            obj = DML()
            node_port = obj.get_node_port(node_ip)[0]
            myswarm = Myswarm()
            con_data = myswarm.container_list(node_ip, node_port)
            self.render('con_manage.html', con_objs=con_data, node_ip=node_ip,name=template_variables)


class NodeList(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        node_objs = obj.get_node()
        self.render('node_list.html', node_objs=node_objs, name=template_variables)


class NodeManage(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        threads = []
        node_update = threading.Thread(target=self._update_node)
        threads.append(node_update)
        node_pass = threading.Thread(target=self._get_pass)
        threads.append(node_pass)
        for t in threads:
            t.setDaemon(True)
            t.start()
        obj = DML()
        node_objs = obj.get_node()
        self.render('node_manage.html', node_objs=node_objs, name=template_variables)

    def _update_node(self):
        node_state = 'up'
        obj = DML()
        node_data = obj.get_node()
        myswarm = Myswarm()
        for line in node_data:
            node_ip = line.node_ip
            node_port = line.port
            if myswarm.connect_port(node_ip, node_port) == 1:
                node_state = 'down'
                obj.update_node_state(node_ip, node_state)
            else:
                node_info = myswarm.node_info_update(node_ip, node_port)
                node_info['state'] = node_state
                ret = obj.update_node(node_ip, node_info)

    def _get_pass(self):
        pass


class NodeModify(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        node_id = self.get_argument('node_id')
        node_obj = obj.get_node_info(node_id)
        self.render('node_modify.html', node_obj=node_obj, name=template_variables)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        obj = DML()
        node_info = {}
        node_info["node_id"] = self.get_argument('node_id')
        node_info["name"] = self.get_argument('name')
        node_info["node_ip"] = self.get_argument('node_ip')
        node_info["port"] = self.get_argument('port')
        node_info["cpus"] = self.get_argument('cpus')
        node_info["mem"] = self.get_argument('mem')
        node_info["images"] = self.get_argument('images')
        node_info["state"] = self.get_argument('state')
        node_info["node_group"] = self.get_argument('node_group')
        node_info["containers"] = self.get_argument('containers')
        node_info["os_version"] = self.get_argument('os_version')
        node_info["kernel_version"] = self.get_argument('kernel_version')
        node_info["docker_version"] = self.get_argument('docker_version')
        obj.modify_node(node_info)
        self.write("<script language='javascript'>window.location.href='/nodemanage'</script>")


class NodeAdd(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('node_add.html', name=template_variables)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        obj = DML()
        name = self.get_argument('name')
        node_ip = self.get_argument('node_ip')
        port = self.get_argument('port')
        node_group = self.get_argument('node_group')
        obj.add_node(name, node_ip, port, node_group)
        self.write("<script language='javascript'>window.location.href='/nodemanage'</script>")


class NodeDel(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        obj = DML()
        node_id = self.get_argument('node_id')
        result = obj.del_node(node_id)
        self.write("<script language='javascript'>window.location.href='/nodemanage'</script>")


class ConCreate(BaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        node_ip = self.get_argument('node_ip', None)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            obj = DML()
            node_port = obj.get_node_port(node_ip)[0]
            myswarm = Myswarm()
            images_data = myswarm.images_list(node_ip, node_port)
            self.render('con_create.html', node_ip=node_ip, images=images_data, name=template_variables)

    def post(self, *args, **kwargs):
        json_ret = json.loads(basejson[0])
        node_ip = self.get_argument('node_ip', 'None')
        if node_ip == 'None':
            print("There is no node ip")
            return
        obj = DML()
        port_ret = obj.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0]
        con_dict = {}
        for key in ['Cmd', 'Image', 'CpuPeriod', 'CpuQuota', 'CpuShares', 'Memory']:
            con_dict[key] = self.get_argument(key.lower())
            if key == 'Cmd' and con_dict[key] != "":
                json_ret[key] = con_dict[key].split()
            elif key == 'Image' and con_dict[key] != "":
                json_ret[key] = con_dict[key]
            elif con_dict[key] != "":
                json_ret['HostConfig'][key] = int(con_dict[key])

        myswarm = Myswarm()
        json_ret['Name'] = str(uuid.uuid4())[0:13]
        json_ret['Hostname'] = json_ret['Name']

        container_id = myswarm.create_container(node_ip, node_port, json_ret)
        if not container_id:
            print("Can not create the Container")
            return
        ret = myswarm.start_container(node_ip, node_port, container_id)
        self.write("<script language='javascript'>window.location.href='/conmanage?node_ip=%s'</script>" %(node_ip))

class ConAction(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip')
        con_id = self.get_argument('con_id')
        obj = DML()
        port_ret = obj.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0]
        myswarm = Myswarm()
        con_data_handled = myswarm.container_info(node_ip, node_port, con_id)
        self.render("con_action.html", name=template_variables, node_ip=node_ip,
            node_port=node_port, con_id=con_id, con_data=con_data_handled)


class ConStart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        print("      Starting the container......")
        ret = myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write("<script language='javascript'>window.location.href='/conmanage?node_ip=%s'</script>" % (con_dict['node_ip']))

class ConStop(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write("<script language='javascript'>window.location.href='/conmanage?node_ip=%s'</script>" % (
        con_dict['node_ip']))


class ConRestart(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        container_ip = {}
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        time.sleep(2)
        myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write("<script language='javascript'>window.location.href='/conmanage?node_ip=%s'</script>" % (
        con_dict['node_ip']))


class ConDestroy(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.destroy_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.write("<script language='javascript'>window.location.href='/conmanage?node_ip=%s'</script>" % (con_dict['node_ip']))
