import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

class steam(object):
    def __init__(self,url,file_name,discount):
        self._url=url
        self._fileName=file_name
        self._discount=discount
        self._gameUrl=[]
        self._gameName=[]
        self._gamePrice=[]
        self._publishDate=[]
        self._headers = [{'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'},
                        {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
                        {'User-agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
                        {'User-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
                        {'User-agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'}]

    def catch_data(self):
        i =1

        while True:
            a = i%5
            url = self._url+str(i)
            #print(url)
            s = requests.session() 
            s.keep_alive = False
            response = s.get(url, headers=self._headers[a])
            print(self._headers[a])
            response.encoding = response.apparent_encoding
            response=response.text

            soup = BeautifulSoup(response, "html.parser")
            contents = soup.find(id="search_result_container").find_all('a')
         
            for content in contents:
                try:
                    name = content.find(class_="title").get_text()
                    date = content.find("div",class_="col search_released responsive_secondrow").get_text()
                    if self._discount == True:
                        price= content.find("div",class_="col search_price discounted responsive_secondrow").get_text()
                    elif self._discount == False:
                        price= content.find("div",class_="col search_price responsive_secondrow").get_text()
                    #img_src = content.find("div",class_="col search_capsule").find('img').get("src")
                    href=content.get("href")

                    self._gameUrl.append(href)
                    self._gameName.append(name)
                    self._gamePrice.append(price)
                    self._publishDate.append(date)
                except:
                    print("something error!")
            
            if len(self._gameUrl)>=100:
                break
            i=i+1

    def extract(self):
        self.catch_data()
        ticks = [time.time()]
        ticks = list(ticks)
        ticks.extend([""]*(len(self._gameName)-len(ticks)))

        test = pd.DataFrame({'time':ticks,'name':self._gameName,'price':self._gamePrice,'date':self._publishDate,'url':self._gameUrl})
        print(test)
        path = './'+self._fileName+str(ticks[0])+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)
        return path

def main():
    data=steam("https://store.steampowered.com/search/?filter=globaltopsellers&page=",'steam_topseller_',discount=False)
    filePath1=data.extract()
    
    data=steam("https://store.steampowered.com/search/?os=win&specials=1&page=",'steam_specials_',discount=True)
    filePath2=data.extract()

if __name__ == '__main__':
    main()
