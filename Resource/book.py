
# -*- coding: utf-8 -*-
# author: Jinxiansen
# Python 3.6 
import requests
from bs4 import BeautifulSoup
import sys
import io
import os
import codecs
import importlib
importlib.reload(sys)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import platform
import json
from contextlib import closing


BookType = 'epub' # epub or txt

HomeURL = 'https://www.ixdzs.com'

#  1 玄幻·奇幻  2 修真·仙侠 3 都市·青春 4 历史·军事 5 网游·竞技 6 科幻·灵异 7 言情·穿越
#  8 耽美·同人 12 侦探·推理 10 武侠小说 9 台言·古言11 古典文学 13 外国文学 
# 14 当代现代 15 童话故事 16 传记纪实 17 韩流青春 18 影视文学 0 其他类别 

# sort/后面的数字对应上面类别
WUXIA = 'https://www.ixdzs.com/sort/1/index_0_0_0_{}.html' #10 -> 武侠 

TestDetailUrl = 'https://www.ixdzs.com/d/153/153616/'

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}

pageIndex = 1

class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def mkDir(path):
	path = path.strip()
	jp = os.path.join(BookType, path)
	isExists = os.path.exists(jp)
	if not isExists:
		print('建了一个名字叫做',path,'的文件夹！')
		os.makedirs(jp)
		os.chdir(jp) # 切换到目录
		return True
	else:
		os.chdir(jp)
		print('名字叫做',path,'的文件夹已经存在了！')
		return False

def requestData(url):
	html = requests.get(url,headers = headers)
	html.encoding='utf-8'
	return html

def swiper(url):
	html = requestData(url)
	soup = BeautifulSoup(html.text,'lxml')
	if soup is None: return

	imgUrl = soup.find('div',class_='d_af fdl').find('img')['src']
	print('图片地址：',imgUrl)

	down = soup.find('div',id = '{}_down'.format(BookType))
	if down is None: return

	a = down.find('a')
	if a is None: return

	ad = ''

	if BookType == 'epub':
		ad = '高速下载'
	else:
		ad = 'TXT全集'

	title = a['title'].split(ad)[0].replace(BookType,'')
	last = a['href']

	ft = ''
	if BookType == 'epub':
		ft = '.epub'
	else:
		ft = '.txt'

	downUrl = HomeURL + last
	print(title,' ',downUrl)

	downLoad(imgUrl,title +'.jpg')

	downLoad(downUrl,title + ft)


def downLoad(url,title):
	with closing(requests.get(url, stream=True)) as response:
		content_size = int(response.headers['content-length'])
		progress = ProgressBar(title, total=content_size,unit="KB", 
			chunk_size=1024, 
			# run_status="正在下载", 
			fin_status="******下载完成*******************")
		with open(title, "wb") as file:
			for data in response.iter_content(chunk_size=1024):
				file.write(data)
				progress.refresh(count=len(data))

def parseURL(url):
	html = requestData(url)
	soup = BeautifulSoup(html.text,'lxml')

	all_class = soup.find_all(class_ = 'list_img')

	if all_class.count == []:
		print('已经爬完。')
		sys.exit(0)

	for c in all_class:
		h = c.find('a')['href']
		detailURL = HomeURL + h
		swiper(detailURL)
	else:
		global pageIndex
		pageIndex += 1
		print('~~~~~~~~~~~~~~~~~~~~下载第{}页~~~~~~~~~~~~~~~~~~~~`'.format(pageIndex))
		parseURL(WUXIA.format(pageIndex))


# 创建目录
mkDir(BookType)

parseURL(WUXIA.format(pageIndex))



