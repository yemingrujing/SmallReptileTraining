# -*- coding: utf-8 -*-

import requests
from urllib import parse
import xlwt, random, os
from lxml import html

etree = html.etree


class DouBanSpider(object):
    def __init__(self):
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.comment_url = 'https://movie.douban.com/subject/26794435/comments?start=start&limit=20&sort=new_score&status=P&comments_only=1'
        self.login_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
            'Origin': 'https://accounts.douban.com',
            'content-Type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'connection': 'keep-alive',
            'Host': 'accounts.douban.com'
        }
        self.proxies = {
            'https': 'https://111.231.91.104:8888'
        }
        self.agent_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        ]

    def login(self, username, password):
        data = {'ck': '', 'name': username, 'password': password, 'remember': '', 'ticket': ''}
        data = parse.urlencode(data)
        response = requests.post(self.url, headers=self.login_header, data=data, proxies=self.proxies, verify=False, )
        cooikes = requests.utils.dict_from_cookiejar(response.cookies)
        return cooikes

    def getComment(self, cooikes=None):
        start = 0
        w = xlwt.Workbook(encoding='ascii')
        ws = w.add_sheet('短评')
        index = 1
        headers = {
            'User-Agent': random.choice(self.agent_list)
        }
        while True:
            try:
                url = self.comment_url.replace('start', str(start))
                start += 20
                if cooikes is None:
                    req = requests.get(url, headers=headers, proxies=self.proxies)
                else:
                    req = requests.get(url, headers=headers, cooikes=cooikes, proxies=self.proxies)
                respose = req.json()
                sourPre = etree.HTML(respose['html'])
                nodes = sourPre.xpath('//div[contains(@class, "comment-item")]')
                for node in nodes:
                    name = node.xpath('.//span[@class="comment-info"]/a/text()')[0]
                    star = node.xpath('.//span[@class="comment-info"]/span[2]/@class')[0][7]
                    comment = node.xpath('.//div[@class="comment"]/p/span/text()')[0]
                    ws.write(index, 0, index)
                    ws.write(index, 1, name)
                    ws.write(index, 2, star)
                    ws.write(index, 3, comment)
                    index += 1
                if index > 60:
                    break
            except Exception as e:
                print(e)
                break
        dirName = 'F:/py/xls'
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        w.save('%s/%s' % (dirName, 'nezha.xls'))


if __name__ == "__main__":
    # 获取cookie，以获取更多的短评数据
    # cookies = DouBanSpider.login('YOUR USERNAME', 'YOUR PASSWORD')
    DouBanSpider().getComment()
