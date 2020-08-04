# coding:utf-8
# psutil:获取系统信息模块，可以获取CPU，内存，磁盘等的使用情况
import psutil
import time
import datetime
from threading import Timer

import time
from apscheduler.schedulers.blocking import BlockingScheduler


def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func time :', ts)


def func2():
    # 耗时2S
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func2 time：', ts)
    time.sleep(2)


def Dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔2S
    scheduler.add_job(func, 'interval', seconds=2, id='test_job1')
    # 添加任务,时间间隔5S
    scheduler.add_job(func2, 'interval', seconds=3, id='test_job2')
    scheduler.start()
    print('end')


def MonitorSystem():
    print('ok')
    # 获取cpu使用情况
    cpuper = psutil.cpu_percent()
    # 获取内存使用情况：系统内存大小，使用内存，有效内存，内存使用率
    mem = psutil.virtual_memory()
    # 内存使用率
    memper = mem.percent
    # 获取当前时间
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} cpu:{cpuper}%, mem:{memper}%'
    print(line)
    Timer(1, MonitorSystem).start()


def MonitorNetWork():
    # 获取网络收信息
    netinfo = psutil.net_io_counters()
    # 获取当前时间
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} bytessent={netinfo.bytes_sent}, bytesrecv={netinfo.bytes_recv}'

    print(line)


if __name__ == '__main__':
    # 记录当前时间
    print('start time ', datetime.datetime.now())
    MonitorSystem()
    # 记录结束时间
    print('end time ', datetime.datetime.now())
