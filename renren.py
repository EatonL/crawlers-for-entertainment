import requests
import re  
from bs4 import BeautifulSoup
import pandas as pd
import time

class renren(object):
    def __init__(self,url):
        self.url=url
        self.headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self.top24_title=[]
        self.top24_href=[]
        self.todayplay_title=[]
        self.todayplay_href=[]

    def get_article_url(self):  
        s = requests.session() 
        s.keep_alive = False
        response = s.get(self.url, headers=self.headers)
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
        data_href = [self.url[:-1]+x for x in pattern1.findall(data)]
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
        self.top24_href,self.top24_title = self.clean_data(top24)
        del self.top24_href[0]
        self.todayplay_href, self.todayplay_title = self.clean_data(todayPlay)        

    def extract(self):
        self.run()
        ticks = [time.time()]
        ticks = list(ticks)

        max_length = len(self.top24_title) if len(self.top24_title)>len(self.todayplay_title) else len(self.todayplay_title)

        self.top24_title.extend([""]*(max_length-len(self.top24_title)))
        self.top24_href.extend([""]*(max_length-len(self.top24_href)))
        self.todayplay_title.extend([""]*(max_length-len(self.todayplay_title)))
        self.todayplay_href.extend([""]*(max_length-len(self.todayplay_href)))
        ticks.extend([""]*(max_length-len(ticks)))

        test = pd.DataFrame({'time':ticks,'top24_title':self.top24_title,'top24_href':self.top24_href,'todayplay_title':self.todayplay_title,'today_href':self.todayplay_href})
        print(test)
        path = './renren_'+str(ticks[0])+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)


def main():
    data=renren("http://www.zmz2019.com/")
    data.extract()

if __name__ == '__main__':
    main()