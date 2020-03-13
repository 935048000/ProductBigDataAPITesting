# -*- coding: utf-8 -*-
# @Time : 2020-3-13 8:57
# @Author : chenhao
# @FileName: app.py
# @Software: PyCharm
# @E-Mail: chenhao886640@gmail.com

from flask import Flask, request, render_template, session, redirect, url_for
from utils.Log import logger
from utils.utils import mysql
from utils.utils import load_config
from utils.utils import returnData

config = load_config()
mysql = mysql(config['mysql'])
app = Flask(__name__)
_logger = logger()
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
        
        sql = """
                INSERT INTO `apitesting`.`t_host`(`host`, `port`, `explain`, `state`)
                VALUES ('{0}', '{1}', '{2}', '1');
                """.format (request.form['host'], request.form['port'], request.form['explain'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/showHostService", methods=["POST"])
def addHostService():
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
                WHERE
                h.state = 1
        """.format (request.form['startDate'], request.form['stopDate'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/addTestCase", methods=["POST"])
def addHostService():
    """
    写入测试用例
    :return:
    """
    try:
        
        sql = """
                INSERT INTO `apitesting`.`t_testcase`(`host_id`, `url`, `requests_data`, `result`)
                VALUES ( {0}, '{1}', '{2}', '{3}')
                """.format (request.form['host_id'], request.form['url'], request.form['requests_data'], request.form['result'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/showTestCase", methods=["POST"])
def addHostService():
    """
    查看测试用例
    :return:
    """
    try:
        
        sql = """
                SELECT
                h.host,h.port,tc.url,tc.requests_data,tc.result
                FROM
                t_testcase tc
                LEFT JOIN t_host h on h.id = tc.host_id
                WHERE
                h.state = 1
                """.format (request.form['startDate'], request.form['stopDate'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


@app.route ("/testing/showTestResult", methods=["POST"])
def addHostService():
    """
    查看测试结果
    :return:
    """
    try:
        
        sql = """
                SELECT
                *
                FROM
                t_test_log tl
                LEFT JOIN t_testcase tc on tc.id = tl.testcase_id
                """.format (request.form['startDate'], request.form['stopDate'])
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return returnData ("404", "失败", None)
    return returnData ("0", "成功", _rdata)


def addHostService(test_code,test_username,testcase_id,testcase_result,testcase_recode,testcase_count):
    """
    写入测试结果
    
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
                VALUES ('{0}', '{1}', {2}, '{3}', '{4}', {5})
                """.format (test_code, test_username,testcase_id,testcase_result,testcase_recode,testcase_count)
        # _logger.info ("sql="+sql)
        _rdata = mysql.fetchall_db (sql)
        _logger.info (_rdata)
    except Exception as e:
        _logger.error ("error: {}".format (e))
        return -1
    return 0

@app.route ("/testing/showTestResult", methods=["POST"])
def executeTestCase():
    """
    执行测试用例
    :return:
    """
    
    pass
    return























if __name__ == '__main__':
    app.run(debug=True, port=8089)