#-*- coding: utf-8 -*-
#===========================================================
# Author：Sha0hua
# E-mail:shi.sh@foxmail.com
# Modified Date: 2019-03-14
#===========================================================
import re
import time
import html
import urllib.request as u

#from html.parser import HTMLParser

#from bs4 import BeautifulSoup
class SciA():
    url = ''
    def __init__(self, url):
        page = u.urlopen(url)
        self.html = page.read().decode('utf-8')
        #f.write(self.html)

    def getLink(self):
        html=self.html
        #print (html)
        #reg=r'("https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?")'
        regAudioLink=r'"source":"(https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?)","mediaID":".*?","type":"audio","title":".*?"'
        regAudioLink = re.compile(regAudioLink)
        link_list = re.findall(regAudioLink,html)   #List all newspage link
        AudioLink = str(link_list[0])
        #print (AudioLink)
        return AudioLink

    def getAudio(self):
        print ("On process...")
        audioLink = self.getLink()

        #Audio name preparation:
        regTitle = r'"source":"https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?","mediaID":".*?","type":"audio","title":"(.*?)"'
        regTitle = re.compile(regTitle)
        Title = str(re.findall(regTitle,self.html)[0]).replace(" ","_")
        Title_audio=Title+".mp3"

        #Download audio file:            
        audioPath='.\%s'%Title_audio
        u.urlretrieve(audioLink,audioPath)
        print ("Audio download finished")
        return Title


        #Get Script
    def getScript(self):
        scriptTitle=self.getAudio()
        f=open("%s.log"%scriptTitle,'w', encoding="utf-8")
        #<a href="https://www.scientificamerican.com/podcast/episode/busting-earth-bound-asteroids-bigger-job-than-we-thought/#transcripts-body" class="t_meta transcripts_link" aria-label="Busting Earth-Bound Asteroids Bigger Job Than We Thought transcript">Full Transcript</a>
        regScript=r'<br/><a href="(https://www.scientificamerican.com/podcast/episode/.*?/#transcripts-body)"'
        regScript = re.compile(regScript)
        scriptLink=str(re.findall(regScript,self.html)[0])
        #print (scriptLink)
        scriptPage=u.urlopen(scriptLink).read().decode('utf-8')
        regPsg=r'<p>(.*?)</p>'
        regPsg=re.compile(regPsg)
        psgList=re.findall(regPsg,scriptPage)
        for p in psgList:
            p=str(p)
            p=re.sub(r'<a.*?>', '', p)
            p=p.replace("</a>","").replace("<em>","").replace("<\em>","")          
            p=html.unescape(p)
            f.write(p+"\n")
        print ("Script compiling finished")
        f.close()
      
if __name__ == '__main__':
    File = SciA("https://www.scientificamerican.com/podcasts/")
    #File.getLink()
    #File.getAudio()
    File.getScript()   
    print ("\ndone")
    time.sleep(3)
