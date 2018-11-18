import requests
url = 'https://junglescoutpro.herokuapp.com/api/v1/sales_estimator?rank=1&category=Appliances&store=us'
refer = 'https://www.junglescout.com/'
headers = {'Referer': 'https://www.junglescout.com/',}
res = requests.get(url, headers=headers)
print(res.text)