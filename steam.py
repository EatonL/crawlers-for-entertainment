import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

class steam(object):
    def __init__(self,url,file_name,discount):
        self.url=url
        self.file_name=file_name
        self.discount=discount
        self.game_url=[]
        self.game_name=[]
        self.game_price=[]
        self.publish_date=[]
        self.headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    def catch_data(self):
        i =1 

        while True:
            url = self.url+str(i)
            #print(url)
            s = requests.session() 
            s.keep_alive = False
            response = s.get(url, headers=self.headers)
            response.encoding = response.apparent_encoding
            response=response.text

            soup = BeautifulSoup(response, "html.parser")
            contents = soup.find(id="search_result_container").find_all('a')
         
            for content in contents:
                try:
                    name = content.find(class_="title").get_text()
                    date = content.find("div",class_="col search_released responsive_secondrow").get_text()
                    if self.discount == True:
                        price= content.find("div",class_="col search_price discounted responsive_secondrow").get_text()
                    elif self.discount == False:
                        price= content.find("div",class_="col search_price responsive_secondrow").get_text()
                    #img_src = content.find("div",class_="col search_capsule").find('img').get("src")
                    href=content.get("href")

                    self.game_url.append(href)
                    self.game_name.append(name)
                    self.game_price.append(price)
                    self.publish_date.append(date)
                except:
                    print("something error!")
            
            if len(self.game_url)>=100:
                break
            i=i+1

    def extract(self):
        self.catch_data()
        ticks = [time.time()]
        ticks = list(ticks)
        ticks.extend([""]*(len(self.game_name)-len(ticks)))

        test = pd.DataFrame({'time':ticks,'name':self.game_name,'price':self.game_price,'date':self.publish_date,'url':self.game_url})
        print(test)
        path = './'+self.file_name+str(ticks[0])+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)

def main():
    data=steam("https://store.steampowered.com/search/?filter=globaltopsellers&page=",'steam_topseller_',discount=False)
    data.extract()
    
    data=steam("https://store.steampowered.com/search/?os=win&specials=1&page=",'steam_specials_',discount=True)
    data.extract()

if __name__ == '__main__':
    main()