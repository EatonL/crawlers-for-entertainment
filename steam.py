import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def catch_data(root_path,discount=False):
    i =1
    game_url=[]
    game_name=[]
    game_price=[]
    publish_date=[] 

    while True:
        url = root_path+str(i)
        print(url)
        s = requests.session()
        res = s.get(url).text
        soup = BeautifulSoup(res, "html.parser")
        contents = soup.find(id="search_result_container").find_all('a')
        
   
        for content in contents:
            try:
                name = content.find(class_="title").get_text()
                date = content.find("div",class_="col search_released responsive_secondrow").get_text()
                if discount == True:
                    price= content.find("div",class_="col search_price discounted responsive_secondrow").get_text()
                elif discount == False:
                    price= content.find("div",class_="col search_price responsive_secondrow").get_text()
                #img_src = content.find("div",class_="col search_capsule").find('img').get("src")
                href=content.get("href")
                print(name)

                game_url.append(href)
                game_name.append(name)
                game_price.append(price)
                publish_date.append(date)
            except:
                print("something error!")
            
        if len(game_url)>=100:
            break
        i=i+1
    return game_name,game_price,publish_date,game_url

def extract(game_name,game_price,publish_date,game_url,file_name):
    ticks = [time.time()]
    ticks = list(ticks)
    ticks.extend([""]*(len(game_name)-len(ticks)))

    test = pd.DataFrame({'time':ticks,'name':game_name,'price':game_price,'date':publish_date,'url':game_url})
    print(test)
    path = './'+file_name+str(ticks[0])+'.csv'
    test.to_csv(path,encoding='utf-8-sig',index=False)

def main():
    topseller_name,topseller_price,topseller_date,topseller_url=catch_data("https://store.steampowered.com/search/?filter=globaltopsellers&page=",discount=False)
    extract(topseller_name,topseller_price,topseller_date,topseller_url,'steam_topseller_')
    
    specials_name,specials_price,specials_date,specials_url=catch_data("https://store.steampowered.com/search/?os=win&specials=1&page=",discount=True)
    extract(specials_name,specials_price,specials_date,specials_url,'steam_specials_')

if __name__ == '__main__':
    main()

