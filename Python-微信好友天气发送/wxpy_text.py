# !/usr/bin/env/python
# _*_coding:utf-8 _*_
# author:LiangJianfei

# from wxpy import *
#
# bot = Bot()
# found = bot.friends()
# print(found)

import requests
location = "石家庄"
path = 'http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'
url = path % location
response = requests.get(url)
result = response.json()

print(result)