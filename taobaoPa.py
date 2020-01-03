#!/usr/bin/env python
# coding:utf8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import uuid
import web
import json
import threading

chromedriver_path = "chromedriver"  # 改成你的chromedriver的完整路径地址

urls = (
    '/taobao/taobao_crawler', 'taobao_crawler'
)

app = web.application(urls, globals())
browsers = {}


# 定义一个taobao类
class taobao_infos:
    # 对象初始化
    def __init__(self):
        self.url = 'https://login.taobao.com/member/login.jhtml'
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s
    
    def get_qrcode_img(self):
        # 打开网页
        self.browser.get(self.url)
        
        # 等待 密码登录选项 出现
        # password_login = self.wait.until(
        #   EC.presence_of_element_located((By.CSS_SELECTOR, '.J_Static2Quick')))
        # password_login.click()
        self.browser.delete_all_cookies()
        qr_code = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-img img')))
        
        IMAGE_URL = qr_code.get_attribute("src")
        
        uid = uuid.uuid1().hex
        data = {
            "image_url": IMAGE_URL,
            "token": uid
        }
        return data
    
    # 登录淘宝
    def check_login(self):
        self.browser.refresh()
        list_cookies = self.browser.get_cookies()
        print(list_cookies)
        data = {}
        # 刷新页面即可更新cookie
        #self.browser.refresh()
        # 将获取的的所有cookies添加到浏览器
        for cookie in list_cookies:
            cookie_name = cookie['name']
            if cookie_name == "cookie2":
                cookie_value = cookie['value']
                data["cookie2"] = cookie_value
            if cookie_name == "unb":
                cookie_value = cookie['value']
                data["unb"] = cookie_value
                self.close()
    
        return data
    
    def close(self):
        self.browser.close()
        self.browser.quit()


class taobao_crawler:
    
    def fun_timer(self):
        if self.token in browsers.keys():
            taobao = browsers[self.token]
            taobao.close()
            browsers.pop(self.token)


    def GET(self):
        data = web.input()
        
        web.header('Content-Type', 'application/json;charset=UTF-8')
        result = {
            "status":"2000",
            "msg":"success, please scan qrcode in 15s",
            "data":{}
        }
        
        if "action" in data.keys():
            action = data["action"]
            
            if action == "get_qr_code":
                taobao = taobao_infos()
                jobj = taobao.get_qrcode_img()
                
                self.token = jobj['token']
                browsers[self.token] = taobao

                timer = threading.Timer(60, self.fun_timer)
                timer.start()
                result['data'] = jobj
            
            elif action == "check_login":
                if "token" in data.keys():
                    self.token = data['token']
                    if self.token in browsers.keys():
                        taobao = browsers[self.token]
                        cookie_jobj = taobao.check_login()
                        if "unb" in cookie_jobj.keys():
                            browsers.pop(self.token)
                            result["data"] = cookie_jobj
                            result["msg"] = "scan qrcode success"
                        else:
                            result["data"] = cookie_jobj
                    else:
                        result["status"] = 4000
                        result["msg"] = "token is invalid or is out of date"
                else:
                    result["status"] = 4003
                    result["msg"] = "token is not found"
            else:
                result["status"] = 4004
                result["msg"] = "action is not found"
                    
        return json.dumps(result)
    
    
    def POST(self):
        self.GET()


if __name__ == "__main__":
    app.run()
