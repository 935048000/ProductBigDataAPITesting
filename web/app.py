# -*- coding: utf-8 -*-
# @Time : 2020-3-13 8:57
# @Author : chenhao
# @FileName: app.py
# @Software: PyCharm
# @E-Mail: chenhao886640@gmail.com
import sys
sys.path.append("..")
from flask import Flask, request, render_template, session, redirect, url_for
from utils.Log import logger
from utils.utils import mysql
from utils.utils import load_config
from utils.utils import returnData,getTestCode,get_url
from utils.requestsTool import requestsTool
import ast
import pymysql
from flask_cors import CORS

config = load_config()
mysql = mysql(config['mysql'])
app = Flask(__name__)
CORS(app, supports_credentials=True)
_logger = logger
# 模板
# @app.route("/user", methods=['POST', 'GET'])
# def user():

# 获取指定参数：
# request.form[""]
# 获取指定参数并生成默认值：
# request.form.get("key", type=str, default=None)

#     login, userid = False, None
#     if 'userid' not in session:
#         return redirect(url_for('loginForm'))
#     else:
#         login, userid = True, session['userid']
#     userinfo = []
#     try:
#         sql = "select UserID,Location,Age from User where UserID='{}'".format(userid)
#         userinfo = mysql.fetchone_db(sql)
#         userinfo = [v for k, v in userinfo.items()]
#     except Exception as e:
#         logger.exception("select UserInfo error: {}".format(e))
#     return render_template("UserInfo.html",
#                            login=login,
#                            useid=userid,
#                            userinfo=userinfo)


@app.route ("/testing/addHostService", methods=["POST"])
def addHostService():
    """
    写入测试服务
    :return:
    """
    try:
        
        sql = """INSERT INTO `t_host` (`host`, `port`, `explain`, `state`)
                VALUE ('{0}', '{1}', '{2}', '1');
                """.format (request.form['host'], request.form['port'], request.form['explain'])
        _logger.info ("sql="+sql)
        _rdata = mysql.exe (sql)
        
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/updateHostService", methods=["POST"])
def updateHostService():
    """
    修改测试服务
    :return:
    """
    try:
        
        sql = """
                UPDATE t_host
                SET `host` = "{1}",`port` = "{2}",`explain` = "{3}",state = "{4}"
                WHERE
                id = {0}
                """.format (request.form['id'], request.form['host'], request.form['port'], request.form['explain'], request.form['state'])
        _logger.info ("sql=" + sql)
        _rdata = mysql.exe (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)

@app.route ("/testing/showAllHostService", methods=["POST"])
def showAllHostService():
    """
    查看测试服务
    :return:
    """
    try:
        sql = """
                SELECT
                *
                FROM
                t_host
                -- WHERE
                -- state = 1
        """
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/addTestCase", methods=["POST"])
def addTestCase():
    """
    写入测试用例
    :return:
    """
    try:
        
        sql = """
                INSERT INTO `apitesting`.`t_testcase`(`host_id`, `url`, `requests_data`, `result`)
                VALUES ( {0}, '{1}', '{2}', "{3}")
                """.format (request.form['host_id'], request.form['url'], request.form.get("requests_data", type=str, default=None), request.form['result'])
        _logger.info ("sql="+sql)
        _rdata = mysql.exe (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/updateTestCase", methods=["POST"])
def updateTestCase():
    """
    修改测试用例
    :return:
    """
    try:
        
        sql = """
                UPDATE t_testcase
                SET host_id = {4},url = "{1}",result = "{3}",requests_data = "{2}"
                WHERE
                id = {0}
                """.format (request.form['testcase_id'], request.form['url'],
                            request.form.get ("requests_data", type=str, default=None), request.form['result'],request.form['host_id'])
        _logger.info ("sql=" + sql)
        _rdata = mysql.exe (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)

@app.route ("/testing/showTestCase", methods=["POST"])
def showTestCase():
    """
    查看测试用例
    :return:
    """
    try:
        
        sql = """
                SELECT
                tc.id,h.id as host_id,h.host,h.port,tc.url,tc.requests_data,tc.result
                FROM
                t_testcase tc
                LEFT JOIN t_host h on h.id = tc.host_id
                WHERE
                h.state = 1
                """
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/showTestResult", methods=["POST"])
def showTestResult():
    """
    查看测试结果
    :return:
    """
    try:
        
        sql = """
                SELECT
                tl.id,tl.test_code,tl.test_username,tl.testcase_id,tl.testcase_result,tl.testcase_recode,tl.testcase_count,date_format(tl.create_at,"%Y-%m-%d %H:%i:%S") as create_at
                FROM
                t_test_log tl
                LEFT JOIN t_testcase tc on tc.id = tl.testcase_id
                order by
                tl.create_at DESC
                """
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/showAppointTestResult", methods=["POST"])
def showAppointTestResult():
    """
    查看测试结果
    :return:
    """
    try:
        
        sql = """
                SELECT
                tl.id,tl.test_code,tl.test_username,tl.testcase_id,tl.testcase_result,tl.testcase_recode,tl.testcase_count,date_format(tl.create_at,"%Y-%m-%d %H:%i:%S") as create_at
                FROM
                t_test_log tl
                LEFT JOIN t_testcase tc on tc.id = tl.testcase_id
                where tl.create_at >= "{0}" and tl.create_at <= "{1}"
                order by
                tl.create_at DESC
                """.format (request.form['startDate'], request.form['stopDate'],)
        _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)

