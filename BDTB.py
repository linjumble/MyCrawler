#coding:utf-8
__author__ = 'lin'

import urllib2
import re

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


class BDTB:

    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.HTTPError, e:
            if hasattr(e):
                print e.reason
                return None

    def getTitle(self, page):
        pattern = re.compile('class="core_title_txt.*?>(.*?)</h3>',re.IGNORECASE | re.DOTALL)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile("max-page=\"(.*?)\"", re.IGNORECASE | re.DOTALL)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, page):
        pattern = re.compile(r'class=\"d_post_content j_d_post_content ">(?P<content>.*?)</div>', re.IGNORECASE | re.DOTALL)
        items = re.findall(pattern, page)
        contesnts = []
        for item in items:
            content = u"\n" + self.tool.replace(item) + u"\n"
            contesnts.append(content.encode('utf-8'))
        return contesnts


    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title+".txt", "w+")
        else:
            self.file = open(self.defaultTitle+".txt","w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = u"\n" + str(self.floor) + u"----------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor+=1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print u"URL失效"
            return
        try:
            print u"该帖子共有" + str(pageNum) + u"页"
            for i in range(1, int(pageNum)+1):
                print u"正在写入第" + str(i) + u"页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print u"写入异常，原因："+e.message
        finally:
            print u"写入完成"


print u"请输入帖子代号"
baseURL = "http://tieba.baidu.com/p/" + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input(u"是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input(u"是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()