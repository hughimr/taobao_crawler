#!/usr/bin/env python
# coding:utf8
import os

import json
import requests
from urllib import quote
from urllib import quote_plus
from pprint import pprint
import base64
import time


def get_proxies():
    proxy_url = "http://dy.1918.cn/api/sign/proxy"
    data = requests.get(proxy_url)
    jobj = json.loads(data.text)
    return jobj["proxy"]


def gwMtopApi(api, v, data, uid="0", sid="0", method='GET'):
    utdid = "XgAeBL57B3EDAEnXWhoksNr3"
    appKey = "21646297"
    timestamp = time.time()
    t = int(timestamp)
    lat = "31.23238"
    lng = "121.477733"
    ttid = '701186@taobao_android_9.1.0'
    deviceId = "AuDnKGSpKEGSPB671gyRVadwJCu_nedoM2FBO_tO93Xb"
    features = "27"
    pageId = "https://market.m.taobao.com/app/tmall-wireless/group-card-618/pages/cc-shareItem?wh_ttid=native"
    pageName = "market.m.taobao.com/app/tmall-wireless/group-card-618/pages/cc-shareItem"
    b64Data = base64.b64encode(data.encode("utf-8"))
    pprint(b64Data)
    postData = {
        "utdid": utdid,
        "uid": uid,
        "deviceId": deviceId,
        "appKey": appKey,
        "x-features": features,
        "ttid": ttid,
        "location": lng + ',' + lat,
        "v": v,
        "sid": sid,
        "t": str(t),
        "api": api,
        "useWua": "1",
        "data": str(b64Data),
        "pageId": pageId,
        "pageName": pageName
    }
    pprint(postData)
    result = getTaobaoSigns(postData)

    jobj = json.loads(result)
    dataJobj = jobj["data"]

    pprint(dataJobj['x-mini-wua'])
    body = "data=" + quote_plus(data)
    requestUrl = "https://guide-acs.m.taobao.com/gw/{0}/{1}/".format(api, v)
    proxies = None
    #proxy = get_proxies()
    #pprint(proxy)
    #proxies = {
    #  'http': 'http://{0}'.format(proxy),
    #  'https': 'https://{0}'.format(proxy)
    #}


    headers = {
        # "Cookie": "WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BNvYcduAiLOG70ho%3D; _w_tb_nick=junges521; lgc=junges521; cookie17=VAFf%2BnzgkJJy; dnk=junges521; munb=700358168; tracknick=junges521; sg=183; _l_g_=Ug%3D%3D; _nk_=junges521; cookie1=U7ekRloujnhaujZRiHXXRwV01%2FgXDe%2F%2FeVVqOsQOWFw%3D; thw=cn; cna=5CFZFtdb4mwCAXxPmPML8Zk7; imewweoriw=36wKPC%2FapAgkzT8WCj1j3M33vsX9FJy0U97tiNzywDU%3D; ockeqeudmj=oSYsKKo%3D; unb=700358168; sn=; uc3=id2=VAFf%2BnzgkJJy&vt3=F8dByuWgmtXoXj148Eg%3D&nk2=CcYsUsfvORNY&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; uc1=existShop=false&cookie14=UoTbmVE6PbLaTg%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie21=W5iHLLyFe3xm; csg=7453f4b4; t=dbad2249b44e187f4492b3974ac9f9e2; skt=4f6f49e40a8ae77e; cookie2=1428ce63b7c9ad1ba7edd8466a30ac1e; uc4=id4=0%40Vhili6I0%2BQn3hYkBe%2BFqF7fGAVg%3D&nk4=0%40C%2FnHPHHuz%2FdYdvcdVSawoERjkEo%3D; _cc_=URm48syIZQ%3D%3D; _tb_token_=e55b7eee5f5e6; sgcookie=d%2FAb8wERA5eD9XxtgZzVOWHnmBDqd69eHHYF0lDpKQ%3D%3D; isg=BAQE85Z6BSQbaLHogbJoA5RG3oD2HSiHqgacUh6lkE-SSaQTRi34Fzroja8L0WDf",
        "x-appkey": appKey,
        "x-devid": deviceId,
        "x-ttid": quote_plus(ttid),
        "x-sign": quote_plus(dataJobj['x-sign']),
        "x-umt": quote_plus(dataJobj['x-umt']),
        "x-mini-wua": quote_plus(dataJobj['x-mini-wua']),
        "x-sgext": dataJobj['x-sgext'],
        "x-t": str(t),
        "x-location": quote_plus("{0},{1}".format(lng, lat)),
        "x-app-ver": "9.1.0",
        "f-refer": "mtop",
        "x-nq": "WIFI",
        "x-nettype": "WIFI",
        "x-region-channel": "CN",
        "f-refer": "mtop",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "A-SLIDER-Q": "appKey%3D21646297%26ver%3D0",
        "cookie": "cna=oxWHFs4uHn4CAbaVpcgYFEBf; _m_h5_tk=cec03ea8205909a0fa9f4a8ee81f5a4c_1577180533995; _m_h5_tk_enc=48372c254ac45efadd225a5d17f2ccab; l=cBEWVp7qQQcYiNAtBOCwCQKbUz7OSCOAguSJGdDMi_5a71T1p8_Ooj_Mie96VbBd9LTB40Sj2Bp9-etemr_ADhYa2SO1.; isg=BBsbKvCywaOjej1W457VRLixoXYp4C30coPgDQ1Y95ox7DvOlcC_QjluggpHTIfq; csg=c44b7e22; dnk=%5Cu6A21%5Cu7CCA%5Cu7684%5Cu9B45%5Cu5F71; munb=1663056325; sgcookie=R5VSuAIMA5aD9Xx8gI30DKDYu0txcjpfQuAyiWLtvJBg; domain=.taobao.com; enc=1iFZ8vAwFbyDzP2VIvIesi7BRoRAQOP6L%2B%2B%2BE9ZAzzmr3Ve6fNFOXIzoxuNYr8kQX3H%2BgDQQkbTdMRjxaVC6CA%3D%3D",

        "x-bx-version": "6.4.11",
        "x-page-url": quote_plus(pageId),
        "a-orange-q": "appKey=21646297&appVersion=9.1.0&clientAppIndexVersion=1120191120160145573&clientVersionIndexVersion=0",
        "x-page-name": pageName,

        "x-pv": "6.3",
        "x-c-traceid": "XLWkskakX5EDAEAuXveJ2YJy1574237572826005219386",
        "x-features": features,
        "x-app-conf-v": str(19),
        "x-utdid": utdid,

        "c-lauch-info": "0,0,1574237572825,1574233432783,3",
        "User-Agent": "MTOPSDK%2F3.1.1.7+%28Android%3B8.1.0%3BHuawei%3BNexus+6P%29",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "x-bx-version": "6.4.11"
    }

    if uid != "":
        headers["x-uid"] = uid
        headers["x-sid"] = sid

    if method == 'GET':
        requestUrl = "https://trade-acs.m.taobao.com/gw/{0}/{1}/?{2}".format(api, v, body)
        pprint(requestUrl)
        result = requests.get(requestUrl, timeout=20, headers=headers, proxies=proxies, verify=True)

    else:
        result = requests.post(requestUrl, data=body, headers=headers, timeout=20, proxies=proxies, verify=True)

    pprint(result.text)
    if result.status_code == requests.codes.ok:
        pprint(result.text)


