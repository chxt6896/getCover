#!/usr/bin/env python
#Windows下需要使用gbk编码
# -*- coding: gbk -*-
# @author chxt<chxt6896@gmail.com>
# @site   git@github.com:chxt6896/getCover.git
# @date   2011-08-14

import eyeD3, re, os, sys, time, urllib
 
urlread = lambda url: urllib.urlopen(url).read()

class getAlbumCover:
    '''从豆瓣获取专辑封面数据，并写入对应的 mp3 文件'''

    _eyeD3 = None

    # 豆瓣搜索以及专辑封面相关的 API 和格式
    _doubanSearchApi    = 'http://api.douban.com/music/subjects?q={0}&max-results=1'
    _doubanCoverPattern3 = 'http://img3.douban.com/spic/s(\d+).jpg'
    _doubanCoverPattern1 = 'http://img1.douban.com/spic/s(\d+).jpg'
    _doubanConverAddr   = 'http://img3.douban.com/lpic/s{0}.jpg'
    #view-source:http://api.douban.com/music/subjects?q=%E6%A2%81%E9%9D%99%E8%8C%B9%20%E5%B4%87%E6%8B%9C&max-results=1
    #view-source:http://api.douban.com/music/subjects?q=%E6%A2%81%E9%9D%99%E8%8C%B9&max-results=1
    #view-source:http://api.douban.com/music/subjects?q=%E5%B4%87%E6%8B%9C&max-results=1
    
    
    artist = '' # 演唱者
    album  = '' # 专辑名称
    title  = '' # 歌曲标题

    def __init__(self, mp3):
        print 'mp3-->',mp3
        self._eyeD3 = eyeD3.Tag()
        # file exists or readable?
        try:
            self._eyeD3.link(mp3)
            self.getFileInfo()
        except:
            print '读取文件错误'

    def updateCover(self, cover_file):
        '''更新专辑封面至文件'''
        try:
            self._eyeD3.removeImages()
            # cover exists or readable?
            #self._eyeD3.removeLyrics()
            #self._eyeD3.removeComments()
            self._eyeD3.addImage(3, cover_file, u'')
            self._eyeD3.update()
            return True
        except:
            print '修改文件错误'
            return False

    def getFileInfo(self):
        ''' 获取专辑信息 '''
        self.artist = self._eyeD3.getArtist().encode('gbk')
        self.album  = self._eyeD3.getAlbum().encode('gbk')
        self.title  = self._eyeD3.getTitle().encode('gbk')

    def getCoverAddrFromDouban(self, keywords = ''):
        ''' 从豆瓣获取专辑封面的 URL '''
        if not len(keywords):
            keywords = self.artist + ' ' + (self.album or self.title)
            print '[keywords]',keywords

        #需要先将keywords解码成gbk再编码成utf-8
        request = self._doubanSearchApi.format(urllib.quote(keywords.decode('gbk').encode('utf-8')))
        #print urllib.unquote('%E6%A2%81%E9%9D%99%E8%8C%B9%20%E5%B4%87%E6%8B%9C').decode('utf-8').encode('gbk')
        print '[request]',request
        result  = urlread(request)
        print '[result]',result
        #f = open('C:/Users/Chxt/Desktop/a.txt', 'w+')
        #f.write(result)
        if not len(result):
            return False

        #如果_doubanCoverPattern3匹配不成功，则匹配_doubanCoverPattern1
        match = re.search(self._doubanCoverPattern3, result, re.IGNORECASE)
        if match:
            pass
        else:
            match = re.search(self._doubanCoverPattern1, result, re.IGNORECASE) 
        print '[match]',match
        if match:
            return self._doubanConverAddr.format(match.groups()[0])
        else:
            return False


if __name__ == "__main__":
    print sys.argv[1]
    #遍历将要查询的目录，搜索所有的mp3文件
    for i in os.listdir(sys.argv[1]):
    #for i in sys.argv:
        if re.search('.mp3$', i):
            print '正在处理:', i,
            handler = getAlbumCover(i)
            if handler.artist and (handler.album or handler.title):
                print '[内容]', handler.artist, handler.title,handler.album
                cover_addr = handler.getCoverAddrFromDouban()
                print '[cover_addr]',cover_addr
                if cover_addr:
                    #cover_file = 'cover.jpg'
                    cover_file = cover_addr.split('/')[-1]
                    print '[cover_file]',cover_file
                    f = file(cover_file, 'wb')
                    f.write(urlread(cover_addr))
                    f.close()
                    if handler.updateCover(cover_file):
                        print '[完成]'
                    else:
                        print '[失败1]'
                    os.remove(cover_file)
                else:
                    print '[失败2]'
            handler = None
            time.sleep(3) # 间隔 3s ，防止被豆瓣 Block

# vim: set et sw=4 ts=4 sts=4 fdm=marker ff=unix fenc=utf8 nobomb ft=python:
