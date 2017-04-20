#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Node, ConUsage, User
from settings import DATABASES


class DML(object):
    def __init__(self):
        self.engine = create_engine("%s+%s://%s:%s@%s:%s/%s" % (DATABASES['DBTYPE'], DATABASES['ENGINE'],
                                                                DATABASES['USER'], DATABASES['PASSWORD'],
                                                                DATABASES['HOST'], DATABASES['PORT'], DATABASES['DBNAME']))
        self.db_session = sessionmaker(bind=self.engine)
        self.session = self.db_session()

    def create_user(self, name, password, group):
        from core.check import Check
        md5_pass = Check.md5(password)
        user_obj = User(name=name,password=md5_pass,user_group=group)
        self.session.add(user_obj)
        self.session.commit()

    def get_user(self, name):
        user_obj = self.session.query(User).filter(User.name == name).first()
        return user_obj

    def get_node(self):
        node_obj = self.session.query(Node).all()
        return node_obj

    def update_node_state(self, node_ip, node_state):
        result = self.session.query(Node).filter(Node.node_ip == node_ip).update({Node.state: node_state})
        self.session.commit()
        return result

    def update_node(self, node_ip, node_info):
        result = self.session.query(Node).filter(Node.node_ip == node_ip).update({Node.name: node_info['Name'],
                                                                                      Node.state: node_info['state'],
                                                                                      Node.cpus: node_info['NCPU'],
                                                                                      Node.mem: node_info['MemTotal'],
                                                                                      Node.images: node_info['Images'],
                                                                                      Node.containers: node_info['Containers'],
                                                                                      Node.os_version: node_info['OperatingSystem'],
                                                                                      Node.kernel_version: node_info['KernelVersion'],
                                                                                      Node.docker_version: node_info['ServerVersion']},
                                                                                     )
        self.session.commit()
        return result

    def get_node_port(self, node_ip):
        result = self.session.query(Node.port).filter(Node.node_ip == node_ip).first()
        return result

    def con_usage_info(self):
        result = self.session.query(ConUsage).all()
        return result

    def get_con_usage_info(self, con_id):
        result = self.session.query(ConUsage).filter(ConUsage.con_id == con_id).all()
        return result

    def del_container(self, container_id):
        result = self.session.query(ConUsage).filter(ConUsage.con_id == container_id).delete()
        self.session.commit()
        return result

    def get_container(self, container_id):
        result = self.session.query(ConUsage.con_id).filter(ConUsage.con_id == container_id).all()
        return result

    def add_container(self, container_id, container_ip, node_ip):
        obj = ConUsage(con_id=container_id, con_ip=container_ip, node_ip=node_ip)
        result = self.session.add(obj)
        self.session.commit()
        return result

    def con_usage_modify(self, con_id, user_name, con_app, con_desc):
        obj = self.session.query(ConUsage).filter(ConUsage.con_id == con_id).first()
        obj.user_name = user_name
        obj.con_app = con_app
        obj.con_desc = con_desc
        self.session.commit()

    def add_node(self, name, node_ip, port, node_group):
        node_obj = Node(name=name,node_ip=node_ip,port=port,node_group=node_group)
        self.session.add(node_obj)
        self.session.commit()

    def del_node(self, node_id):
        result = self.session.query(Node).filter(Node.id == node_id).delete()
        self.session.commit()
        return result

    def get_node_info(self, node_id):
        result = self.session.query(Node).filter(Node.id == node_id).first()
        return result

    def modify_node(self,node_info):
        result = self.session.query(Node).filter(Node.id == node_info["node_id"]).update({Node.name: node_info['name'],
                                                                                  Node.node_ip: node_info['node_ip'],
                                                                                  Node.port: node_info['port'],
                                                                                  Node.cpus: node_info['cpus'],
                                                                                  Node.mem: node_info['mem'],
                                                                                  Node.images: node_info['images'],
                                                                                  Node.state: node_info['state'],
                                                                                  Node.node_group: node_info['node_group'],
                                                                                  Node.containers: node_info['containers'],
                                                                                  Node.os_version: node_info['os_version'],
                                                                                  Node.kernel_version: node_info['kernel_version'],
                                                                                  Node.docker_version: node_info['docker_version']},
                                                                                 )
        self.session.commit()
        return result


if __name__ == "__main__":
    obj = DML()
    #创建一个测试用账号
    obj.create_user('docker', 'docker', 'admin')

