#!/usr/bin/env python
# coding:utf8

import os
import logging
import time
import json
from time import gmtime, strftime, localtime
import requests
from urllib.parse import quote
from pprint import pprint
from random import *

device_info = '''{"new_user":1,"device_id":69780607228,"iid":89868643417,"uuid":"40d261469000389","device":{"os_api":"25","device_brand":"vivo","os_version":"7.1.2","device_type":"vivo_X9s","serial_number":"679945696041","dpi":"480","resolution":"1080*1920"},"openudid":"359c0f6a46510cc9"}'''
# device_info = '''{"device_id":"69234417243","iid":"82922345047","uuid":"534680619175920","device":{"os_api":"19","device_brand":"VOTO","os_version":"4.4.4","device_type":"VOTO GT7","dpi":"320","resolution":"720*1280"},"openudid":"7b526fa09041593d"}'''
COOKIE_COMMONS_FMT = "install_id=%s; ttreq=1$adc52d5d686086d07aec24b36e617b8d1a80273b; qh[360]=1; odin_tt=%s; sid_guard=%s|1567411874|5184000|Fri,+01-Nov-2019+08:11:14+GMT; uid_tt=%s; sid_tt=%s; sessionid=%s";
VERSION_CODE = "850"
VERSION_NAME = "8.5.0"
UPDATE_VERSION_CODE = "8602"
URL_BASE = "127.0.0.1:8887"
DOUYIN_KOL_USERID = "71453961415"
CHANNEL = "aweGW"

device_jobj = json.loads(device_info)

comonParamDicts = {
    "channel": CHANNEL,
    "aid": "1128",
    "app_name": "aweme",
    "version_code": VERSION_CODE,
    "version_name": VERSION_NAME,
    "manifest_version_code": VERSION_CODE,
    "update_version_code": UPDATE_VERSION_CODE,
    "device_platform": "android",
    "ssmix": "a",
    "language": "zh",
    "app_type": "normal",
    "retry_type": "no_retry",
    "js_sdk_version": "1.19.2.0",
    "mcc_mnc": "46011",
    "tt_data": "a",
    "ac": "wifi",
    
    "device_type": device_jobj["device"]["device_type"],
    "device_brand": device_jobj["device"]["device_brand"],
    "os_api": device_jobj["device"]["os_api"],
    "os_version": device_jobj["device"]["os_version"],
    "resolution": device_jobj["device"]["resolution"],
    "dpi": device_jobj["device"]["dpi"],
    
    "device_id": device_jobj["device_id"],
    "iid": device_jobj["iid"],
    "uuid": device_jobj["uuid"],
    "openudid": device_jobj["openudid"],
}
commonParams = ""

for key in comonParamDicts:
    param = "&{0}={1}".format(key, comonParamDicts[key])
    commonParams = commonParams + param


def build_data(douyinUrl, timestamp):
    encode_url = quote(douyinUrl)
    buildUrl = "http://{0}/douyin?action=as_cp_mas_xgon&url={1}&ts={2}&reverse_version={3}".format(URL_BASE, encode_url,
                                                                                                   timestamp,
                                                                                                   VERSION_CODE)
    headers = {
        "allow_access": "true",
        "user-agent": "douyinfuck"
    }
    dataStr = ""
    pprint(buildUrl)
    result = requests.get(buildUrl, timeout=20, headers=headers)
    if result.status_code == requests.codes.ok:
        dataStr = result.text
    pprint(dataStr)
    return dataStr


def build_data_post(douyinUrl, timestamp):
    buildUrl = "http://{0}/douyin?".format(URL_BASE)
    sessionId = "".join([choice("0123456789ABCDEF") for i in range(32)])
    odin_tt = "".join([choice("0123456789ABCDEF") for i in range(96)])
    uid_tt = "".join([choice("0123456789ABCDEF") for i in range(32)])
    headers = {
        "allow_access": "true",
        "user-agent": "douyinfuck"
    }
    pyload = {
        "action": "as_cp_mas_xgon",
        "url": douyinUrl,
        "ts": timestamp,
        "reverse_version": VERSION_CODE,
        "cookie": "{0}{1}{2}{3}{4}{5}{6}".format(COOKIE_COMMONS_FMT, device_jobj["iid"], odin_tt, sessionId, uid_tt,
                                                 sessionId, sessionId)
    }
    dataStr = ""
    pprint(buildUrl)
    result = requests.post(buildUrl, data=json.dumps(pyload), timeout=20, headers=headers)
    pprint(result);
    if result.status_code == requests.codes.ok:
        dataStr = result.text
    pprint(dataStr)
    return dataStr


