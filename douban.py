import requests
import json
import time
import pandas as pd
import numpy as np

class douban(object):
    def __init__(self,url_root):
        self.page=0
        self.url_root=url_root
        self.url=[]
        self.movie_title=[]
        self.movie_rate=[]
        self.headers=[{'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0','Connection':'close'},\
                      {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
                      {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
  
    def catch_data(self):
        while True:
            #requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False

            url_visit=self.url_root+'{}'.format(self.page*20)
            time.sleep(np.random.rand()*5)
            file = s.get(url_visit,headers=self.headers[self.page%len(self.headers)]).json()
            print(self.headers[self.page%len(self.headers)])
            self.page+=1
            item_num=len(file['subjects'])
            if item_num<20:
                break
            for i in range(item_num):
                dict=file['subjects'][i]   
                urlname=dict['url']
                self.url.append(urlname)
                title=dict['title']
                self.movie_title.append(title)
                rate=dict['rate']
                self.movie_rate.append(rate)
    
    def extract(self):
        self.catch_data()
        ticks = [time.ctime()]
        ticks = list(ticks)
        ticks.extend([""]*(len(self.url)-len(ticks)))

        test = pd.DataFrame({'time':ticks,'title':self.movie_title,'rate':self.movie_rate,'url':self.url})
        print(test)
        path = './douban_'+str(ticks[0]).replace(':','-')+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)
        return path

def main():
    data=douban("https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=")
    filePath=data.extract()

if __name__ == '__main__':
    main()   