def addHostService(test_code,test_username,testcase_id,testcase_result,testcase_recode,testcase_count):
    """
    测试结果写入数据库
    
    :param test_code: 测试编码
    :param test_username: 测试用户
    :param testcase_id: 测试用例id
    :param testcase_result: 测试结果
    :param testcase_recode: 测试结果码
    :param testcase_count: 测试次数
    :return:
    """
    try:
        
        sql = """
                INSERT INTO `apitesting`.`t_test_log`(`test_code`, `test_username`, `testcase_id`, `testcase_result`, `testcase_recode`, `testcase_count`)
                VALUES ('{0}', '{1}', {2}, "{3}", '{4}', {5})
                """.format (test_code, test_username,testcase_id,testcase_result,testcase_recode,testcase_count)
        _logger.info ("sql="+sql)
        _rdata = mysql.exe (sql)
        # _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return -1
    return 0

@app.route ("/testing/exeTestCase", methods=["POST"])
def exeTestCase():
    """
    单次执行测试用例
    :return:
    """
    try:
        id_value = []
        
        if (request.form['id']):
            id_value.append (request.form['id'])
            id_value.append (request.form['id'])
            _id = str (tuple (id_value))
        else:
            return returnData ("404", "失败", None)
        
        _logger.info("测试用例ID："+_id)
        
        sql = """
                SELECT
                tc.id,h.host,h.port,tc.url,tc.requests_data,tc.result
                FROM
                t_testcase tc
                LEFT JOIN t_host h on h.id = tc.host_id
                WHERE
                h.state = 1
                and tc.id = {0}
                """.format(request.form['id'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata[0])
        # _logger.info (type(_rdata[0]))
        _requestsTool = requestsTool ()

        # 循环执行测试用例
        for i in _rdata:
            if len(i['requests_data']) < 2:
                data = ""
            else:
                data = ast.literal_eval (i['requests_data'])

            url = get_url(i['host'],i['port'],i['url'])

            code,rdata = _requestsTool.send_post(url,data)

            # 写入数据库
            addHostService(getTestCode(),request.form['username'],i['id'],(str(rdata).replace("\"","\'").replace("'","\'")),code,1)

    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", None)


@app.route ("/testing/exeBatchTestCase", methods=["POST"])
def exeBatchTestCase():
    """
    批量执行测试用例
    :return:
    """

    try:
        # return returnData ("0", "成功", None)
        _logger.info (request.get_data ().decode())
        _logger.info (request.form.get("username", type=str, default="admin_test"))
        t_list = ast.literal_eval(request.get_data ().decode())
        
        print(t_list['jsondata']['list'])
        _logger.info ("批量执行长度=%d"%len(t_list['jsondata']['list']))
        # 批量执行判断，取出需要执行测试用例ID
        id_value = []
        if len(t_list['jsondata']['list']) >= 2:
            _logger.info ("执行多个测试用例")
            for i in t_list['jsondata']['list']:
                id_value.append(i['id'])
            _id = str(tuple(id_value))
        else:
            _logger.info ("执行一个测试用例")
            id_value.append(t_list['jsondata']['list'][0]['id'])
            id_value.append (t_list['jsondata']['list'][0]['id'])
            _id = str (tuple (id_value))
        
        _logger.info ("测试用例ID：" + _id)
        
        sql = """
                SELECT
                tc.id,h.host,h.port,tc.url,tc.requests_data,tc.result
                FROM
                t_testcase tc
                LEFT JOIN t_host h on h.id = tc.host_id
                WHERE
                h.state = 1
                and tc.id in %s
                """%(_id)
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        # _logger.info (_rdata[0])
        # _logger.info (type(_rdata[0]))
        _requestsTool = requestsTool ()
        
        # 循环执行测试用例
        for i in _rdata:
            if len (i['requests_data']) < 2:
                data = ""
            else:
                data = ast.literal_eval (i['requests_data'])
            
            url = get_url (i['host'], i['port'], i['url'])
            
            code, rdata = _requestsTool.send_post (url, data)
            
            # 写入数据库
            addHostService (getTestCode (), t_list['jsondata']['username'], i['id'], (str (rdata).replace ("\"", "\'").replace ("'", "\'")),
                            code, 1)
    
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", None)

@app.route ("/login", methods=["POST"])
def login():
    """
    用户登录
    :return:
    """
    try:
        sql = """
                SELECT
                id,`name`,account
                FROM
                `user`
                WHERE
                account = '{0}'
                AND `password` = '{1}'
                """.format (request.form['account'], request.form['password'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
        if (len(_rdata) <= 0 ):
            return returnData ("404", "失败", None)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)



















if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=False, port=8090,host='0.0.0.0')
    # pass
    # _requestsTool = requestsTool ()
    # data = ast.literal_eval ("{'year': '2019'}")
    # code, rdata = _requestsTool.send_post ("http://49.235.241.182:8080/price/monCorrespondingPeriod",data )
    # print(code)
    # print(getTestCode())

    
    
    
    
    
    
    