def check_kol_info(kol_user_id):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = int(timestamp * 1000)
    
    kol_url = "https://aweme.snssdk.com/aweme/v1/user/?user_id={0}&{1}&_rticket={2}&ts={3}".format(kol_user_id,
                                                                                                   commonParams,
                                                                                                   timestamp_13,
                                                                                                   timestamp_10)
    
    pprint(kol_url)
    result = build_data_post(kol_url, timestamp_10)
    pprint("check_kol_info:" + result)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            douyinJobj = json.loads(dataStr)
            if not douyinJobj["user"]:
                return False, dataJobj["buildUrl"]
            else:
                return True, dataJobj["buildUrl"]
    
    except Exception as e:
        return False, dataJobj["buildUrl"]


def monitor_kol_info(douyinApi):
    i = 3
    isCheck = True
    while (i > 0 & isCheck):
        isCheck, douyinUrl = douyinApi(DOUYIN_KOL_USERID)
        i = i - 1


def check_product(product_id, author_id, sec_author_id):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = timestamp * 1000
    kol_url = "https://aweme-hl.snssdk.com/aweme/v2/shop/promotion/?promotion_id={0}&{1}&product_id={2}&author_id={3}&sec_author_id={4}&_rticket={5}&ts={6}".format(
        product_id + "00", commonParams, product_id, author_id, sec_author_id, timestamp_13, timestamp_10)
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            return True
        else:
            return False;
    
    except Exception as e:
        return False


def check_video_comment(aweme_id, cursor, count):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = str(timestamp_10) + "323"
    kol_url = "https://aweme.snssdk.com/aweme/v2/comment/list/?aweme_id={0}&{1}&count={2}&cursor={3}&_rticket={4}&ts={5}".format(
        aweme_id,
        commonParams, count, cursor, timestamp_13, timestamp_10)
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/860 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            return True
        else:
            return False;
    
    except Exception as e:
        return False


def check_user_post(user_id, cursor, count):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = timestamp * 1000
    kol_url = "https://aweme.snssdk.com/aweme/v1/aweme/post/?user_id={0}&{1}&count={2}&cursor={3}&_rticket={4}&ts={5}".format(
        user_id,
        commonParams, count, cursor, timestamp_13, timestamp_10)
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint('aweme', dataStr)
            return True
        else:
            return False
    
    except Exception as e:
        print(e)
        return False


def check_store(kol_user_id, cursor, count):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = timestamp * 1000
    kol_url = "https://aweme-hl.snssdk.com/aweme/v1/promotion/user/promotion/list/?user_id={0}&{1}&count={2}&cursor={3}&_rticket={4}&ts={5}".format(
        kol_user_id,
        commonParams, count, cursor, timestamp_13, timestamp_10)
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            return True
        else:
            return False;
    
    except Exception as e:
        return False


def check_video(aweme_id):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = timestamp * 1000
    
    kol_url = "https://aweme.snssdk.com/aweme/v1/aweme/detail/?aweme_id={0}&{1}&_rticket={2}&ts={3}".format(aweme_id,
                                                                                                            commonParams,
                                                                                                            timestamp_13,
                                                                                                            timestamp_10)
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            return True
        else:
            return False;
    
    except Exception as e:
        return False


# 检测kol粉丝信息接口
def check_kol_follower(kol_user_id):
    count = 20
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = int(timestamp * 1000)
    
    kol_url = "https://aweme-hl.snssdk.com/aweme/v1/user/follower/list/?user_id={0}&{1}&_rticket={2}&ts={3}&max_time={4}&offset=0&source_type=1" \
              "&address_book_access=2&gps_access=1&count={5}".format(kol_user_id,
                                                                     commonParams,
                                                                     timestamp_13,
                                                                     timestamp_10, timestamp_10, count)
    
    pprint(kol_url)
    result = build_data_post(kol_url, timestamp_10)
    pprint(result)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            douyinJobj = json.loads(dataStr)
            if not douyinJobj["followers"]:
                return False, dataJobj["buildUrl"]
            else:
                return True, dataJobj["buildUrl"]
    
    except Exception as e:
        return False, dataJobj["buildUrl"]


