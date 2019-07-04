#-*- coding: utf-8 -*-
#===========================================================
# Author：Sha0hua
# E-mail:shi.sh@foxmail.com
# Modified Date: 2019-03-26
# Version Description: fixed file naming bug
#===========================================================
import re
import sys
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
        print ("Hi, this is Shaohua, the author of this toy, if there's any thing I can help, please contact me via shi.sh@foxmail.com. Enjoy!\n")
        print ("initiating...")
      
        html=self.html
        regAudioLink=r'"source":"(https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?)","mediaID":".*?","type":"audio","title":".*?"'
        regAudioLink = re.compile(regAudioLink)
        link_list = re.findall(regAudioLink,html)
        AudioLink = str(link_list[0])
        #print (AudioLink)
        
        return AudioLink

    def report_hook(self, count, block_size, total_size):
        #count: downloaded size of block; block_size: size of block; total_size: size of file
        _output=sys.stdout
        #print (count, block_size, total_size)  
        _output.write(f'\rprogress: %d%%' %(100.0 * count * block_size/ total_size))

    def getAudio(self):
        audioLink = self.getLink()
        
        #Audio name preparation:
        regTitle = r'"source":"https://flex.acast.com/www.scientificamerican.com/podcast/podcast.mp3\?fileId=.*?","mediaID":".*?","type":"audio","title":"(.*?)"'
        regTitle = re.compile(regTitle)
        #Title = str(re.findall(regTitle,self.html)[0]).replace(" ","_")
        Title = str(re.findall(regTitle,self.html)[0])
        illegal_str=['?', '*', ':', '"', '<', '>', '\\', '/', '|']
        if any(x in Title for x in illegal_str):
            regTitle=r'<br/><a href="https://www.scientificamerican.com/podcast/episode/(.*?)/#transcripts-body"'
            regTitle = re.compile(regTitle)
            Title=str(re.findall(regTitle,self.html)[0])
        Title_audio=Title+".mp3"

        #Download audio file:            
        audioPath='%s'%Title_audio
        u.urlretrieve(audioLink, audioPath, reporthook=self.report_hook)
        
        return audioLink, Title

    def getScript(self):
        (audioLink, scriptTitle)= self.getAudio()

        f=open("%s.log"%scriptTitle,'w', encoding="utf-8")
        f.write("Title: "+scriptTitle+"\n\n")
        regScript=r'<br/><a href="(https://www.scientificamerican.com/podcast/episode/.*?/#transcripts-body)"'
        regScript = re.compile(regScript)
        scriptLink=str(re.findall(regScript,self.html)[0])
        #print (scriptLink)
        scriptPage=u.urlopen(scriptLink).read().decode('utf-8')
        regPsg=r'<p>(.*?)</p>'
        regPsg=re.compile(regPsg)
        psgList=re.findall(regPsg,scriptPage)
        #print (psgList)
        for p in psgList:
            p=str(p)
            #Delete matched string
            p=re.sub(r'<.*?>', '', p)
            #p=p.replace("</a>","").replace("<em>","").replace("</em>","").replace("<p>","").replace("</p>","")
            #Unescape html-specialized code
            p=html.unescape(p)
            f.write(p+"\n\n")
            if 'The above text is a transcript of this podcast'in p:
                break
        f.write('Script link: %s\n'%scriptLink)
        f.write('Audio link: %s'%audioLink)
        f.close()
      
if __name__ == '__main__':
    File = SciA("https://www.scientificamerican.com/podcasts/")
    #File.getLink()
    #File.getAudio()
    File.getScript()
    print ("\nfinished")
    time.sleep(3)
