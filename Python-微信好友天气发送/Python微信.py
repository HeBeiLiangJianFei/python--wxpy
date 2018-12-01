# !/usr/bin/env/python
# _*_coding:utf-8 _*_
# author:LiangJianfei

'''
1.从wxpy获取好友列表
2.创建定时器
3.定时器触发函数
4.函数执行，遍历好友列表
5.好友对象执行带参函数，参数为该好友城市
6.函数中请求百度天气接口，得到该好友对应天气数据，解析处理数据，发送天气信息，完成该对象发送。
7.遍历结束，发送完毕

缺陷：打包为exe文件之后启动失败，原因是定时器找不到trigger，要想解决需要查看Apscheduler相关资料。
解决方法：换一种定时器。
编译器上正常执行。
打包为exe之后，可以很方便发给别人使用。扫码登录后每天早上5：30会自动给所有好友发送效果图中的天气预报

'''

from wxpy import *
import requests
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler #定时框架
bot = Bot(cache_path=True)
#tuling = Tuling(api_key=你的api')#机器人api
def send_weather(location):
#准备url地址
    path ='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'
    url = path % location
    response = requests.get(url)
    result = response.json()
    #如果城市错误就按照濮阳发送天气
    if result['error'] !=0:
        location ='石家庄'
        url = path % location
        response = requests.get(url)
        result = response.json()
    str0 = ('    早上好！这是今天的天气预报！……机器人：PyChatBot\n')
    results = result['results']
    # 取出数据字典
    data1 = results[0]
    # 取出城市
    city = data1['currentCity']
    str1 ='    你的城市: %s\n' % city
    # 取出pm2.5值
    pm25 = data1['pm25']
    str2 ='    Pm值    : %s\n' % pm25
    # 将字符串转换为整数 否则无法比较大小
    if pm25 =='':
        pm25 =0
        pm25 =int(pm25)
    # 通过pm2.5的值大小判断污染指数
    pollution = "pm2.5"
    if 0 <= pm25 <35:
        pollution ='优'
    elif 35 <= pm25 <75:
        pollution ='良'
    elif 75 <= pm25 <115:
        pollution ='轻度污染'
    elif 115 <= pm25 <150:
        pollution ='中度污染'
    elif 150 <= pm25 <250:
        pollution ='重度污染'
    elif pm25 >=250:
        pollution ='严重污染'
    str3 ='    污染指数: %s\n' % pollution
    result1 = results[0]
    weather_data = result1['weather_data']
    data = weather_data[0]
    temperature_now = data['date']
    str4 ='    当前温度: %s\n' % temperature_now
    wind = data['wind']
    str5 ='    风向    : %s\n' % wind
    weather = data['weather']
    str6 ='    天气    : %s\n' % weather
    str7 ='    温度    : %s\n' % data['temperature']
    message = data1['index']
    str8 ='    穿衣    : %s\n' % message[0]['des']
    str9 ='    我很贴心: %s\n' % message[2]['des']
    str10 ='    运动    : %s\n' % message[3]['des']
    str11 ='    紫外线 : %s\n' % message[4]['des']
    str = str0 + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11
    return str

#好友列表
# my_friends = []
my_friends = bot.friends()
my_friends.pop(0)

#发送函数
def send_message():
#给全体好友发送
    for friend in my_friends:
        friend.send(send_weather(friend.city))

#发送成功通知我
    bot.file_helper.send(send_weather('石家庄'))
    bot.file_helper.send('发送完毕')

#定时器
print('star')
sched = BlockingScheduler()
sched.add_job(send_message,'cron',month='1-12',day='1-31',hour=7,minute =00)
sched.start()