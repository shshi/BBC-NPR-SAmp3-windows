#!/usr/bin/python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: KKen.py
# Author：Sha0hua
# E-mail:sha0hua@foxmail.com
# Created Date: 2014-01-17
# Modified Date: 2017-01-06
# Version: 2.0
# Description: Added progess bar while downloading 
#===========================================================
import re
import urllib
import os
import time
import shutil

def mycopytree(src,dst):
    _orig_copystat = shutil.copystat
    shutil.copystat = lambda x, y: x
    shutil.copytree(src, dst)
    shutil.copystat = _orig_copystat

if os.path.exists('c:/Python27/Lib/site-packages/progressbar/'):
    pass
else:
    mycopytree('./4install/python-progressbar-master/progressbar','c:/Python27/Lib/site-packages/progressbar/')

if os.path.exists('c:/Python27/Lib/site-packages/bs4/'):
    pass
else:
    mycopytree('./4install/beautifulsoup4-4.3.2/bs4','c:/Python27/Lib/site-packages/bs4/')

from progressbar import *
class KKen():
    url = ''
    def __init__(self, url):
        self.url = url

    def getLink(self):
        url = self.url
        page = urllib.urlopen(url)
        html = page.read()
        reg = r'<a href="(.*?)" title="(?:(?!视频|词汇).)*?" target="_blank">.*?</a>'
        link_re = re.compile(reg)
        link_list = re.findall(link_re,html)   #List all newspage link
        newspage = str(link_list[1])
        return newspage

    def getMp3(self):
        url = self.getLink()
        page = urllib.urlopen(url)
        global html
        html = page.read()
        reg0 = r"var domain= '(.*?)';"
        Furl0_re = re.compile(reg0)
        Furl0 = re.findall(Furl0_re,html)   #Get 1st part of mp3 link

        reg1 = r'var thunder_url ="(.*?\.mp3)"'
        Furl1_re = re.compile(reg1)
        global Furl1
        Furl1 = re.findall(Furl1_re,html)   #Get 2nd part of mp3 link  
           
        Link_mp3 = str(Furl0[0])+str(Furl1[0])   #Integrate mp3 link

#Download mp3(with progress bar):
        mp3_path= './kekemp3/%s'%Furl1[0].split('/')[-1]

        widgets = ['downloading...', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets)

        def dlProgress(count, blockSize, totalSize):
            if pbar.maxval is None:
                pbar.maxval = totalSize
                pbar.start()
            pbar.update(min(count*blockSize, totalSize))

        if os.path.exists('./kekemp3'):
            if os.path.exists(mp3_path):
                print "no update"
            else:
                urllib.urlretrieve(Link_mp3,mp3_path,reporthook=dlProgress)   #Downlad mp3
                pbar.finish()
                return mp3_path
        else:
            os.makedirs('./kekemp3')
            urllib.urlretrieve(Link_mp3,mp3_path,reporthook=dlProgress)   #Downlad mp3
            pbar.finish()  
            return mp3_path

    def getLrc(self):
        reglrc = r'var jmlrc = "(.*?)";'
        Furlrc_re = re.compile(reglrc)
        Furlrc = re.findall(Furlrc_re,html)
        Link_lrc = "http://www.kekenet.com/"+str(Furlrc[0])
        if os.path.exists('./kekemp3/%s.lrc'%re.split('/|\.',Furlrc[0])[-2]):
            return False
        else:
            lrc_path='./kekemp3/%s.lrc'%re.split('/|\.',Furlrc[0])[-2]
            urllib.urlretrieve(Link_lrc,lrc_path)
            return lrc_path

if __name__ == '__main__':
    print "\nHi, this is Shaohua, the writer of this script, thanks for using it. If there's any problem plz send me email: cell.fantasy@qq.com. Enjoy Learning!\n"
    File1 = KKen("http://www.kekenet.com/broadcast/bbc/") #BBC
    File2 = KKen("http://www.kekenet.com/broadcast/npr/") #NPR
    File3 = KKen("http://www.kekenet.com/broadcast/Science/") #Scientific American
    print "Analyzing BBC data..."
    File1.getMp3()
    File1.getLrc()
    print "Analyzing NPR data..."
    File2.getMp3()
    File2.getLrc()
    #print "Analyzing SA data..."
    #File3.getMp3()
    #File3.getLrc()
    print "\ndone"
    time.sleep(3)
