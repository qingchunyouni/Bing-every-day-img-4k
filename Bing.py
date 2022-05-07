# 用于爬取Bing首页背景，获得UHD+分辨率的图片。
import requests
import json
import re

def Download_img(header,savepath,ImgCount):
    # mkt，非必要，默认根据访问IP地址返回所在地区数据，指定 mkt=ZH-CN 返回中国区数据，其它可选地区：EN-US, JA-JP, EN-AU, EN-UK, DE-DE, EN-NZ, EN-CA（区分大小写）
    url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=ImgCount&mkt=ZH-CN".replace('ImgCount',ImgCount)
    print(url)
    HtmlApi = requests.get(url,headers=header).text
    Json_list = json.loads(HtmlApi)
    print(HtmlApi)
    Json_images = Json_list["images"]
    # url = Json_images[0]["url"]
    for Json_image in Json_images:
        print(Json_image)
        urlbase =Json_image['urlbase']
        print("urlbase"+urlbase)
        copyright = Json_image['copyright']
        描述 = ','.join('{0}'.format(x) for x in re.findall(r"([^,]*)，",copyright))
        print(描述)
        title = Json_image['title']
        # 寻找图片URL并尝试将之更改为高分辨率图片地址
        Full_url = "https://cn.bing.com"+urlbase+"_UHD.jpg"
        Get_images = requests.get(Full_url,headers=header,stream=True)
        saveName = title+"_"+ 描述
        if Get_images.status_code==200:
           open(f'{savepath}\{saveName}.jpg','wb').write(Get_images.content)
        del Get_images

if __name__=='__main__':
   SavePath  = "f:\Bing\imgs"
   header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"} 
   Download_img(header,SavePath,"100")





