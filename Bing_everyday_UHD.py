# 用于爬取Bing首页背景，获得UHD+分辨率的图片。
import requests
import json
import re
from pathlib import Path
import os


def Download_img(header, savepath, ImgStartCount):
    # mkt，非必要，默认根据访问IP地址返回所在地区数据，指定 mkt=ZH-CN 返回中国区数据，其它可选地区：EN-US, JA-JP, EN-AU, EN-UK, DE-DE, EN-NZ, EN-CA（区分大小写）
    # idx = 开始图片位置 n是结束最多8张
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=ImgStartCount&n=100&mkt=ZH-CN".replace(
        'ImgStartCount', ImgStartCount)
    print(url)
    HtmlApi = requests.get(url, headers=header).text
    Json_list = json.loads(HtmlApi)
    print(HtmlApi)
    Json_images = Json_list["images"]
    # url = Json_images[0]["url"]
    for Json_image in Json_images:
        print(Json_image)
        urlbase = Json_image['urlbase']
        print("urlbase"+urlbase)
        copyright = Json_image['copyright']
        描述 = ','.join('{0}'.format(x)
                      for x in re.findall(r"([^,]*)，", copyright))
        print(描述)
        title = Json_image['title']
        # 寻找图片URL并尝试将之更改为高分辨率图片地址
        Full_url = "https://cn.bing.com"+urlbase+"_UHD.jpg"
        Get_images = requests.get(Full_url, headers=header, stream=True)
        saveName_Temp = title+"_" + 描述
        # 格式化可能存在的非法字符串
        saveName = str(saveName_Temp).replace('?', '_').replace('，', '_')
        SavePath = savepath+"\\"+saveName + ".jpg"
        if Get_images.status_code == 200:
            if (Path(SavePath).is_file()):
                print("文件已经存在:   " + SavePath)
                del Get_images
            else:
                open(f'{SavePath}', 'wb').write(Get_images.content)
                del Get_images


def CheckDirExists(Path):
    if not os.path.exists(Path):
        os.makedirs(Path)


if __name__ == '__main__':
    SavePath = "f:\Bing\imgs"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"
    }
   #  检查文件夹是否存在
    CheckDirExists(SavePath)
    for x in range(0, 16, 8):
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
