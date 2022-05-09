# 用于爬取Bing首页背景，获得UHD+分辨率的图片。
from socket import timeout
import requests
import json
import os
from lxml import etree
# from selenium.webdriver import edge
from selenium import webdriver
import re
import time
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

Browser = webdriver.Edge()
Browser.maximize_window()
Browser.get('https://www.qq.com')


def Download_img(ImgStartCount):
    # mkt，非必要，默认根据访问IP地址返回所在地区数据，指定 mkt=ZH-CN 返回中国区数据，其它可选地区：EN-US, JA-JP, EN-AU, EN-UK, DE-DE, EN-NZ, EN-CA（区分大小写）
    # idx = 开始图片位置 n是结束最多8张
    # Test11
    url_temp = "http://bing.plmeizi.com/?page={0}"
    # url_temp = "http://bing.plmeizi.com/view/{0}"
    url = url_temp.format(ImgStartCount)
    print(url)
    # Browser.refresh()
    # Browser.get(url)
    # Browser.implicitly_wait(5)
    # time.sleep(3)
    Browser.execute_script(
        "window.open('http://bing.plmeizi.com/view/848')")
    time.sleep(5)
    # Browser.refresh()
    # time.sleep(3)
    input_xpath = Browser.find_elements_by_xpath(
        '/html/body/div[2]/div[1]/img')
    action = ActionChains(Browser).move_to_element(input_xpath)  # 移动到该元素
    action.context_click(input_xpath)  # 右键点击该元素
    action.perform()  # 执行
    pyautogui.typewrite(['V'])  # 敲击V进行保存
    # 单击图片另存之后等1s敲回车
    time.sleep(1)
    pyautogui.typewrite(['enter'])
    print(".......")
    # /html/body/div[2]/div[1]/img
    # APIhtml = etree.HTML(str(HtmlApi))
    # Sourceclasss = APIhtml.xpath('//html//body//div')
    # for Sourceclass in Sourceclasss:
    #     # print(str(Sourceclass.attrib))
    #     if str(Sourceclass.attrib) == "{'class': 'list '}":
    #         listClasss = Sourceclass.xpath('./div')
    #         for listClass in listClasss:
    #             # print(str(listClass.attrib))
    #             if str(listClass.attrib) == "{'class': 'clearfix'}":
    #                 clearfixClasss = listClass.xpath('./a')
    #                 for clearfixClass in clearfixClasss:
    #                     ImgInfos = clearfixClass.xpath('./div/img')
    #                     for ImgInfo in ImgInfos:
    #                         TextToJson = str(
    #                             ImgInfo.attrib).replace(
    #                             ': "', ": '").replace(
    #                             ')"', ")'").replace(
    #                             '"', '_').replace(
    #                             "': '", '": "').replace(
    #                             "{'", '{"').replace(
    #                             "'}", '"}').replace(
    #                             "', '", '", "').replace(
    #                             "':", '":').replace(
    #                             "\\", '_')
    #                         print(TextToJson)
    #                         print(ImgInfo.attrib)
    #                         Json_fomart = json.loads(TextToJson)
    #                         # Url = "http:" + \
    #                         #     Json_fomart['src'].replace("-listpic", "")
    #                         Url = "http://bing.plmeizi.com/view/12"
    #                         # .replace("/", "")
    #                         # (?<=/O).*?(?=_1920x1080)
    #                         # (?<=/O).*?(?=_1920x1080)|(?<=/K).*?(?=_1920x1080)
    #                         #   (?<=(2013|2014|2015|2016|2017|2018|2019|2020|2021|2022)/).*?(?=_1920x1080)
    #                         alt = Json_fomart['alt']
    #                         saveName_Temp = alt
    #                         print("Url:  "+Url)
    #                         print("alt:  "+alt)


if __name__ == '__main__':
    SavePath = "f:\Bing\imgs2"

    for x in range(148, 900, 1):
        print(x)
        Download_img(str(x))


# 必应每天都会更新一张背景图片，如果我们想要在自己的网站中每天动态得更新这种图标就需要用到API去请求，必应官方API
# 请求实例：
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN
# 参数说明：

# 参数名称	是否必需	可选值	参数说明
# format	否	js，xml	返回数据格式，不存在返回xml格式
# idx	否	0（今天），-1（ 截止中明天 （预准备的）），1（截止至昨天，类推（目前最多获取到7天前的图片））	请求图片截止天数
# n	否	1~8	返回请求数量，目前最多一次获取8张
# mkt	否	zh-CN，…	地区
