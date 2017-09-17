#!/usr/bin/python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: SciA.py
# Author：Sha0hua
# E-mail:sha0hua@foxmail.com
# Created Date: 2014-01-17
# Modified Date: 2017-01-06
# Version: 2.0
# Description: Added progess bar while downloading
#===========================================================
import re
import urllib
import urllib2
import os
import time
import cookielib
import HTMLParser
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
#from bs4 import BeautifulSoup
class SciA():
    url = ''
    def __init__(self, url):
        self.url = url

    def getLink(self):
        url = self.url
        page = urllib.urlopen(url)
        html = page.read()
        #reg = r'<a class="thumb" href="(.*?)" title=".*?">'
        reg = r'<a href="(https://www.scientificamerican.com/podcast/episode/.*?)">'
        link_re = re.compile(reg)
        link_list = re.findall(link_re,html)   #List all newspage link
        newspage = str(link_list[0])
        return newspage
        #print newspage

    def getMp3(self):
        print "analyzing..."
        url = self.getLink()
        page = urllib.urlopen(url)
        html = page.read()
#        print html
#        reg = r'<a id="mp3Link" href="(.*?)"'
        reg = r'<source src="(.*?)" type="audio/mp3">'

        Mp3_re = re.compile(reg)
        Mp3_list = re.findall(Mp3_re,html)   #Find all mp3 link     
        Mp3_link = "http://www.scientificamerican.com"+str(Mp3_list[0])   #Integrate mp3 link
#        print Mp3_link

#Mp3 name preparation:
        regn = r'<title>(.*?)</title>'
        regn_re = re.compile(regn)
        reg_name = str(re.findall(regn_re,html)[0])+".mp3"

#Download mp3(with progress bar):            
        mp3_path='.\SAmp3\%s'%reg_name

        widgets = ['downloading...', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets)

        def dlProgress(count, blockSize, totalSize):
            if pbar.maxval is None:
                pbar.maxval = totalSize
                pbar.start()
            pbar.update(min(count*blockSize, totalSize))

        if os.path.exists('.\SAmp3'):
            if os.path.exists(mp3_path):
                print "no update"
            else:
                urllib.urlretrieve(Mp3_link,mp3_path,reporthook=dlProgress)   #Downlad mp3
                pbar.finish()
        else:
            os.makedirs('.\SAmp3')
            urllib.urlretrieve(Mp3_link,mp3_path,reporthook=dlProgress)   #Downlad mp3
            pbar.finish()  

    def getPage(self):
        url = self.getLink()
        page = urllib.urlopen(url)
        html = page.read()

#Get HTML file:
        page_path='.\SAmp3\%s.html'%str(re.findall(re.compile(r'<title>(.*?)</title>'),html)[0])
        if os.path.exists(page_path):
#            print "no update"
            return False
        else:
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

            req = urllib2.Request(url)

            operate = opener.open(req)
            msg = operate.read()
            #print msg

            file_object = open(page_path,'w')
            file_object.write(msg)
            file_object.close()

#Get txt file:
        txt_path='.\SAmp3\%s.txt'%str(re.findall(re.compile(r'<title>(.*?)</title>'),html)[0])
        if os.path.exists(txt_path):
            return False
        else:
            f = open(txt_path,'a')
            plus_tag = re.findall(re.compile(r'<p>(.*?)</p>'),html)  #List all text(with tag)
            for i in plus_tag:
                de_tag = re.compile("\<.*?\>").sub('',i).encode("utf-8")   #Remove tags
                f.write('%s\n\n'%HTMLParser.HTMLParser().unescape(de_tag).encode("utf-8"))  #Write Body& unescape 
            f.close()
            return txt_path
'''
#######use beautifulsoup to extract text from page#######
        if os.path.exists(txt_path):
            print "no update"
            return False
        else:
            f = open(txt_path,'a')
            f.write('%s'%soup.find("span",text=re.compile("2017")).get_text())    #Write Date
            f.write('\n%s\n'%soup.title.get_text())                               #Write Title 
            f.write('%s\n'%soup.p.get_text().encode("utf-8"))                     #Write Introduction
            f.write('*'*17)                                                       #Write Delimiter
            for i in soup.find_all('p')[4:10]:
                f.write('%s'%i.get_text().encode("utf-8"))                        #Write Body
            f.close()
            return txt_path
##########################################################
'''

if __name__ == '__main__':
    print "\nHi, this is Shaohua, the writer of this script, thanks for using it. If there's any problem plz send me email: cell.fantasy@qq.com. Enjoy Learning!\n"
    File = SciA("http://www.scientificamerican.com/podcast/60-second-science/")
    File.getLink()
    File.getMp3()
    File.getPage()
    print "\ndone"
    time.sleep(3)
