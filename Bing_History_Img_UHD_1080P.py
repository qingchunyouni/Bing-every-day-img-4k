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
                            src_Temp = ','.join('{0}'.format(x) for x in re.findall(
                                r"(?=[2010-2030]).*?(?=_1920x1080)", Json_fomart['src'])).replace("'", "_")
                            src = ','.join('{0}'.format(x)
                                           for x in re.findall(r"(?<=/).*", src_Temp))
                            # .replace("/", "")
                            # (?<=/O).*?(?=_1920x1080)
                            # (?<=/O).*?(?=_1920x1080)|(?<=/K).*?(?=_1920x1080)
                            #   (?<=(2013|2014|2015|2016|2017|2018|2019|2020|2021|2022)/).*?(?=_1920x1080)
                            alt = Json_fomart['alt']
                            print("src:  "+src)
                            print("alt:  "+alt)
                            # sleep(1.1)
                            # 寻找图片URL并尝试将之更改为高分辨率图片地址
                            UHD_url = "https://cn.bing.com//th?id="+src+"_UHD.jpg"
                            UHD_url_OHR = "https://cn.bing.com//th?id=OHR."+src+"_UHD.jpg"
                            P1080_url = "https://cn.bing.com//th?id="+src+"_1920x1080.jpg"
                            P1080_url_OHR = "https://cn.bing.com//th?id=OHR."+src+"_1920x1080.jpg"
                            if ("OHR" in UHD_url):
                                url = UHD_url
                            else:
                                url = UHD_url_OHR
                             # 获取照片
                            Get_image_UHD = requests.get(
                                url, headers=header, stream=True)
                            saveName_Temp = alt
                            # 格式化可能存在的非法字符串
                            saveName = str(saveName_Temp).replace(
                                '?', '_').replace('，', '_').replace('/', '_').replace('|', '_')
                            SavePath = savepath+"\\"+saveName + ".jpg"
                            if Get_image_UHD.status_code == 200:
                                if (Path(SavePath).is_file()):
                                    print("文件已经存在:   " + SavePath)
                                    del Get_image_UHD
                                else:
                                    open(f'{SavePath}', 'wb').write(
                                        Get_image_UHD.content)
                                    print("文件保存成功：   " + SavePath)
                                    del Get_image_UHD
                            else:
                                if ("OHR" in P1080_url):
                                    url1080 = P1080_url
                                else:
                                    url1080 = P1080_url_OHR

                                Get_image_1080P = requests.get(
                                    url1080, headers=header, stream=True)
                                if Get_image_1080P.status_code == 200:
                                    if (Path(SavePath).is_file()):
                                        print("文件已经存在:   " + SavePath)
                                        del Get_image_1080P
                                    else:
                                        open(f'{SavePath}', 'wb').write(
                                            Get_image_1080P.content)
                                        print("文件保存成功：   " + SavePath)
                                        del Get_image_1080P
                                else:
                                    print("Get Imgs error :" +
                                          str(Get_image_1080P.status_code))


def CheckDirExists(Path):
    if not os.path.exists(Path):
        os.makedirs(Path)


if __name__ == '__main__':
    SavePath = "f:\Bing\imgs1"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"
    }
   #  检查文件夹是否存在
    CheckDirExists(SavePath)
    for x in range(142, 234, 1):
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
