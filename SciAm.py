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

class SciA():
    url = ''
    def __init__(self, url):
        page = u.urlopen(url)
        self.html = page.read().decode('utf-8')
        #f.write(self.html)

    def getLink(self):
        print ("in progress...")
        
        html=self.html
        regAudioLink=r'"source":"(https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?)","mediaID":".*?","type":"audio","title":".*?"'
        regAudioLink = re.compile(regAudioLink)
        link_list = re.findall(regAudioLink,html)
        AudioLink = str(link_list[0])
        
        return AudioLink

    def getAudio(self):
        audioLink = self.getLink()
        
        #Audio name preparation:
        regTitle = r'"source":"https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?","mediaID":".*?","type":"audio","title":"(.*?)"'
        regTitle = re.compile(regTitle)
        Title = str(re.findall(regTitle,self.html)[0]).replace(" ","_")
        Title_audio=Title+".mp3"

        #Download audio file:            
        audioPath='%s'%Title_audio
        u.urlretrieve(audioLink,audioPath)
        
        return Title

    def getScript(self):
        scriptTitle=self.getAudio()
        f=open("%s.log"%scriptTitle,'w', encoding="utf-8")
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
            #Delete matched string
            p=re.sub(r'<a.*?>', '', p)
            p=p.replace("</a>","").replace("<em>","").replace("</em>","").replace("<p>","").replace("</p>","")
            #Unescape html-specialized code
            p=html.unescape(p)
            f.write(p+"\n\n")
            if 'The above text is a transcript of this podcast'in p:
                break
        f.close()
      
if __name__ == '__main__':
    File = SciA("https://www.scientificamerican.com/podcasts/")
    #File.getLink()
    #File.getAudio()
    File.getScript()   
    print ("finished")
    time.sleep(3)
