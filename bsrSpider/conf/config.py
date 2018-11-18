import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')
# print(LOG_DIR)
LOG_TEM_DEBUG = (
'GMT+8:%(asctime)s, PID:%(process)d, TID:[%(thread)d %(threadName)s, LEV:%(levelno)s %(levelname)s, MSG:, %(message)s',
'%Y-%m-%d %H:%M:%S')
LOG_TEM_INFO = ('GMT+8:%(asctime)s, TID:%(thread)d %(threadName)s, MSG:, %(message)s', '%Y-%m-%d %H:%M:%S')
LOG_TEM_DB = ('GMT+8:%(asctime)s, TID:%(thread)d %(threadName)s, MSG:, %(message)s', '%Y-%m-%d %H:%M:%S')
LOG_TEM_ERROR = (
'GMT+8:%(asctime)s, PID:%(process)d, TID:%(thread)d %(threadName)s, LEV:%(levelno)s %(levelname)s, MSG:, %(message)s',
'%Y-%m-%d %H:%M:%S')

BASE_TYPE = 'develop'
# BASE_TYPE = 'test'
# BASE_TYPE = 'production'

# 每个分类获取数据的最大的排名
MAX_RANK = 10

# 设置一个排名的标志位  在这个标志位之前的排名每个都需要获取  在这个标志位之后的排名按照指定步长获取数据
FLAG_RANK = 5

# 设置一个步长 在标志位之后  按照步长来爬取数据
RANK_STEP = 2

# 设置保存到的postpresql数据库中表的名字
# 更新表 只存一份数据
UPDATE_TABEL_NAME = 'AMAZON_BSR_QTY'
# 历史表 保存历史数据  每次爬取都按照日期存储一份
DRUID_TABEL_NAME = 'AMAZON_DRUID_BSR_QTY'

# 设置从redis获取url的协程的数量
GET_URL_COROUTINE_NUM = 5

# 设置获取数据的协程的数量
GET_DATA_COROUTINE_NUM = 5

# redis配置
REDIS_CONFIG = {
    "develop": dict(
        host='127.0.0.1',
        port=6379,
        db=2,
        decode_responses=True,
    ),
    "test": dict(
        host='192.168.0.149',
        port=6379,
        db=3,
        decode_responses=True,
    ),
    "production": dict(
        host='192.168.0.149',
        port=6379,
        db=4,
        decode_responses=True,
    )
}

# postpresql数据库配置
DATADB_CONFIG = {
    "develop": dict(
        database='ic_crawler',
        user='postgres',
        password='123456',
        host='192.168.13.8',
        port='15432'
    ),
    "test": dict(
        database='ic_crawler',
        user='postgres',
        password='123456',
        host='192.168.0.149',
        port='15432'
    ),
    'production': dict(
        database='ic_crawler_online',
        user='postgres',
        password='123456',
        host='192.168.0.149',
        port='15432'
    )
}

# categorys分类信息
CATEGORYS = [
    "Appliances",
    "Arts, Crafts & Sewing",
    "Automotive",
    "Baby",
    "Beauty",
    "Beauty & Personal Care",
    "Books",
    "Camera & Photo",
    "Cell Phones & Accessories",
    "Clothing, Shoes & Jewelry",
    "Computers & Accessories",
    "Electronics",
    "Grocery & Gourmet Food",
    "Health & Household",
    "Home & Garden",
    "Home & Kitchen",
    "Home Improvement",
    "Industrial & Scientific",
    "Kindle Store",
    "Kitchen & Dining",
    "Music",
    "Musical Instruments",
    "Office Products",
    "Patio, Lawn & Garden",
    "Pet Supplies",
    "Software",
    "Sports & Outdoors",
    "Toys & Games",
    "Video Games",
    "Watches"
]
