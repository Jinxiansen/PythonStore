# -*- coding:utf-8 -*-
__author__ = 'dadiao'
__date__ = '2017/9/20 下午3:05'

import requests
from bs4 import BeautifulSoup
import os

# Mac 用户只需修改下面路径的用户名(不需要事先创建 mzz 文件夹，会自动生成)， Windows 则修改 MzituDir 为你想存放的路径。
MzituDir = '/Users/用户名/Desktop/mzz'
class meizi():

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self,url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            # print(u'开始保存：', title)
            path = str(title).replace("?", '_')
            self.mkdir(path)
            href = a['href']
            self.html(href)

    def html(self, href):  ##这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        self.headers['referer'] = href
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)  ##调用img函数

    def img(self, page_url):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):  ##这个函数保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'wb')
        f.write(img.content)
        f.close()

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(MzituDir, path))
        if not isExists:
            #print("'u建了一个名字叫做', path, u'的文件夹！'")
            os.makedirs(os.path.join(MzituDir, path))
            os.chdir(os.path.join(MzituDir, path))  ##切换到目录
            return True
        else:
            print("u'名字叫做', path, u'的文件夹已经存在了！'")
            return False

    def request(self, url):  ##这个函数获取网页的response 然后返回
        content = requests.get(url, headers=self.headers)
        return content

Mzitu = meizi()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')