def getTaobaoSigns(arr):
    pprint(arr)
    requestURL = "http://111.231.203.16:8066/fakeAliParam"

    headers = {
        "allow_access": "true",
        "user-agent": "douyin"
    }
    data = json.dumps(arr)
    pprint(data)

    result = requests.post(requestURL, data=arr, timeout=20, headers=headers)
    pprint(result)
    dataStr = ""
    if result.status_code == requests.codes.ok:
        dataStr = result.text
    pprint(dataStr)
    return dataStr


def getTaobaoDetail():
    data = '''{"detail_v":"3.3.2","exParams":"{\\"NAV_START_ACTIVITY_TIME\\":\\"1574237572624\\",\\"NAV_TO_URL_START_TIME\\":\\"1574237572567\\",\\"ad_type\\":\\"1.0\\",\\"appReqFrom\\":\\"detail\\",\\"clientCachedTemplateKeys\\":\\"[]\\",\\"container_type\\":\\"xdetail\\",\\"countryCode\\":\\"CN\\",\\"cpuCore\\":\\"8\\",\\"cpuMaxHz\\":\\"1555200\\",\\"dinamic_v3\\":\\"true\\",\\"id\\":\\"595977491862\\",\\"item_id\\":\\"595977491862\\",\\"latitude\\":\\"31.23238\\",\\"locate\\":\\"guessitem-item\\",\\"longitude\\":\\"121.477733\\",\\"osVersion\\":\\"27\\",\\"phoneType\\":\\"Nexus+6P\\",\\"pvid\\":\\"cade2b68-2075-43e3-80e4-2485fecbfc76\\",\\"rmdChannelCode\\":\\"guessULike\\",\\"scm\\":\\"1007.10088.149221.786_1735_1783_1860_2038_1467_1342_1689_4631_4315_2999\\",\\"soVersion\\":\\"2.0\\",\\"spm\\":\\"a2141.1.guessitemtab_1.2\\",\\"spm-cnt\\":\\"a2141.7631564\\",\\"ultron2\\":\\"true\\",\\"utdid\\":\\"XLWkskakX5EDAEAuXveJ2YJy\\"}","itemNumId":"595977491862"}'''
    v = "6.0"

    api = "mtop.taobao.detail.getdetail"
    gwMtopApi(api, v, data, uid="1663056325", sid="5e11550dfed95881d17ee715df3ffe91")


if __name__ == '__main__':
    getTaobaoDetail()
    api = "mtop.taobao.wireless.amp2.im.message.send"
    v = "1.0"
    timestamp = int(time.time())
    t = str(timestamp)+"123"
    pprint(timestamp)
    data = '''{"accessKey":"taobao-app","accessSecret":"taobao-app-secret","bizType":"14","entityId":"0_G_2206965260698#3_1576296399309_0_2206965260698#3","entityType":"G","messages":"[{\\"templateData\\":\\"{\\\\\\"text\\\\\\":\\\\\\"123\\\\\\"}\\",\\"templateId\\":101,\\"bizUnique\\":\\"0_G_2206965260698#3_1576296399309_0_2206965260698#3_1576316146812_791796116\\",\\"summary\\":\\"123\\",\\"ext\\":{\\"bizChainID\\":null,\\"messageSource\\":2}}]","sdkVersion":"1.0.0"}'''
    pprint(data)
    jobj = json.loads(data)
    # entityId = jobj["entityId"]
    # messages = jobj["messages"]
    # mjobj = json.loads(messages)
    #gwMtopApi(api, v, data, uid="700358168", sid="96d58db05c3654c6015572075f9e41ea", method="POST")
