# -*-coding:utf-8-*-

# 天堂图片网爬取高质量图片


import urllib.request as urllib2
import random, re
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import quote
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

userAgent = random.choice(ua_list)

# 要爬取的关键词，中文编码出错，待解决
Img_Name = '美女'
urlPre = "http://www.ivsky.com/search.php?q=" + Img_Name + "&PageNo="
# 设置代理，创建ProxyHandler
httpProxyHandler = urllib2.ProxyHandler({"https": "111.231.91.104:8888"})
# 创建opener
opener = urllib2.build_opener(httpProxyHandler, urllib2.ProxyHandler)
# 安装opener
urllib2.install_opener(opener)
# 构造图片页数
# 利用抛出错误的代码，判断结果小于2也的情况
pageCount1 = 0
pageCount2 = 1
while pageCount2 > pageCount1:
    urlPre = quote(urlPre, safe=string.printable)
    requestPre = urllib2.Request(url=urlPre + str(pageCount2))
    requestPre.add_header('User-Agent', userAgent)
    # 使用自己安装好的opener
    responsePre = urllib2.urlopen(requestPre)
    sourPre = etree.HTML(responsePre.read())
    aaa = sourPre.xpath('//*[@class="pagelist"]/a/text()')
    pageCount1 = int(aaa[-2])
    if aaa[-1] != '下一页':
        break

    print('正在计算总页数，已搜索到第%s页' % pageCount1)
    requestPre1 = urllib2.Request(url=urlPre + str(pageCount1))
    requestPre1.add_header('User-Agent', userAgent)

    responsePre1 = urllib2.urlopen(requestPre1)

    soupPre1 = etree.HTML(responsePre1.read())
    aaa1 = soupPre1.xpath('//*[@class="pagelist"]/a/text()')
    pageCount2 = int(aaa1[-2])

    if aaa1[-1] != '下一页':
        break
if pageCount1 > pageCount2:
    pageCount = pageCount1
else:
    pageCount = pageCount2
# 得用类解决上边代码重复问题


pageNumberS = 0
# 图片总页数，待更新自动获取总页数。
# pageCount=1
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
    response = urllib2.urlopen(request1)
    # 服务器返回的类文件对象支持python文件对象的操作方法
    # html=response.read()
    # print(html.decode('utf-8'))

    # 如出现编码错误，试试这个 response.encoding=('utf-8', 'ignore')

    # .decode('utf-8', 'ignore').replace(u'\xa9', u'')
    soup = BeautifulSoup(response, "html.parser")
    # for i in soup.find_all('div',{'class':'il_img'}):
    img_name = 0
    for i in soup.find_all('div', {'class': {'il_img', }}):
        img_name = img_name + 1
        for ii in i.find_all('a'):
            # 可以直接取属性获得href内容 https://bbs.csdn.net/topics/392161042?list=lz
            url2 = 'http://www.ivsky.com' + ii['href']
            request2 = urllib2.Request(url=url2)
            request2.add_header('User-Agent', userAgent)

            response2 = urllib2.urlopen(request2)
            # response2.encoding=('utf-8', 'ignore')
            soup2 = BeautifulSoup(response2, "html.parser")
            soup22 = soup2.find_all('img', {'id': 'imgis'})

            # url3=soup2.find_all('div',{'class':'bt-green'})
            img_url = re.findall('src="+(.*)"', str(soup22))[0]

            # 这是MAC下的目录
            # urllib2.urlretrieve(img_url,'/Users/lhuibin/py/img/%s%s.jpg' % (pageNumberS,img_name))

            # 这是WIN10HOME下的目录
            urllib2.urlretrieve(img_url, 'C:/py/img/%s%s.jpg' % (pageNumberS, img_name))
            print('正在下载第%s页第%s张图片，总计%s页' % (pageNumberS, img_name, pageCount))
            print('存储为C:/py/img/%s%s.jpg' % (pageNumberS, img_name))

print("已经全部下载完毕！")
