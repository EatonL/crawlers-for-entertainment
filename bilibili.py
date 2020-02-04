import requests
from bs4 import BeautifulSoup
import re 
import sys 
import time
import pandas as pd
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') 

class bilibili(object):
    def __init__(self,url):
        self._url=url
        self._headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self._title=[]
        self._videoHref=[]
        self._authorHref=[]
        self._author = []
        self._playNum = []
        self._viewNum = []
    
    def get_contents(self):
        s = requests.session()
        s.keep_alive = False
        response = s.get(self._url, headers=self._headers)
        response.encoding = response.apparent_encoding
        response=response.text
        allThings = BeautifulSoup(response,"html.parser")
        contents = allThings.find_all('li',class_='rank-item')
        return contents
        
    def catch_data(self):
        contents=self.get_contents()
        pattern1 = re.compile(r'<a\b[^>]+\bhref="([^"]*)"[^>]*>',re.M)
        for i in range(len(contents)):
            href = pattern1.findall(str(contents[i]))
            videoHref = href[0]
            authorHref = 'https:' + href[2]

            info =contents[i].get_text("/d").split('/d')
            '''
            title = info[1]
            playNum = info[2]
            viewNum = info[3]
            author = info[4]
            '''

            self._title.append(info[1])
            self._videoHref.append(videoHref)
            self._authorHref.append(authorHref)
            self._author.append(info[4])
            self._playNum.append(info[2])
            self._viewNum.append(info[3])

    def extract(self):
        self.catch_data()
        ticks = time.strftime("%Y-%m-%d", time.localtime())

        test = pd.DataFrame({'title':self._title,'videoHref':self._videoHref,'author':self._author,'authorHref':self._authorHref,'playNum':self._playNum,'viewNum':self._viewNum})
        path = './bilibili_hits_'+str(ticks)+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)

def main():
    data=bilibili("https://www.bilibili.com/ranking/all/0/0/1")
    data.extract()

if __name__ == '__main__':
    main()         
