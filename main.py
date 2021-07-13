# -*- coding: utf-8 -*-
# @Time    : 2021/7/13
# @Author  : 丶大K丶
# @Email   : k@hwkxk.cn

import requests,json,time,logging,traceback,os,random,notify,datetime

#用户登录全局变量
client = None
session = None
#日志基础配置
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 创建一个handler，用于写入日志文件
# w 模式会记住上次日志记录的位置
fh = logging.FileHandler('./log.txt', mode='a', encoding='utf-8')
fh.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(fh)
# 创建一个handler，输出到控制台
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("[%(asctime)s]:%(levelname)s:%(message)s"))
logger.addHandler(ch)

#读取用户配置信息
def readConfig():
    try:
        #用户配置信息
        with open('./config.json','r') as fp:
            users = json.load(fp)
            return users
    except Exception as e:
        print(traceback.format_exc())
        logging.error('账号信息获取失败错误，原因为: ' + str(e))
        logging.error('1.请检查是否在目录下的config.json添加了账号cookies')
        logging.error('2.填写之前，是否在网站验证过Json格式的正确性。')

#获取个人信息，判断登录状态
def get_infouser(HT_cookies,HT_UA):
    flag = False
    global session
    session = requests.Session()
    headers = {
        'Host': 'www.heytap.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': HT_UA,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': HT_cookies
    }
    response = session.get('https://www.heytap.com/cn/oapi/users/web/member/info', headers=headers)
    response.encoding='utf-8'
    try:
        result = response.json()
        if result['code'] == 200:
            logger.info('=== 欢太商城任务 ===')
            logger.info('【登录成功】: ' + result['data']['realName'])
            flag = True
        else:
            logger.info('【登录失败】: ' + result['errorMessage'])
    except Exception as e:
        print(traceback.format_exc())
        logger.error('【登录】: 发生错误，原因为: ' + str(e))
    if flag:
        return session
    else:
        return False

#任务中心列表，获取任务及任务状态
def taskCenter():
    headers = {
    'Host': 'store.oppo.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'User-Agent': HT_UserAgent,
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'cookie': HT_cookies,
    'referer':'https://store.oppo.com/cn/app/taskCenter/index'
    }
    res1 = client.get('https://store.oppo.com/cn/oapi/credits/web/credits/show', headers=headers)
    res1 = res1.json()
    return res1
        

#每日签到
#位置: APP → 我的 → 签到
def daySign_task():
    try:
        dated = time.strftime("%Y-%m-%d")
        headers = {
        'Host': 'store.oppo.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': HT_cookies,
        'referer':'https://store.oppo.com/cn/app/taskCenter/index'
        }
        client.headers.update(headers)
        res = taskCenter()
        res = res['data']['userReportInfoForm']['gifts']
        for data in res:
            if data['date'] == dated:
                qd = data
        if qd['today'] == False:
            data = "amount=" + str(qd['credits'])
            res1 = client.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately', headers=headers,data=data)
            res1 = res1.json()
            if res1['code'] == 200:
                logger.info('【每日签到成功】: ' + res1['data']['message'])
            else:
                logger.info('【每日签到失败】: ' + res1)
        else:
            print(str(qd['credits']),str(qd['type']),str(qd['gift']))
            data = "amount=" + str(qd['credits']) + "&type=" + str(qd['type']) + "&gift=" + str(qd['gift'])
            res1 = client.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately',  headers=headers,data=data)
            res1 = res1.json()
            if res1['code'] == 200:
                logger.info('【每日签到成功】: ' + res1['data']['message'])
            else:
                logger.info('【每日签到失败】')
        time.sleep(1)
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日签到】: 错误，原因为: ' + str(e))



#浏览商品 10个sku +20 分
#位置: APP → 我的 → 签到 → 每日任务 → 浏览商品
def daily_viewgoods():
    try:
        headers = {
        'clientPackage': 'com.oppo.store',
        'Host': 'msec.opposhop.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': 'okhttp/3.12.12.200sp1',
        'Accept-Encoding': 'gzip',
        'cookie': HT_cookies,
        }
        res = taskCenter()
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '浏览商品':
                qd = data
        if qd['completeStatus'] == 0:
            client.headers.update(headers)
            shopList = client.get('https://msec.opposhop.cn/goods/v1/SeckillRound/goods/3016?pageSize=12&currentPage=1')
            res = shopList.json()
            if res['meta']['code'] == 200:
                for skuinfo in res['detail']:
                    skuid = skuinfo['skuid']
                    print('正在浏览商品ID：', skuid)
                    client.get('https://msec.opposhop.cn/goods/v1/info/sku?skuId='+ str(skuid), headers=headers)
                    time.sleep(5)
                res2 = cashingCredits(qd['marking'],qd['type'],qd['credits'])
                if res2 == True:
                    logger.info('【每日浏览商品】: ' + '任务完成！积分领取+' + str(credits))
                else:
                    logger.info('【每日浏览商品】: ' + "领取积分奖励出错！")
            else:
                ogger.info('【每日浏览商品】: ' + '错误，获取商品列表失败')
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日浏览任务】: 错误，原因为: ' + str(e))

def daily_sharegoods():
    try:
        headers = {
        'clientPackage': 'com.oppo.store',
        'Host': 'msec.opposhop.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': 'okhttp/3.12.12.200sp1',
        'Accept-Encoding': 'gzip',
        'cookie': HT_cookies,
        }
        daySignList = taskCenter()
        res = daySignList
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '分享商品到微信':
                qd = data
        if qd['completeStatus'] == 0:
            count = qd['readCount']
            endcount = qd['times']
            while (count <= endcount):
                client.get('https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_sharegoods', headers=headers)
                count += 1
            res2 = cashingCredits(qd['marking'],qd['type'],qd['credits'])
            if res2 == True:
                logger.info('【每日分享商品】: ' + '任务完成！积分领取+' + str(credits))
            else:
                logger.info('【每日分享商品】: ' + '领取积分奖励出错！')
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日分享商品】: 错误，原因为: ' + str(e))

def daily_viewpush():
    try:
        headers = {
        'clientPackage': 'com.oppo.store',
        'Host': 'msec.opposhop.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': 'okhttp/3.12.12.200sp1',
        'Accept-Encoding': 'gzip',
        'cookie': HT_cookies,
        }
        daySignList = taskCenter()
        res = daySignList
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '点推送消息':
                qd = data
        if qd['completeStatus'] == 0:
            count = qd['readCount']
            endcount = qd['times']
            while (count <= endcount):
                client.get('https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_viewpush', headers=headers)
                count += 1
            res2 = cashingCredits(qd['marking'],qd['type'],qd['credits'])
            if res2 == True:
                logger.info('【每日推送消息】: ' + '任务完成！积分领取+' + str(credits))
            else:
                logger.info('【每日推送消息】: ' + '领取积分奖励出错！')
    except Exception as e:
        print(traceback.format_exc())
        logging.error('【每日推送消息】: 错误，原因为: ' + str(e))


#执行完成任务领取奖励
def cashingCredits(info_marking,info_type,info_credits):
    headers = {
    'Host': 'store.oppo.com',
    'clientPackage': 'com.oppo.store',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'User-Agent': HT_UserAgent,
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'cookie': HT_cookies,
    'Origin': 'https://store.oppo.com',
    'X-Requested-With': 'com.oppo.store',
    'referer':' https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
    }

    data = "marking=" + str(info_marking) + "&type=" + str(info_type) + "&amount=" + str(info_credits)
    res = client.post('https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits', data=data, headers=headers)
    res = res.json()
    if res['code'] == 200:
        return True
    else:
        return False

#腾讯云函数入口
def main(event, context):
    users = readConfig()
    for user in users:
        #清空上一个用户的日志记录
        open('./log.txt',mode='w',encoding='utf-8')
        global client
        global HT_cookies
        global HT_UserAgent
        HT_cookies=user['cookies']
        HT_UserAgent=user['User-Agent']
        #print(user['cookies'],user['User-Agent'])
        client = get_infouser(HT_cookies,HT_UserAgent)

        if client != False:
            daySign_task() #执行每日签到
            daily_viewgoods() #执行每日商品浏览任务
            daily_sharegoods() #执行每日商品分享任务
            daily_viewpush() #执行每日推送消息任务

        if ('dingtalkWebhook' in user) :
            notify.sendDing(user['dingtalkWebhook']) #钉钉推送日记
'''            
        if ('telegramBot' in user) :
            notify.sendTg(user['telegramBot']) #电报Bot推送日记
        if ('pushplusToken' in user) :
            notify.sendPushplus(user['pushplusToken'])  #pushplus推送日记
        if('enterpriseWechat' in user) :
            notify.sendWechat(user['enterpriseWechat'])  #企业微信推送日记
        if('IFTTT' in user) :
            notify.sendIFTTT(user['IFTTT'])
        if('Bark' in user) :
            notify.sendBark(user['Bark'])
'''
#主函数入口
if __name__ == '__main__':
    main("","")
