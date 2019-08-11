# -*-coding:utf-8-*-

# 天堂图片网爬取高质量图片


import urllib.request as urllib2
import random,re,os
from lxml import html
from urllib.parse import quote
from bs4 import BeautifulSoup
from http import cookiejar
import string

'''
# userAgent是爬虫与反爬虫斗争的第一步
ua_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}'''
# 用于模拟http头的User-agent
ua_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]

etree = html.etree
userAgent = random.choice(ua_list)

# 要爬取的关键词，中文编码出错，待解决
Img_Name = '美女'
urlPre = "http://www.ivsky.com/search.php?q=" + Img_Name + "&PageNo="
# 声明一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
# 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
cookieHandler = urllib2.HTTPCookieProcessor(cookie)
# 设置代理，创建ProxyHandler
httpProxyHandler = urllib2.ProxyHandler({"https": "111.231.91.104:8888"})
# 创建opener
opener = urllib2.build_opener(httpProxyHandler, cookieHandler)
# 安装opener
urllib2.install_opener(opener)
# 构造图片页数
pageCount = 1
flag = True
while flag:
    urlPre = quote(urlPre, safe=string.printable)
    requestPre = urllib2.Request(url=urlPre + str(pageCount))
    requestPre.add_header('User-Agent', userAgent)
    # 使用自己安装好的opener
    responsePre = urllib2.urlopen(requestPre)
    sourPre = etree.HTML(responsePre.read())
    aaa = sourPre.xpath('//*[@class="pagelist"]/a/text()')
    pageCount = int(aaa[-2])
    if aaa[-1] != '下一页' or int(aaa[-2]) == 7:
        flag = False

pageNumberS = 0
# 图片总页数，待更新自动获取总页数。
pageCount=1
print('计算完成，关键词为%s的图片总计有%s页' % (Img_Name, pageCount))

print('现在开始下载...')
for p in range(pageCount):
    pageNumberS = pageNumberS + 1
    pageNumber = str(pageNumberS)

    # 构建URL
    url = urlPre + pageNumber

    # 通过Request()方法构造一个请求对象

    request1 = urllib2.Request(url=url)
    # 把头添加进去
    request1.add_header('User-Agent', userAgent)
    # 向指定的url地址发送请求，并返回服务器响应的类文件对象
    response1 = urllib2.urlopen(request1)
    # 服务器返回的类文件对象支持python文件对象的操作方法
    soup1 = etree.HTML(response1.read())
    imageUrls = soup1.xpath('//*[contains(@class, "il_img")]/a/@href')
    dirName = 'F:/py/img'
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    for imageSkipUrl in imageUrls:
        # 可以直接取属性获得href内容 https://bbs.csdn.net/topics/392161042?list=lz
        url2 = 'http://www.ivsky.com' + imageSkipUrl
        request2 = urllib2.Request(url=url2)
        request2.add_header('User_Agent', userAgent)
        response2 = urllib2.urlopen(request2)
        soup2 = BeautifulSoup(response2, "html.parser")
        pattern = re.compile(r"var imgURL='(.*?)';", re.MULTILINE | re.DOTALL)
        # //img.ivsky.com'+imgURL+'?download
        script = soup2.find("script", text=pattern)
        imageUrlFoot = pattern.search(script.text).group(1)
        if len(imageUrlFoot.strip()) != 0:
            imageName = re.search(r"[^/]+(?!.*/)", imageUrlFoot, re.MULTILINE | re.DOTALL).group()

            imageUrl = 'https://img.ivsky.com' + imageUrlFoot
            headers = {
                'Cache-Control': 'no-cahce',
                'Referer': ' https://www.ivsky.com/download_pic.html?picurl=' + imageUrlFoot,
                'Sec-Fetch-Mode': ' no-cors',
                'User-Agent': userAgent
            }
            request = urllib2.Request(url=imageUrl, data=None, headers=headers)
            response = urllib2.urlopen(request)
            data = response.read()
            with open('%s/%s_%s.jpg' % (dirName, pageNumberS, imageName), 'wb') as f:
                f.write(data)
            print('正在下载第%s页第%s张图片，总计%s页' % (pageNumberS, imageName, pageCount))
            print('存储为%s/%s_%s.jpg' % (dirName, pageNumberS, imageName))
print("已经全部下载完毕！")
