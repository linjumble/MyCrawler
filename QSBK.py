# -*- coding:utf-8 -*-
__author__ = 'lin'

import re
import urllib2

class QSBK:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.headers = {'User-Agemt':self.user_agent}
        self.authors = []
        self.contents = []
        self.enable = False
        self.read = 0

    def getPage(self):
        try:
            url = u'http://www.qiushibaike.com/hot/'
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u'连接失败，错误原因：'+e.reason
                return None

    def getPageItems(self):
        pageCode = self.getPage()
        if not pageCode:
            print u'页面加载失败'
            return None
        pattern = re.compile(r'<div class="article block untagged mb15".*?title="(?P<author>.*?)".*?<div class="content">.*?<span>(?P<content>.*?)</span>',re.IGNORECASE | re.DOTALL)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile(r'<br/>')
            text = re.sub(replaceBR, '\n', item[1])
            self.authors.append(item[0])
            self.contents.append(text.strip())
        return pageStories

    def loadPage(self):
        if self.enable == True:
            self.getPageItems()


    def getOneStory(self):
        for content in self.contents:
            print '请输入：\n'
            input = raw_input()
            if input == 'Q':
                self.enable = False
                return
            print self.authors[self.read]+': '+self.contents[self.read]+'\n'
            self.read+=1

    def start(self):
        self.enable = True
        self.loadPage()
        while self.enable:
            self.getOneStory()


spider = QSBK()
spider.start()

