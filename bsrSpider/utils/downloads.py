import json
import time
from copy import deepcopy
import os
import requests
from conf.config import BASE_DIR
from fake_useragent import UserAgent

get_ua = lambda location: UserAgent(use_cache_server=False, path=location).random

headers = {
    'Origin': 'https://www.junglescout.com',
    'Referer': 'https://www.junglescout.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}


def get_use_requests(params):
    '''
    :param params: need the dict
    :return:
    '''
    try:
        # 必要参数
        url = params['url']
    except KeyError:
        # 模拟位置参数, 缺则报错
        raise Exception('Required parameter missing: url, user_anget')
    # 用于动态调整参数
    need_param = dict(
        headers=None,
        cookies=None,
        proxies=None,
        verify=None,
        timeout=60,
    )

    # 过滤参数
    need_param = filter_params(need_param=need_param, params=params)
    the_headers = deepcopy(headers)
    try:
        # 设置'User-Agent'
        location = os.path.join(BASE_DIR, 'conf/UAPOND.json')
        the_headers['User-Agent'] = get_ua(location)
        # 检查headers, 设置缺省值
        need_param.setdefault('headers', the_headers)
        need_param['url'] = url
        # print(get_use_requests.__name__, params.get('num'), need_param)
        # 发送请求
        resp = requests.get(** need_param)
        # 返回数据
        return resp
    except Exception as e:
        if "NotFound" in str(e):
            raise Exception("NOT_FOUND")
        raise e


# 参数过滤
def filter_params(need_param=None, params=None):
    if type(need_param) is not dict or type(params) is not dict:
        return
    give_up_params = []
    for param in need_param:
        need_param[param] = params.get(param, None)
    for param in need_param:
        if need_param[param] is None:
            give_up_params.append(param)
    # print(give_up_params)
    for param in give_up_params:
        need_param.pop(param)
    return need_param



