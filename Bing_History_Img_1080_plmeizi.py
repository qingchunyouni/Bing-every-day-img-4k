# 用于爬取Bing首页背景，获得UHD+分辨率的图片。
from ast import If
from calendar import month
import requests
import json
import re
from pathlib import Path
import os
from lxml import etree
from time import sleep


def Download_img(header, savepath, ImgStartCount):
    # mkt，非必要，默认根据访问IP地址返回所在地区数据，指定 mkt=ZH-CN 返回中国区数据，其它可选地区：EN-US, JA-JP, EN-AU, EN-UK, DE-DE, EN-NZ, EN-CA（区分大小写）
    # idx = 开始图片位置 n是结束最多8张
    # Test
    url_temp = "http://bing.plmeizi.com/?page={0}"
    url = url_temp.format(ImgStartCount)
    print(url)
    HtmlApi = requests.get(url, headers=header).text
    APIhtml = etree.HTML(str(HtmlApi))
    Sourceclasss = APIhtml.xpath('//html//body//div')
    for Sourceclass in Sourceclasss:
        # print(str(Sourceclass.attrib))
        if str(Sourceclass.attrib) == "{'class': 'list '}":
            listClasss = Sourceclass.xpath('./div')
            for listClass in listClasss:
                # print(str(listClass.attrib))
                if str(listClass.attrib) == "{'class': 'clearfix'}":
                    clearfixClasss = listClass.xpath('./a')
                    for clearfixClass in clearfixClasss:
                        ImgInfos = clearfixClass.xpath('./div/img')
                        for ImgInfo in ImgInfos:
                            TextToJson = str(
                                ImgInfo.attrib).replace(
                                ': "', ": '").replace(
                                ')"', ")'").replace(
                                '"', '_').replace(
                                "': '", '": "').replace(
                                "{'", '{"').replace(
                                "'}", '"}').replace(
                                "', '", '", "').replace(
                                "':", '":').replace(
                                "\\", '_')
                            print(TextToJson)
                            print(ImgInfo.attrib)
                            Json_fomart = json.loads(TextToJson)
                            # Url = "http:" + \
                            #     Json_fomart['src'].replace("-listpic", "")
                            Url = "http://bing.plmeizi.com/view/12"
                            # .replace("/", "")
                            # (?<=/O).*?(?=_1920x1080)
                            # (?<=/O).*?(?=_1920x1080)|(?<=/K).*?(?=_1920x1080)
                            #   (?<=(2013|2014|2015|2016|2017|2018|2019|2020|2021|2022)/).*?(?=_1920x1080)
                            alt = Json_fomart['alt']
                            saveName_Temp = alt
                            print("Url:  "+Url)
                            print("alt:  "+alt)
                            Save_Img(Url, SavePath, saveName_Temp, header)
    # del(HtmlApi)
    # sleep(1.1)
    # 寻找图片URL并尝试将之更改为高分辨率图片地址
    # 获取照片


def Save_Img(Url, SavePath, saveName_Temp, header):

    Get_image = requests.get(Url, headers=header)
    Get_image.encoding = 'utf-8'
    print(Get_image.text)
    # 格式化可能存在的非法字符串
    saveName = str(saveName_Temp).replace(
        '?', '_').replace('，', '_').replace('/', '_').replace('|', '_')
    SavePath = SavePath+"\\"+saveName + "TEST.jpg"
    if Get_image.status_code == 200:
        if (Path(SavePath).is_file()):
            print("文件已经存在:   " + SavePath)
            del Get_image
        else:
            open(f'{SavePath}', 'wb').write(
                Get_image.content)
            print("文件保存成功：   " + SavePath)
            del Get_image
    else:
        print(Get_image.status_code)


def CheckDirExists(Path):
    if not os.path.exists(Path):
        os.makedirs(Path)


if __name__ == '__main__':
    SavePath = "f:\Bing\imgs2"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"
    }
   #  检查文件夹是否存在
    CheckDirExists(SavePath)
    for x in range(148, 234, 1):
        print(x)
        Download_img(header, SavePath, str(x))


# 必应每天都会更新一张背景图片，如果我们想要在自己的网站中每天动态得更新这种图标就需要用到API去请求，必应官方API
# 请求实例：
# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN
# 参数说明：

# 参数名称	是否必需	可选值	参数说明
# format	否	js，xml	返回数据格式，不存在返回xml格式
# idx	否	0（今天），-1（ 截止中明天 （预准备的）），1（截止至昨天，类推（目前最多获取到7天前的图片））	请求图片截止天数
# n	否	1~8	返回请求数量，目前最多一次获取8张
# mkt	否	zh-CN，…	地区