# 检测kol关注信息接口
def check_kol_following(kol_user_id):
    count = 20
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = int(timestamp * 1000)
    
    kol_url = "https://aweme-hl.snssdk.com/aweme/v1/user/following/list/?user_id={0}&{1}&_rticket={2}&ts={3}&max_time={4}&offset=0&source_type=1" \
              "&address_book_access=2&gps_access=1&count={5}".format(kol_user_id,
                                                                     commonParams,
                                                                     timestamp_13,
                                                                     timestamp_10, timestamp_10, count)
    
    pprint(kol_url)
    result = build_data_post(kol_url, timestamp_10)
    pprint(result)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    
    xgorn = dataJobj["XGon"]
    
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/750 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    try:
        result = requests.get(dataJobj["buildUrl"], timeout=20, headers=headers)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            douyinJobj = json.loads(dataStr)
            if not douyinJobj["followings"]:
                return False, dataJobj["buildUrl"]
            else:
                return True, dataJobj["buildUrl"]
    
    except Exception as e:
        return False, dataJobj["buildUrl"]


def search_user(keyword, cursor, count):
    timestamp = time.time()
    timestamp_10 = int(timestamp)
    timestamp_13 = str(timestamp_10) + "323"
    kol_url = "https://aweme.snssdk.com/aweme/v1/discover/search/?{0}&_rticket={1}&ts={2}".format(commonParams, timestamp_13, timestamp_10)
    
    result = build_data_post(kol_url, timestamp_10)
    
    jobj = json.loads(result)
    dataJobj = jobj["data"]
    xgorn = dataJobj["XGon"]
    headers = {
        "Cookie": "install_id={0}".format(device_jobj["iid"]),
        "X-Khronos": str(timestamp_10),
        "sdk-version": "1",
        "X-SS-REQ-TICKET": str(timestamp_13),
        "X-Gorgon": xgorn,
        "User-Agent": "com.ss.android.ugc.aweme/860 (Linux; U; Android 8.1.0; zh_CN; V1829T; Build/N2G47H; Cronet/58.0.2991.0)",
        "Connection": "Keep-Alive",
    }
    formParams = {
        "keyword": keyword,
        "cursor": cursor,
        "count": count,
        "type": "1",
        
        "is_pull_refresh": "0",
        "hot_search": "0",
        "search_source": "",
        "search_id": "",
        "query_correct_type": "1"
    }
    
    try:
        pprint(dataJobj["buildUrl"])
        result = requests.post(dataJobj["buildUrl"], formParams, timeout=20, headers=headers)
        pprint(result)
        if result.status_code == requests.codes.ok:
            dataStr = result.text
            pprint(dataStr)
            return True
        else:
            return False;
    
    except Exception as e:
        return False
    
    
def register_device():
    params = {
        "andid":"076c5e3600f45582", #可随机
        "device_brand": "Android",
        "imei": "359250052187091", #手机imei
        "imsi": "460002010621516", #手机imsi
        "mac": "40:45:da:99:38:3a", #手机网络mac地址
        "device_type":"HammerHead", #手机设备类型
        "ser":"913600345152", #手机序列号
        "os_version":"4.4.4", #手机版本
        "os_api":19, #手机安卓系统api
        "resolution":"1776*1080", #分辨率
        "dpi":"480"
    }

    proxy_url = "http://dy.1918.cn/api/sign/proxy?signkey=b359250052187091aadacb359250ccef"


    result = requests.get(proxy_url, params=params, timeout=20)
    jobj = json.loads(result.text)
    # 传入你的代理
    # params["proxy"] = jobj["proxy"]
    
    douyin_url = "http://127.0.0.1:8080/v1/registerDevice"

        
    pprint(douyin_url)

    result = requests.get(douyin_url, params=params, timeout=20)
    pprint(result.text)


if __name__ == '__main__':
    # monitor_kol_info(check_kol_info)
    # monitor_kol_info(check_kol_follower)
    # monitor_kol_info(check_kol_following)
    # check_video("6716344192462753035")
    # check_store("84990209480", 0, 20)
    # check_product("599193043276", "84990209480", "MS4wLjABAAAAAEtO1dCIZvj4VWbLU4Xce7DgVgsKNMNu88eNR2c2LtY")
    # check_user_post("84990209480", 0, 20)
    # check_video_comment("6716344192462753035", 0, 20)

    # search_video("6716344192462753035", 0, 20)

    # search_user("jack", 0, 20)
    register_device()
    
    # search_general("6716344192462753035", 0, 20)
