#!/usr/bin/env python
# coding:utf8

import json
import time
from pprint import pprint

import requests


def getSmsCode(phone, deviceId, device_fingerprint, authorization):
	channel = "YingYongBao"

	timestamp = time.time()
	t = int(timestamp)
	versionName = "6.8.0"

	params = {
		"channel": channel,
		"deviceId": deviceId,
		"device_fingerprint": device_fingerprint,
		"device_fingerprint1": device_fingerprint,
		"lang": "zh-Hans",
		"phone": phone,
		"platform": "Android",
		"t": str(t),
		"type": "login",
		"versionName": versionName,
		"zone": "86"
	}

	paramStr = ""
	for key,value in params.items():
		paramStr = paramStr+key+"="+value+"&"


	api = "https://www.xiaohongshu.com/api/sns/v1/system_service/vfc_code?"+paramStr



	arr = {
		"action":"getShield",
		"url":api,
		"deviceId":deviceId,
		"device_fingerprint":device_fingerprint,
		"authorization":authorization
	}
	shield, sign = getShield(arr)
	api = api + "sign=" + sign

	# 防止请求频繁
	time.sleep(60)
	if shield:
		xhsHeaders = {
			"shield": shield,
			"device_id": deviceId,
			"Authorization": authorization,
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; Redmi 5 Plus MIUI/8.11.2) Resolution/1080*2030 Version/5.31.0 Build/5210121 Device/(Xiaomi;Redmi 5 Plus)"
		}
		proxies = {
			"http": "http://127.0.0.1:8888",
			"https": "http://127.0.0.1:8888"
		}

		result = requests.get(api, timeout=20, headers=xhsHeaders, proxies=proxies, verify=False)
		pprint(result.text)


def getShield(arr):
	requestURL = "http://192.168.0.102:8889/fakeXhsParam"

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
	deviceId = "7a750e37-f5a7-3936-9205-2a5c6d7c00c0"
	device_fingerprint = "2019041010390171f44ab22c92d2b7884ab2f41da2c43a013aa232c7a86002"
	phone = "13335938690"
	authorization = "session.1566023018517656053845"
	getSmsCode(phone, deviceId, device_fingerprint, authorization)
