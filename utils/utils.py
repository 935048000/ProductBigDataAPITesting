import io
import os
import time

import yaml
import pymysql
# from logger import setup_log
import json

# logger = setup_log(__name__)
DEFAULT_CONFIG_LOCATION = 'config.yml'


class mysql:

    def __init__(self, config):
        """
        实例化链接对象
        :param config: 数据配置参数
        """
        self.connection = pymysql.connect(user=config['user'],
                                          password=config['password'],
                                          port=config['port'],
                                          host=config['host'],
                                          db=config['db'],
                                          charset=config['charset'])

    def fetchone_db(self, sql):
        """
        数据查询
        :param sql: sql语句
        :return:    sql结果
        """
        c = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        self.connection.ping(reconnect=True)
        c.execute(sql)
        return c.fetchone()

    def fetchall_db(self, sql):
        """
        数据查询
        :param sql: sql语句
        :return:    sql结果
        """
        c = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        self.connection.ping(reconnect=True)
        c.execute(sql)
        return c.fetchall()

    def exe(self, sql):
        """
        数据添加
        :param sql: sql语句
        """
        c = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        self.connection.ping(reconnect=True)
        c.execute(sql)
        self.connection.commit()

    def rollback(self):
        """
        回滚
        """
        self.connection.ping(reconnect=True)
        self.connection.rollback()


class InvalidConfigError(ValueError):
    """如果遇到无效的配置.就会引发此异常
    """

    def __init__(self, message):
        super(InvalidConfigError, self).__init__(message)


def read_file(filename, encoding="UTF-8"):
    """
    从本地读入一个文件
    """
    with io.open(filename, encoding=encoding) as f:
        return f.read()


def fix_yaml_loader():
    """确保读出的yaml文件内容
       可以被unicode编码
    """
    from yaml import Loader, SafeLoader

    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
    SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def read_yaml(content):
    """读入yaml文件
    """
    fix_yaml_loader()
    return yaml.load(content)


def read_yaml_file(filename):
    """
    从本地读入yaml文件
    """
    fix_yaml_loader()
    return yaml.load(read_file(filename, "utf-8"))


def load_config(filename=DEFAULT_CONFIG_LOCATION, **kwargs):
    """
        input:
            filename:
                    "/Config/config.yml"
        output:
            items:
                    {'language': 'zh',
                     'neo4j':
                         {'host': '127.0.0.1',
                          'http_port': 7474,
                          'user': 'neo4j',
                          'password': '123456'
                          }
                    }
    """
    if filename is None and os.path.isfile(DEFAULT_CONFIG_LOCATION):
        filename = DEFAULT_CONFIG_LOCATION
    if filename is not None:
        try:
            file_config = read_yaml_file(filename)
        except Exception as e:
            error = "Failed to read configuration file '{}'. Error: {}".format(filename, e)
            # logger.error(error)
            raise InvalidConfigError(error)
        if kwargs:
            file_config.update(kwargs)
        return file_config
    else:
        return kwargs

def returnData(errcode,errmsg,data):
    """
    API返回数据模板
    :param errcode: 返回码
    :param errmsg: 返回信息
    :param data: 返回数据
    :return: JSON字符串
    """
    rdata = {"errcode":None,"errmsg":None,"data":None}
    _data_data = {'data':None}
    rdata["errcode"] = errcode
    rdata["errmsg"] = errmsg
    _data_data["data"] = data
    rdata["data"] = _data_data
    # logger.info(str(rdata))
    return json.dumps(rdata,ensure_ascii=False),{"Content-Type":"application/json;charset=utf-8"}

def getTestCode():
    """
    获取测试code，唯一
    :return:
    """
    return str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-4:]

def get_url(host,port,url):
    """
    获取测试用例URL
    :return:
    """
    return host+":"+port+url













