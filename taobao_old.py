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
    utdid = "XDcBvR7n1a8DALT5WXIbSK58"
    appKey = "21646297"
    timestamp = time.time()
    t = int(timestamp)
    lat = "31.23238"
    lng = "121.477733"
    ttid = '255200@taobao_android_8.1.10'
    deviceId = "AucyHx9-FS4hNHlY6ba9UqxFLl2yO1suEjUIy_ZzqxOd"
    features = "27"
 
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
        "t": t,
        "api": api,
        "data": str(b64Data)
    }
    pprint(postData)
    result = getTaobaoSigns(postData)

    jobj = json.loads(result)
    dataJobj = jobj["data"]

    body = "data=" + quote_plus(data)
    requestUrl = "https://guide-acs.m.taobao.com/gw/{0}/{1}/".format(api, v)
    proxies = None
    proxy = get_proxies()

    proxies = {
      'http': 'http://{0}'.format(proxy),
      'https': 'https://{0}'.format(proxy)
    }
    pprint(quote(dataJobj['miniWua']))
    #HHnB_ULbB0nzunw3V7vW3Bi%2BfwHLGedQiZieQKMckO4IAJoU8CLTSld6SUV909yg7IkpRduEzEl5w4XO43hkLQD31Or%2BFbrui5mErT6CNOTK%2Bz8cQOeFrcxAwEV7ytgIlCUPt
    #HHnB_jJRVu4tsgtJbEfZ0FUAHpigRnqyijmc4wBHEePHxeQW5VHmz2ipi1qP44be0OOgRIqftdpr7yjR8k0vyyRiV9RG2GHQVd%252FsoipcgxKGh3h%252FxFdyI1dMQCtLz2VsHsY3d

    headers = {
        # "Cookie": "WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BNvYcduAiLOG70ho%3D; _w_tb_nick=junges521; lgc=junges521; cookie17=VAFf%2BnzgkJJy; dnk=junges521; munb=700358168; tracknick=junges521; sg=183; _l_g_=Ug%3D%3D; _nk_=junges521; cookie1=U7ekRloujnhaujZRiHXXRwV01%2FgXDe%2F%2FeVVqOsQOWFw%3D; thw=cn; cna=5CFZFtdb4mwCAXxPmPML8Zk7; imewweoriw=36wKPC%2FapAgkzT8WCj1j3M33vsX9FJy0U97tiNzywDU%3D; ockeqeudmj=oSYsKKo%3D; unb=700358168; sn=; uc3=id2=VAFf%2BnzgkJJy&vt3=F8dByuWgmtXoXj148Eg%3D&nk2=CcYsUsfvORNY&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; uc1=existShop=false&cookie14=UoTbmVE6PbLaTg%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie21=W5iHLLyFe3xm; csg=7453f4b4; t=dbad2249b44e187f4492b3974ac9f9e2; skt=4f6f49e40a8ae77e; cookie2=1428ce63b7c9ad1ba7edd8466a30ac1e; uc4=id4=0%40Vhili6I0%2BQn3hYkBe%2BFqF7fGAVg%3D&nk4=0%40C%2FnHPHHuz%2FdYdvcdVSawoERjkEo%3D; _cc_=URm48syIZQ%3D%3D; _tb_token_=e55b7eee5f5e6; sgcookie=d%2FAb8wERA5eD9XxtgZzVOWHnmBDqd69eHHYF0lDpKQ%3D%3D; isg=BAQE85Z6BSQbaLHogbJoA5RG3oD2HSiHqgacUh6lkE-SSaQTRi34Fzroja8L0WDf",
        "x-appkey": appKey,
        "x-devid": deviceId,
        "x-ttid": quote_plus(ttid),
        "x-sign": quote_plus(dataJobj['xSign']),
    
        "x-t": str(t),
        "x-location": quote_plus("{0},{1}".format(lng, lat)),


        "x-mini-wua": dataJobj['miniWua'],
       
        "x-pv": "5.2",
        "x-umt":"PWtLqf9LOi0KwDVtPuMr/puwKhuLF9bP",
  
        "x-features": features,
        "x-app-conf-v": str(19),
        "x-utdid": utdid,

        "User-Agent": "MTOPSDK%2F3.1.0.1+%28Android%3B4.4.4%3BLGE%3BAOSP+on+HammerHead%29",

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
    requestURL = "http://127.0.0.1:8889/fakeAliParam"

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
    data = '''{"detail_v":"3.1.9","exParams":"{\\"URL_REFERER_ORIGIN\\":\\"//item.taobao.com/item.htm?id=585292777603&scm=1007.10088.119722.786_1732_1783_1858_3254_2334_1689_2999&pvid=4fbdd9b5-7fb2-4d59-bbd7-cdedf2fd281f&locate=guessitem-item&spm=a2141.1.guessitemtab_1.0&utparam=%7B%22guessModelVersion%22%3A%22%22%2C%22card_subtype%22%3A%22auction%22%2C%22up_pvid%22%3A%22f3c1cac4-9393-43d2-b192-47d6d607f76a%22%2C%22x_sid_shuffle%22%3A%2237451c0bea7d47005d808e4d33dba5eb%22%2C%22x_object_type%22%3A%22item%22%2C%22matrix_score%22%3A0.0%2C%22mtx_sab%22%3A3%2C%22x_contentad_sid%22%3A%22cc491c0bd2f557005d808e4dc71630a8%22%2C%22miniapp_score%22%3A0.0%2C%22hybrid_score%22%3A0.09671696570202708%2C%22card_type%22%3A%22auction%22%2C%22tpp_buckets%22%3A%2288%230%23119722%2313_88%23110%23786%23923_88%23164%231732%23587_88%23461%231783%23693_88%23332%231858%2347_88%23377%233254%23605_88%23344%231334%23581_88%23432%231689%23249_88%23490%232999%23131_8994%230%23145349%2337_8994%23219%23828%2341_8437%230%23106255%2311_8437%23147%23555%23694_9420%230%23138227%230_9420%231009%233735%2310_9420%23555%232818%23998_14778%230%23141653%2372_14778%23465%231816%23703_14778%231%23141653%231%22%2C%22x_ad_bucketid_shuffle%22%3A%2262552%2C62560%2C62566%2C62569%2C62575%2C62596%2C62604%2C65322%2C62615%2C77207%2C62621%2C239041%2C171029%2C202909%2C242661%2C246578%2C295018%22%2C%22miniapphc_score%22%3A0.0%2C%22mtx_ab%22%3A1%2C%22pvid%22%3A%224fbdd9b5-7fb2-4d59-bbd7-cdedf2fd281f%22%2C%22x_item_ids%22%3A585292777603%2C%22x_contentad_bucketid%22%3A%22116895%2C189982%2C116902%2C116905%2C116909%2C116912%2C116921%2C118999%2C121126%2C171356%2C171360%2C236994%2C242110%2C293013%2C1146678%22%2C%22auction_score%22%3A0.47984389893743223%2C%22x_sytab%22%3A%221001%22%2C%22x_object_id%22%3A585292777603%7D&rmdChannelCode=guessULike\\",\\"appReqFrom\\":\\"detail\\",\\"countryCode\\":\\"CN\\",\\"cpuCore\\":\\"1\\",\\"cpuMaxHz\\":\\"N/A\\",\\"from_NavigationActivity\\":\\"true\\",\\"id\\":\\"585292777603\\",\\"latitude\\":\\"31.232275\\",\\"locate\\":\\"guessitem-item\\",\\"longitude\\":\\"121.477803\\",\\"nick\\":\\"junges521\\",\\"osVersion\\":\\"19\\",\\"phoneType\\":\\"AOSP on HammerHead\\",\\"pvid\\":\\"4fbdd9b5-7fb2-4d59-bbd7-cdedf2fd281f\\",\\"rmdChannelCode\\":\\"guessULike\\",\\"scm\\":\\"1007.10088.119722.786_1732_1783_1858_3254_1334_1689_2999\\",\\"soVersion\\":\\"2.0\\",\\"spm\\":\\"a2141.1.guessitemtab_1.0\\",\\"utdid\\":\\"ACCZ+0h8nwIDAODU409KNbjb\\",\\"utparam\\":\\"{\\\\\\"guessModelVersion\\\\\\":\\\\\\"\\\\\\",\\\\\\"card_subtype\\\\\\":\\\\\\"auction\\\\\\",\\\\\\"up_pvid\\\\\\":\\\\\\"f3c1cac4-9393-43d2-b192-47d6d607f76a\\\\\\",\\\\\\"x_sid_shuffle\\\\\\":\\\\\\"37451c0bea7d47005d808e4d33dba5eb\\\\\\",\\\\\\"x_object_type\\\\\\":\\\\\\"item\\\\\\",\\\\\\"matrix_score\\\\\\":0.0,\\\\\\"mtx_sab\\\\\\":3,\\\\\\"x_contentad_sid\\\\\\":\\\\\\"cc491c0bd2f557005d808e4dc71630a8\\\\\\",\\\\\\"miniapp_score\\\\\\":0.0,\\\\\\"hybrid_score\\\\\\":0.09671696570202708,\\\\\\"card_type\\\\\\":\\\\\\"auction\\\\\\",\\\\\\"tpp_buckets\\\\\\":\\\\\\"88#0#119722#13_88#110#786#923_88#164#1732#587_88#461#1783#693_88#332#1858#47_88#377#3254#605_88#344#1334#581_88#432#1689#249_88#490#2999#131_8994#0#145349#37_8994#219#828#41_8437#0#106255#11_8437#147#555#694_9420#0#138227#0_9420#1009#3735#10_9420#555#2818#998_14778#0#141653#72_14778#465#1816#703_14778#1#141653#1\\\\\\",\\\\\\"x_ad_bucketid_shuffle\\\\\\":\\\\\\"62552,62560,62566,62569,62575,62596,62604,65322,62615,77207,62621,239041,171029,202909,242661,246578,295018\\\\\\",\\\\\\"miniapphc_score\\\\\\":0.0,\\\\\\"mtx_ab\\\\\\":1,\\\\\\"pvid\\\\\\":\\\\\\"4fbdd9b5-7fb2-4d59-bbd7-cdedf2fd281f\\\\\\",\\\\\\"x_item_ids\\\\\\":585292777603,\\\\\\"x_contentad_bucketid\\\\\\":\\\\\\"116895,189982,116902,116905,116909,116912,116921,118999,121126,171356,171360,236994,242110,293013,1146678\\\\\\",\\\\\\"auction_score\\\\\\":0.47984389893743223,\\\\\\"x_sytab\\\\\\":\\\\\\"1001\\\\\\",\\\\\\"x_object_id\\\\\\":585292777603}\\"}","itemNumId":"585292777603"}'''
    v = "6.0"

    api = "mtop.taobao.detail.getdetail"
    gwMtopApi(api, v, data, uid="0", sid="0")


if __name__ == '__main__':
    getTaobaoDetail()

