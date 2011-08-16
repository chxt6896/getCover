#!/usr/bin/env python
#Windows����Ҫʹ��gbk����
# -*- coding: gbk -*-
# @author chxt<chxt6896@gmail.com>
# @site   git@github.com:chxt6896/getCover.git
# @date   2011-08-14

import eyeD3, re, os, sys, time, urllib
 
urlread = lambda url: urllib.urlopen(url).read()

class getAlbumCover:
    '''�Ӷ����ȡר���������ݣ���д���Ӧ�� mp3 �ļ�'''

    _eyeD3 = None

    # ���������Լ�ר��������ص� API �͸�ʽ
    _doubanSearchApi    = 'http://api.douban.com/music/subjects?q={0}&max-results=1'
    _doubanCoverPattern3 = 'http://img3.douban.com/spic/s(\d+).jpg'
    _doubanCoverPattern1 = 'http://img1.douban.com/spic/s(\d+).jpg'
    _doubanConverAddr   = 'http://img3.douban.com/lpic/s{0}.jpg'
    #view-source:http://api.douban.com/music/subjects?q=%E6%A2%81%E9%9D%99%E8%8C%B9%20%E5%B4%87%E6%8B%9C&max-results=1
    #view-source:http://api.douban.com/music/subjects?q=%E6%A2%81%E9%9D%99%E8%8C%B9&max-results=1
    #view-source:http://api.douban.com/music/subjects?q=%E5%B4%87%E6%8B%9C&max-results=1
    
    
    artist = '' # �ݳ���
    album  = '' # ר������
    title  = '' # ��������

    def __init__(self, mp3):
        print 'mp3-->',mp3
        self._eyeD3 = eyeD3.Tag()
        # file exists or readable?
        try:
            self._eyeD3.link(mp3)
            self.getFileInfo()
        except:
            print '��ȡ�ļ�����'

    def updateCover(self, cover_file):
        '''����ר���������ļ�'''
        try:
            self._eyeD3.removeImages()
            # cover exists or readable?
            #self._eyeD3.removeLyrics()
            #self._eyeD3.removeComments()
            self._eyeD3.addImage(3, cover_file, u'')
            self._eyeD3.update()
            return True
        except:
            print '�޸��ļ�����'
            return False

    def getFileInfo(self):
        ''' ��ȡר����Ϣ '''
        self.artist = self._eyeD3.getArtist().encode('gbk')
        self.album  = self._eyeD3.getAlbum().encode('gbk')
        self.title  = self._eyeD3.getTitle().encode('gbk')

    def getCoverAddrFromDouban(self, keywords = ''):
        ''' �Ӷ����ȡר������� URL '''
        if not len(keywords):
            keywords = self.artist + ' ' + (self.album or self.title)
            print '[keywords]',keywords

        #��Ҫ�Ƚ�keywords�����gbk�ٱ����utf-8
        request = self._doubanSearchApi.format(urllib.quote(keywords.decode('gbk').encode('utf-8')))
        #print urllib.unquote('%E6%A2%81%E9%9D%99%E8%8C%B9%20%E5%B4%87%E6%8B%9C').decode('utf-8').encode('gbk')
        print '[request]',request
        result  = urlread(request)
        print '[result]',result
        #f = open('C:/Users/Chxt/Desktop/a.txt', 'w+')
        #f.write(result)
        if not len(result):
            return False

        #���_doubanCoverPattern3ƥ�䲻�ɹ�����ƥ��_doubanCoverPattern1
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
    #������Ҫ��ѯ��Ŀ¼���������е�mp3�ļ�
    for i in os.listdir(sys.argv[1]):
    #for i in sys.argv:
        if re.search('.mp3$', i):
            print '���ڴ���:', i,
            handler = getAlbumCover(i)
            if handler.artist and (handler.album or handler.title):
                print '[����]', handler.artist, handler.title,handler.album
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
                        print '[���]'
                    else:
                        print '[ʧ��1]'
                    os.remove(cover_file)
                else:
                    print '[ʧ��2]'
            handler = None
            time.sleep(3) # ��� 3s ����ֹ������ Block

# vim: set et sw=4 ts=4 sts=4 fdm=marker ff=unix fenc=utf8 nobomb ft=python:
