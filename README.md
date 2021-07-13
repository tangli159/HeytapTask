# HeytapTask
欢太商城自动签到脚本


## 已实现功能

* [x] 每日签到
* [x] 每日浏览商品任务
* [x] 每日分享商品任务
* [x] 每日信息推送任务

## 使用方式
### 1.下载本项目
### 2.打开config.json,按说明填写
```json
[
    {
        "cookies": "sa_distinct_id=xxxxxxxxxxxxxxx;TOKENSID=TOKEN_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; xxx Build/xxxxx; wv)",
        "dingtalkWebhook": "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
]
```
注意`json`格式，最后一个要删掉逗号。建议在填写之前，使用[json校验工具](https://www.bejson.com/)进行校验。

注意：不要fork后将个人信息填写到自己仓库`config.json`文件中（不要动这个文件就没事），请下载到本地编辑，以免泄露。

cookies 和 User-Agent 信息请自行在手机登录 `欢太商城` APP后使用抓包工具获取！（具体抓包方式请百度\Google）

# 申明

本项目仅用于学习研究，禁止任何人用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.<br>
如果任何单位或个人认为该项目的脚本可能涉及侵犯其权利，则应及时通知并提供相关证明，我将在收到认证文件后删除相关脚本.
