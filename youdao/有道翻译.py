import random

import requests
import time
import hashlib

url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

transtr = '你好'
salt = str(int(time.time() * 1000) + random.randint(1, 10))  # 获取当前时间戳 毫秒级 再加上一个随机数
print(salt)

md5 = hashlib.md5()
digStr = "fanyideskweb" + transtr + salt + "6x(ZHw]mwzX#u0V7@yfwK"
md5.update(digStr.encode('utf-8'))
sign = md5.hexdigest()
print(sign)

data = {
    "i": transtr,
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": salt,
    "sign": sign,
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_CLICKBUTTION",
    "typoResult": "true",
}

res = requests.post(url, data=data)
print(res.content.decode())
