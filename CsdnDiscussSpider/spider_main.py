# -*- coding: utf-8 -*-

import requests
import re

'''
登录CSDN帐号后爬取我的博客评论管理列表

Customer opener Cookie
'''


class CsdnSpider(object):
    def __init__(self):
        self.url_login = "https://passport.csdn.net/v1/register/pc/login/doLogin"
        self.url_feedback = "http://write.blog.csdn.net/feedback/in/"
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer': 'https://passport.csdn.net/login',
            'origin': 'https://passport.csdn.net',
            'content-Type': 'application/json;charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'connection': 'keep-alive',
            'Host': 'passport.csdn.net'
        }
        self.proxies = {
            'https': 'https://111.231.91.104:8888'
        }

    def get_random_webflow_form(self):
        '''
        uaToken 网页js生成
        webUmidToken  网页js生成
        :return: 返回FORM表单流水字典
        '''
        return {'loginType': '1', 'uaToken': '', 'webUmidToken': ''}

    def login(self, user_name=None, password=None):
        '''
        登录CSDN账号
        :param user_name: 用户名
        :param password: 密码
        :return: 返回登陆后的cookie
        '''
        if user_name is None or password is None:
            print('You need use a valied user name and password to login!')
            return None
        post_form = self.get_random_webflow_form()
        post_form['userIdentification'] = user_name
        post_form['pwdOrVerifyCode'] = password
        print(str(post_form))
        try:
            response = requests.post(self.url_login, data=str(post_form), headers=self.header, proxies=self.proxies, verify=False)
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            print(response.text)
            return cookies
        except Exception as e:
            print("login Exception." + str(e))
            return None

    def get_page_feedback_dict(self, cookies=None, page_index=1):
        '''
        获取CSDN我的博客页面的评论管理页面我文章的评论列表（按照评论页数获取）
        :return: {'maxPage'100:, 'dict':[{'article':'xxx', 'url':'xxx', 'commentator':'xxx', 'time':'xxx', 'content':'xxx'}]}
        '''
        content = requests.get(self.url_feedback + str(page_index), proxies=self.proxies, verify=False, cookies=cookies).text
        page_content_search = re.search(re.compile(r'<div class="page_nav"><span>.*?共(\d+)页</span>'), content)
        if page_content_search is not None:
            max_page = re.search(re.compile(r'<div class="page_nav"><span>.*?共(\d+)页</span>'), content).group(1)
            reg_main = re.compile(
                r"<tr class='altitem'>.*?<a href='(.*?)'.*?>(.*?)</a></td><td><a.*?class='user_name' target=_blank>(.*?)</a></td><td>(.*?)</td>.*?<div class='recon'>(.*?)</div></td></tr>",
                re.S)
            main_items = re.findall(reg_main, content)
            dict_list = list()
            for item in main_items:
                dict_list.append({
                    'url': item[0],
                    'article': item[1],
                    'commentator': item[2],
                    'time': item[3],
                    'content': item[4]
                })
            return {'maxPage': max_page, 'dict': dict_list}
        return None

    def run(self, name=None, pwd=None):
        cookies = self.login(name, pwd)

        total_feedback = 0;
        cur_page = 1
        max_page = 1
        while cur_page <= max_page:
            print("start get " + str(cur_page) + " page feedback.")
            page_dict = self.get_page_feedback_dict(cookies=cookies, page_index=cur_page)
            if page_dict is None:
                break
            total_feedback = total_feedback + len(page_dict['dict'])
            max_page = int(page_dict['maxPage'])
            cur_page = cur_page + 1
        print("Finish! Toal valid feedback is:" + str(total_feedback))


if __name__ == "__main__":
    CsdnSpider().run("Your UserName", "Your PassWord")
