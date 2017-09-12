# coding:utf-8

import platform
import threading
import time

import requests
from bs4 import BeautifulSoup

from meizi import Meizi


class Zhuanti:
    def __init__(self, url):
        self.baseurl = url

    def start(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'refer': ''}
        real_list = []
        num = int(raw_input("要爬多少个呢？"))
        root_dir = raw_input('输入保存位置：')
        tail = '\\' if platform.system() == 'windows' else '/'
        if root_dir[-1] != tail:
            root_dir += tail
        i = 1
        while real_list.__len__() < num:
            response = requests.get(self.baseurl + '/page/' + str(i), headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            tags_of_meizi = soup.find(name='ul', id='pins').find_all('li')
            real_list.extend(tags_of_meizi)
            temp = soup.find('a', string='下一页»')
            if not temp:
                print '这个专题只有%d套图了……我尽量下完这%d套图吧' % (real_list.__len__(), real_list.__len__())
                break
            i += 1
        for tag in real_list[0:num]:
            Meizi(tag.a['href'], root_dir, unicode(tag.span.string)).start()
        while True:
            if threading.activeCount() == 1:
                print '爬完了，快去看看吧'
                break
            time.sleep(0.1)


if __name__ == "__main__":
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    response = requests.get('http://www.mzitu.com/zhuanti', headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    beauties = soup.find('dl', class_='tags').find_all('a')
    for index, a_tag in enumerate(beauties):
        print index + 1, a_tag.text
    num = int(raw_input('告诉我你要找的专题序号：'))
    try:
        url = beauties[num - 1]['href']
    except:
        print '(滑稽）'
        exit('出错了，是不是序号输入有误？')
    zt = Zhuanti(url)
    zt.start()
