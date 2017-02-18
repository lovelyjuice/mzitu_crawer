# coding:utf-8
import os
import platform
import threading

import requests
from bs4 import BeautifulSoup


class Meizi(threading.Thread):
    def __init__(self, url, root_dir, model_name):
        threading.Thread.__init__(self)
        self.root_dir = root_dir.decode('utf-8')
        self.model_name = model_name
        self.baseurl = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def run(self):
        temp = True
        if not os.path.exists(self.root_dir + self.model_name):
            os.makedirs(self.root_dir + self.model_name)
        i = 0
        while temp:
            i += 1
            myfunc = self.decorator(requests.get, 3)
            response = myfunc(self.baseurl + '/' + str(i), headers=self.headers)
            if not response:
                continue
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            temp = soup.find('a', string='下一页»')
            zhuti = soup.find('div', class_='main-image')
            if zhuti:
                try:
                    self.download_pic(zhuti.p.a.img['src'], self.root_dir + self.model_name, i)
                except requests.exceptions.ConnectionError, e:
                    print e
        print '抓了一个妹子(๑•̀ㅂ•́)و✧  还剩%d个' % (threading.activeCount() - 2)

    def download_pic(self, url, directory, count):
        split = '\\' if platform.system() == 'windows' else '/'
        final_path = directory + split + str(count) + '.jpg'
        myfunc = self.decorator(requests.get, 3)
        response = myfunc(url, headers=self.headers)
        with open(final_path, 'wb+') as f:
            f.write(response.content)

    @staticmethod
    def decorator(function, times):
        def autoconn(*args, **kwargs):
            again = 0
            while again < times:
                try:
                    response = function(*args, **kwargs)
                    if again != 0:
                        print "重连成功!"
                    break
                except requests.exceptions.ConnectionError, e:
                    again += 1
                    if again == 1:
                        print '网络似乎有点问题，开始重连...'
                    print "尝试进行第%d次重新连接" % again
            if again == times:
                print 'Sorry...重连失败，将跳过该图片'
            return response

        return autoconn
