#!/usr/bin/env python
# coding:utf8

import json
import time
from pprint import pprint

import requests


def buildCommonParam():
    channel = "YingYongBao"
    timestamp = time.time()
    t = int(timestamp)
    deviceId = "7a750e37-f5a7-3936-9205-2a5c6d7c00c1"
    versionName = "5.31.0"
    device_fingerprint = "2019041010390171f44ab22c92d2b7884ab2f41da2c43a013aa232c7a86002"
    params = {
        "channel": channel,
        "deviceId": deviceId,
        "device_fingerprint": device_fingerprint,
        "device_fingerprint1": device_fingerprint,
        "lang": "zh-Hans",
        "platform": "Android",
        "t": str(t),
        "type": "login",
        "versionName": versionName,
    }
    return params


def searchNote(keyword, authorization):
    params = buildCommonParam()
    params["keyword"] = keyword
    params["filters"] = ""
    params["page"] = str(1)
    params["page_size"] = str(20)
    params["search_id"] = "01776AE76A678E55F8C1C6FE9B5184B0"
    params["sort"] = ""
    params["source"] = "explore_feed"
    params["sid"] = authorization

    paramStr = ""
    for key, value in params.items():
        paramStr = paramStr + key + "=" + value + "&"

    api = "https://www.xiaohongshu.com/api/sns/v8/search/notes?" + paramStr

    arr = {
        "action": "getShield",
        "url": api,
        "deviceId": params["deviceId"],
        "device_fingerprint": params["device_fingerprint"],
        "authorization": authorization
    }
    shield, sign = getShield(arr)
    xhsApi = api + "sign=" + sign
    xhsRequest(xhsApi, shield, params["deviceId"], authorization)


def getSmsCode(phone, authorization):
    params = buildCommonParam()
    params["phone"] = phone
    params["zone"] = "86"

    paramStr = ""
    for key, value in params.items():
        paramStr = paramStr + key + "=" + value + "&"

    api = "https://www.xiaohongshu.com/api/sns/v1/system_service/vfc_code?" + paramStr

    arr = {
        "action": "getShield",
        "url": api,
        "deviceId": params["deviceId"],
        "device_fingerprint": params["device_fingerprint"],
        "authorization": authorization
    }
    shield, sign = getShield(arr)
    xhsApi = api + "sign=" + sign
    xhsRequest(xhsApi, shield, params["deviceId"], authorization)


def xhsRequest(xhsApi, shield, deviceId, authorization):
    # 防止请求频繁
    if shield:
        xhsHeaders = {
            "shield": shield,
            "device_id": deviceId,
            "Authorization": authorization,
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; Redmi 5 Plus MIUI/8.11.2) Resolution/1080*2030 Version/5.31.0 Build/5210121 Device/(Xiaomi;Redmi 5 Plus)"
        }
        proxyUrl = "http://dy.1918.cn/api/sign/proxy?tdsourcetag=s_pctim_aiomsg"
        result = requests.get(proxyUrl, timeout=20)
        pprint(result)

        jobj = json.loads(result.text)
        proxy = jobj["proxy"]
        pprint(proxy)
        # proxies = None

        proxies = {
            'http': 'http://{0}'.format(proxy),
            'https': 'https://{0}'.format(proxy)
        }

        result = requests.get(xhsApi, timeout=20, headers=xhsHeaders, proxies=proxies, verify=True)
        pprint(result.text)


def getShield(arr):
    requestURL = "http://127.0.0.1:9999/fakeXhsParam"

    headers = {
        "allow_access": "true",
        "user-agent": "xhs"
    }

    result = requests.post(requestURL, data=json.dumps(arr), timeout=20, headers=headers)
    pprint(result)
    shield = ""
    if result.status_code == requests.codes.ok:
        dataStr = result.text

        jobj = json.loads(dataStr)
        shield = jobj["data"]["shield"]
        sign = jobj["data"]["sign"]
    pprint(shield)
    return shield, sign


if __name__ == '__main__':
    phone = "13335938860"
    authorization = "session.1566023018517656053845"
    # getSmsCode(phone, authorization)
    keyword = u"电脑"
    searchNote(keyword, authorization)

