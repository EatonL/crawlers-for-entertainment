import requests
import re  
from bs4 import BeautifulSoup
import pandas as pd
import time

class renren(object):
    def __init__(self,url):
        self._url=url
        self._headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self._top24Title=[]
        self._top24Href=[]
        self._todayplayTitle=[]
        self._todayplayHref=[]

    def get_article_url(self):  
        s = requests.session() 
        s.keep_alive = False
        response = s.get(self._url, headers=self._headers)
        response.encoding = response.apparent_encoding
        response=response.text

        a = BeautifulSoup(response,"html.parser")
        find_top24 = a.find_all('div',class_='fl box top24')  
        find_todayPlay = a.find_all("div",class_="fr today-play")
        return find_top24, find_todayPlay

    def clean_data(self,data):
        data = str(data)
        pattern1 = re.compile(r'<a\b[^>]+\bhref="([^"]*)"[^>]*>',re.M)
        pattern2 = re.compile(r'<a\b[^>]+\btitle="([^"]*)"[^>]*>',re.M)
        data_href = [self._url[:-1]+x for x in pattern1.findall(data)]
        data_title = pattern2.findall(data)

        for x in range(len(data_href)-1,-1,-1):
            result = '/resource/' in data_href[x]        
            if result == False:
                data_href.remove(data_href[x])
            elif result == True:
                pass
        return data_href, data_title
    
    def run(self):
        top24,todayPlay = self.get_article_url()
        self._top24Href,self._top24Title = self.clean_data(top24)
        del self._top24Href[0]
        self._todayplayHref, self._todayplayTitle = self.clean_data(todayPlay)        

    def extract(self):
        self.run()
        ticks = [time.time()]
        ticks = list(ticks)

        max_length = len(self._top24Title) if len(self._top24Title)>len(self._todayplayTitle) else len(self._todayplayTitle)

        self._top24Title.extend([""]*(max_length-len(self._top24Title)))
        self._top24Href.extend([""]*(max_length-len(self._top24Href)))
        self._todayplayTitle.extend([""]*(max_length-len(self._todayplayTitle)))
        self._todayplayHref.extend([""]*(max_length-len(self._todayplayHref)))
        ticks.extend([""]*(max_length-len(ticks)))

        test = pd.DataFrame({'time':ticks,'top24_title':self._top24Title,'top24_href':self._top24Href,'todayplay_title':self._todayplayTitle,'today_href':self._todayplayHref})
        print(test)
        path = './renren_'+str(ticks[0])+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)


def main():
    data=renren("http://www.rrys2019.com/")
    data.extract()

if __name__ == '__main__':
    main()
