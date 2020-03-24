# -*- coding: utf-8 -*-
# @Time : 2020-3-20 8:50
# @Author : chenhao
# @FileName: cronTaskTest.py
# @Software: PyCharm
# @E-Mail: chenhao886640@gmail.com

from flask import Flask, request
from flask_apscheduler import APScheduler  # 主要插件
import datetime

app = Flask(__name__)
scheduler = APScheduler()

def task1(a, b):
    print('mession1')
    print(datetime.datetime.now())


def task2(a, b):
    print('mession2')
    print(datetime.datetime.now())


@app.route('/pause', methods=['POST'])
def pausetask():  # 暂停
    data = request.form['id']
    scheduler.pause_job(str(data))
    return "Success!"


@app.route('/resume', methods=['POST'])
def resumetask():  # 恢复
    data = request.form['id']
    scheduler.resume_job(str(data))
    return "Success!"


@app.route('/gettask', methods=['POST'])
def get_task():  # 获取
    data = request.form['id']
    jobs = scheduler.get_jobs()
    print(jobs)
    return str(jobs)


@app.route('/remove_task', methods=['POST'])
def remove_task():  # 移除
    data = request.form['id']
    scheduler.remove_job(str(data))
    return 111


@app.route('/addjob', methods=['GET', 'POST'])
def addtask():
    data = request.form['id']
    if data == '1':
        scheduler.add_job(func=task1, id='1',name="测试1", args=(1, 2), trigger='cron', day_of_week='0-6', hour=8, minute=57,
                          second=10,
                          replace_existing=True)
        # trigger='cron' 表示是一个定时任务
    else:
        scheduler.add_job(func=task2, id='2',name="测试2", args=(1, 2), trigger='interval', seconds=10,
                          replace_existing=True)
        # trigger='interval' 表示是一个循环任务，每隔多久执行一次
    return 'sucess'


if __name__ == '__main__':
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(debug=True, port=8070)
