from redis import Redis
from conf.config import MAX_RANK, FLAG_RANK, RANK_STEP
from conf.config import REDIS_CONFIG
from conf.config import CATEGORYS
# 运行类型(开发\测试\生产)
from conf.config import BASE_TYPE


if __name__ == '__main__':
    # 创建redis连接对象
    sr = Redis(**REDIS_CONFIG[BASE_TYPE])

    for category in CATEGORYS:
        # 保存转换前的category  用于拼接redis数据库中的键
        category_name = category
        # 转换category的信息 用于拼接url
        category = '+'.join(category.split(' ')) if type(category.split(' ')) is list and len(
            category.split(' ')) > 1 else category
        category = '%2c'.join(category.split(',')) if type(category.split(',')) is list and len(
            category.split(',')) > 1 else category
        category = '%26'.join(category.split('&')) if type(category.split('&')) is list and len(
            category.split('&')) > 1 else category
        rank = 1
        while rank < MAX_RANK:
            res = sr.lpush('{}_url'.format(category_name), 'https://junglescoutpro.herokuapp.com/api/v1/sales_estimator?rank={}&category={}&store=us'.format(rank, category))
            if rank < FLAG_RANK:
                rank += 1
            else:
                rank += RANK_STEP
            print(category, rank)