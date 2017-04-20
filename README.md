
# Sunny
这是用python2.7开发的docker管理系统，实现了如下功能

• 存储Docker节点和容器的基本信息

• 数据完全自动收集和更新

• Docker节点添加，修改，删除。

• 容器创建，启动，停止，重启，销毁
 
• 用户登录认证


# 使用说明

settings.py里面是sqlalchemy使用的数据库连接引擎的配置文件，需要修改成你自己环境的正确参数。

进入model目录，运行python models.py 将自动创建项目需要的表

运行python handle.py 将自动创建一个用户名密码都是docker管理用户，你可以修改最后一行来更改名字和密码，属组。

运行python main.py将启动程序于8000端口  


