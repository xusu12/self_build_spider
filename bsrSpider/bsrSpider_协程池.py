import sys
import re
import json
import time
import datetime
import psycopg2

from redis import Redis
from gevent import monkey
# 打猴子补丁, 让程序在sleep,socket等一些耗时任务的时候, 自动切换
monkey.patch_all()
from gevent.pool import Pool

from conf.config import CATEGORYS
from conf.config import REDIS_CONFIG
from utils.downloads import get_use_requests

from queue import Queue
# 运行类型(开发\测试\生产)
from conf.config import BASE_TYPE
# 协程的数量
from conf.config import GET_URL_COROUTINE_NUM, GET_DATA_COROUTINE_NUM
from conf.config import DATADB_CONFIG
from conf.config import UPDATE_TABEL_NAME, DRUID_TABEL_NAME

# 从工具包中导入日志类
from utils.util import Logger


class AsinSpider(object):
    def __init__(self, name):
        self.name = name
        self.headers = {
            'Origin': 'https://www.junglescout.com',
            'Referer': 'https://www.junglescout.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        # 创建redis连接对象
        self.sr = Redis(**REDIS_CONFIG[BASE_TYPE])
        # 用于保存预测销量的标志位  初始值不为'< 5'就可以
        self.state = 1
        # 用于redis保存每个分类的排名
        self.rank = 0
        # 创建线程池
        self.pool = Pool()
        # url队列
        self.url_queue = Queue()
        # 创建postpresql连接
        self.conn = psycopg2.connect(**DATADB_CONFIG[BASE_TYPE])
        # 创建游标
        self.cur = self.conn.cursor()

        # 设置日志信息
        self.log_name = sys.argv[0].split('/')[-1].split('.')[0]
        self.info_log = Logger(log_name=self.log_name, log_level='info')
        self.error_log = Logger(log_name=self.log_name, log_level='error')

    def get_data(self, url, category):
        # 从url中提取排名
        rank = re.findall(r'rank=(\d+)&', url)
        # 获取响应数据
        try:
            # 调用utils中的下载器的方法  请求下载数据
            response = get_use_requests({"url": url})
            data = json.loads(response.text)
        except Exception as e:
            self.error_log.error(e)
            data = {}

        # 将数据写入日志文件
        self.info_log.info(data)
        # 提取月销量的数据
        est = data.get('estSalesResult')
        # 将每次获取的预测价格的信息保存到数据中
        self.sr.set('{}_state'.format(category), est)
        # 将每次获取的数据的排名保存到redis
        self.sr.set('{}_rank'.format(category), rank)
        # 从redis中获取预测销量的状态
        self.state = self.sr.get('{}_state'.format(category))

        # 获取当前时间戳
        tm = int(round(time.time() * 1000))
        # 获取当前日期
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        if type(est) == int or est == '< 5':
            # 确定当前的爬虫状态  如果返回的销量数据是数字或者是'< 5' 那么就判定状态是正常  否则就是失败
            state = 1
        elif est == 'N.A.':
            # 如果获取的数据是'N.A.'   那么说明没有拿到正常的数据  就把est的值设置为0
            est = 0
            state = 2
        else:
            state = 2

        # 如果返回的数据不是'< 5' 那就将数据保存到数据库中
        if est != '< 5' and est:
            self.info_log.info(
                '类别是：{}, 爬虫的状态是：{}, 当前时间戳是：{}, 销量排名是：{}, 月销量是：{}'.format(category, state, tm, rank[0], est))
            self.save_date_to_db(category, state, tm, rank[0], est, date)

    def get_url(self, category):
        # 从Redis队列中获取url
        res = self.sr.rpop('{}_url'.format(category))
        # 如果url不为空  就把url添加到内存的队列中
        if res:
            self.url_queue.put(res)

    def save_date_to_db(self, *args):
        try:
            # self.cur.execute(
            #     # 插入数据的表名和数据都是以变量的形式传入
            #     # 插入数据到update表中
            #     "INSERT INTO " + UPDATE_TABEL_NAME + " (CATEGORY, STATE, TM, BSR, MOON_SALE_QTYM) VALUES ( '" + args[
            #         0] + "', '" + str(args[1]) + "', '" + str(args[2]) + "',  '" + args[3] + "', '" + str(
            #         args[4]) + "')");
            self.cur.execute(
                # 插入数据到druid表中
                "INSERT INTO " + DRUID_TABEL_NAME + " (CATEGORY, STATE, TM, BSR, MOON_SALE_QTYM, ADAY) VALUES ( '" +
                args[
                    0] + "', '" + str(args[1]) + "', '" + str(args[2]) + "',  '" + args[3] + "', '" + str(
                    args[4]) + "', '" + args[5] + "')");

            # 提交数据到数据库
            self.conn.commit()
        except Exception as e:
            # 将错误信息保存到日志文件中
            self.error_log.error(e)

    def execute_task_data(self, task, category, count):
        # 创建协程的代码
        for i in range(count):
            if self.url_queue.qsize() > 0:
                url = self.url_queue.get()
                # 使用线程的异步任务
                self.pool.apply_async(task, (url, category))
            else:
                break

    def execute_task_url(self, task, category, count):
        # 创建协程的代码
        for i in range(count):
            # 使用线程的异步任务
            self.pool.apply_async(task, (category,))

    def run(self):
        for category in CATEGORYS:
            # 每一个分类在redis中都对应一个队列  分别取出其中的url获取数据
            while True:
                # 如果获取的响应数据是 < 5  那么后面的url就不用再发送请求
                if self.state == '< 5':
                    # 爬到的数据是 < 5 那么后面的url就不需要了  直接把剩下的队列删除
                    self.sr.delete('{}_url'.format(category))
                    self.sr.delete('{}_state'.format(category))
                    self.state = 0  # 重置状态值
                    break

                self.execute_task_url(self.get_url, category, GET_URL_COROUTINE_NUM)
                time.sleep(0.1)

                if self.url_queue.qsize() == 0:
                    break
                # print(category)
                self.execute_task_data(self.get_data, category, GET_DATA_COROUTINE_NUM)
                time.sleep(0.01)
                self.pool.join()
        # 程序结束  关闭连接
        self.conn.close()


if __name__ == '__main__':
    asin = AsinSpider('销量')
    asin.run()
